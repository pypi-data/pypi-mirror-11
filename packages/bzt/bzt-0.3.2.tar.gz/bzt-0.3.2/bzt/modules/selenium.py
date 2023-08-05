"""
Module holds selenium stuff
"""
from abc import abstractmethod

import os
import time
import shutil
import sys
import subprocess
import urwid

from bzt.engine import ScenarioExecutor, Scenario
from bzt.utils import RequiredTool, shell_exec, shutdown_process, BetterDict, JavaVM
from bzt.six import string_types, text_type
from bzt.modules.aggregator import ConsolidatingAggregator
from bzt.modules.console import WidgetProvider
from bzt.modules.jmeter import JTLReader


class SeleniumExecutor(ScenarioExecutor, WidgetProvider):
    """
    Selenium executor
    """
    SELENIUM_DOWNLOAD_LINK = "http://selenium-release.storage.googleapis.com/{version}/" \
                             "selenium-server-standalone-{version}.0.jar"
    SELENIUM_VERSION = "2.46"

    JUNIT_DOWNLOAD_LINK = "http://search.maven.org/remotecontent?filepath=junit/junit/{version}/junit-{version}.jar"
    JUNIT_VERSION = "4.12"

    SUPPORTED_TYPES = [".py", ".jar", ".java"]

    def __init__(self):
        super(SeleniumExecutor, self).__init__()
        self.start_time = None
        self.end_time = None
        self.runner = None
        self.widget = None
        self.reader = None
        self.kpi_file = None

    def prepare(self):
        """
        1) Locate script or folder
        2) detect script type
        3) create runner instance, prepare runner
        """
        scenario = self.get_scenario()
        self.kpi_file = self.engine.create_artifact("selenium_tests_report", ".csv")
        script_type, script_is_folder = self.detect_script_type(scenario.get("script"))
        runner_config = BetterDict()

        if script_type == ".py":
            self.runner = NoseTester
            runner_config = self.settings.get("selenium-tools").get("nose")

        elif script_type == ".jar" or script_type == ".java":
            self.runner = JunitTester
            runner_config = self.settings.get("selenium-tools").get("junit")

        runner_config["script-type"] = script_type
        runner_working_dir = self.engine.create_artifact(runner_config.get("working-dir", "classes"), "")
        runner_config["working-dir"] = runner_working_dir
        runner_config.get("artifacts-dir", self.engine.artifacts_dir)
        runner_config.get("working-dir", runner_working_dir)
        runner_config.get("report-file", self.kpi_file)

        if Scenario.SCRIPT in scenario:
            if script_is_folder:
                shutil.copytree(scenario.get("script"), runner_working_dir)
            else:
                os.makedirs(runner_working_dir)
                shutil.copy2(scenario.get("script"), runner_working_dir)

        self.runner = self.runner(runner_config, scenario, self.log)

        runner_std_out = self.engine.create_artifact("runner_out", ".log")
        runner_std_err = self.engine.create_artifact("runner_err", ".log")
        self.runner.prepare(runner_std_out, runner_std_err)
        self.reader = JTLReader(self.kpi_file, self.log, None)
        if isinstance(self.engine.aggregator, ConsolidatingAggregator):
            self.engine.aggregator.add_underling(self.reader)

    def detect_script_type(self, script_path):
        """
        checks if script is java or python
        if it's folder or single script
        :return:
        """
        if not isinstance(script_path, string_types) and not isinstance(script_path, text_type):
            raise RuntimeError("Nothing to test, no files were provided in scenario")
        script_path_is_directory = False
        test_files = []
        for dir_entry in os.walk(script_path):
            if dir_entry[2]:
                for test_file in dir_entry[2]:
                    if os.path.splitext(test_file)[1].lower() in SeleniumExecutor.SUPPORTED_TYPES:
                        test_files.append(test_file)

        if os.path.isdir(script_path):
            file_ext = os.path.splitext(test_files[0])[1].lower()
            script_path_is_directory = True
        else:
            file_ext = os.path.splitext(script_path)[1]

        if file_ext not in SeleniumExecutor.SUPPORTED_TYPES:
            raise RuntimeError("Supported tests types %s was not found" % SeleniumExecutor.SUPPORTED_TYPES)
        return file_ext, script_path_is_directory

    def startup(self):
        """
        Start runner
        :return:
        """
        self.start_time = time.time()
        self.runner.run_tests()

    def check(self):
        """
        check if test completed
        :return:
        """
        if self.widget:
            self.widget.update()

        return self.runner.is_finished()

    def shutdown(self):
        """
        shutdown test_runner
        :return:
        """
        self.runner.shutdown()

        if self.start_time:
            self.end_time = time.time()
            self.log.debug("Selenium tests ran for %s seconds", self.end_time - self.start_time)

        if self.kpi_file:
            if (not os.path.exists(self.kpi_file) or not os.path.getsize(self.kpi_file)) and not self.runner.is_failed:
                msg = "Empty runner report, most likely runner failed: %s"
                raise RuntimeWarning(msg % self.kpi_file)

    def get_widget(self):
        if not self.widget:
            self.widget = SeleniumWidget(self.get_scenario().get("script"), self.runner.opened_descriptors["std_out"].name)
        return self.widget


class AbstractTestRunner(object):
    """
    Abstract test runner
    """

    def __init__(self, settings, scenario):
        self.process = None
        self.settings = settings
        self.required_tools = []
        self.scenario = scenario
        self.report_file = self.settings.get("report-file")
        self.artifacts_dir = self.settings.get("artifacts-dir")
        self.working_dir = self.settings.get("working-dir")
        self.log = None
        self.opened_descriptors = {"std_err": None, "std_out": None}
        self.is_failed = False

    @abstractmethod
    def prepare(self, file_std_out, file_std_err):
        pass

    @abstractmethod
    def run_checklist(self):
        pass

    @abstractmethod
    def run_tests(self):
        pass

    def is_finished(self):
        ret_code = self.process.poll()
        if ret_code is not None:
            if ret_code != 0:
                self.log.debug("Test runner exit code: %s", ret_code)
                with open(self.opened_descriptors["std_err"].name) as fds:
                    std_err = fds.read()
                self.is_failed = True
                raise RuntimeError("Test runner %s has failed: %s" % (self.__class__.__name__, std_err.strip()))
            return True
        return False

    def check_tools(self):
        for tool in self.required_tools:
            if not tool.check_if_installed():
                self.log.info("Installing %s", tool.tool_name)
                tool.install()

    def shutdown(self):
        shutdown_process(self.process, self.log)
        for desc in self.opened_descriptors.values():
            desc.close()
        self.opened_descriptors = {}


class JunitTester(AbstractTestRunner):
    """
    Allows to test java and jar files
    """

    def __init__(self, junit_config, scenario, parent_logger):
        super(JunitTester, self).__init__(junit_config, scenario)
        self.log = parent_logger.getChild(self.__class__.__name__)
        path_lambda = lambda key, val: os.path.abspath(os.path.expanduser(self.settings.get(key, val)))

        self.junit_path = path_lambda("path", "~/.bzt/selenium-taurus/tools/junit/junit.jar")
        self.selenium_server_jar_path = path_lambda("selenium-server", "~/.bzt/selenium-taurus/selenium-server.jar")
        self.junit_listener_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "resources",
                                                "taurus_junit.jar")

        self.base_class_path = [self.selenium_server_jar_path, self.junit_path, self.junit_listener_path]
        self.base_class_path.extend(self.scenario.get("additional-classpath", []))

    def prepare(self, std_out, std_err):
        """
        run checklist, make jar.
        """
        self.run_checklist()

        if self.settings.get("script-type", None) == ".java":
            self.compile_scripts()

        std_out_desc = open(std_out, "wt")
        std_err_desc = open(std_err, "wt")
        self.opened_descriptors["std_err"] = std_err_desc
        self.opened_descriptors["std_out"] = std_out_desc

    def run_checklist(self):
        """
        java
        javac
        selenium-server.jar
        junit.jar
        junit_listener.jar
        """

        if self.settings.get("script_type", None) == ".java":
            self.required_tools.append(JavaC("", "", self.log))
        self.required_tools.append(JavaVM("", "", self.log))
        self.required_tools.append(SeleniumServerJar(self.selenium_server_jar_path,
                                                     SeleniumExecutor.SELENIUM_DOWNLOAD_LINK.format(
                                                         version=SeleniumExecutor.SELENIUM_VERSION), self.log))
        self.required_tools.append(JUnitJar(self.junit_path, SeleniumExecutor.JUNIT_DOWNLOAD_LINK.format(
            version=SeleniumExecutor.JUNIT_VERSION)))
        self.required_tools.append(JUnitListenerJar(self.junit_listener_path, ""))

        self.check_tools()

    def compile_scripts(self):
        """
        Compile .java files
        """
        self.log.debug("Compiling .java files started")
        java_files = []

        for dir_entry in os.walk(self.working_dir):
            if dir_entry[2]:
                for test_file in dir_entry[2]:
                    if os.path.splitext(test_file)[1].lower() == ".java":
                        java_files.append(os.path.join(dir_entry[0], test_file))

        compile_cl = ["javac", "-cp", os.pathsep.join(self.base_class_path)]
        compile_cl.extend(java_files)

        with open(os.path.join(self.artifacts_dir, "javac_out"), 'ab') as javac_out:
            with open(os.path.join(self.artifacts_dir, "javac_err"), 'ab') as javac_err:
                self.process = shell_exec(compile_cl, cwd=self.working_dir, stdout=javac_out, stderr=javac_err)
                ret_code = self.process.poll()

                while ret_code is None:
                    self.log.debug("Compiling .java files...")
                    time.sleep(1)
                    ret_code = self.process.poll()

        if ret_code != 0:
            self.log.debug("javac exit code: %s", ret_code)
            with open(javac_err.name) as err_file:
                out = err_file.read()
            raise RuntimeError("Javac exited with error:\n %s" % out.strip())

        self.log.info("Compiling .java files completed")

        self.make_jar()

    def make_jar(self):
        """
        move all .class files to compiled.jar
        """
        self.log.debug("Making .jar started")

        with open(os.path.join(self.artifacts_dir, "jar_out"), 'ab') as jar_out:
            with open(os.path.join(self.artifacts_dir, "jar_err"), 'ab') as jar_err:
                class_files = [java_file for java_file in os.listdir(self.working_dir) if java_file.endswith(".class")]
                jar_name = self.settings.get("jar-name", "compiled.jar")
                if class_files:
                    compile_jar_cl = ["jar", "-cf", jar_name]
                    compile_jar_cl.extend(class_files)
                else:
                    package_dir = os.listdir(self.working_dir)[0]
                    compile_jar_cl = ["jar", "-cf", jar_name, "-C", package_dir, "."]

                self.process = shell_exec(compile_jar_cl, cwd=self.working_dir, stdout=jar_out, stderr=jar_err)
                ret_code = self.process.poll()

                while ret_code is None:
                    self.log.debug("Making jar file...")
                    time.sleep(1)
                    ret_code = self.process.poll()

        if ret_code != 0:
            with open(jar_err.name) as err_file:
                out = err_file.read()
            self.log.info("Making jar failed with code %s", ret_code)
            self.log.info("jar output: %s", out)
            raise RuntimeError("Jar exited with non-zero code")

        self.log.info("Making .jar file completed")

    def run_tests(self):
        # java -cp junit.jar:selenium-test-small.jar:
        # selenium-2.46.0/selenium-java-2.46.0.jar:./../selenium-server.jar
        # org.junit.runner.JUnitCore TestBlazemeterPass

        jar_list = [os.path.join(self.working_dir, jar) for jar in os.listdir(self.working_dir) if jar.endswith(".jar")]
        self.base_class_path.extend(jar_list)

        junit_command_line = ["java", "-cp", os.pathsep.join(self.base_class_path),
                              "taurus_junit_listener.CustomRunner"]
        junit_command_line.extend(jar_list)
        junit_command_line.extend([self.report_file])

        self.process = shell_exec(junit_command_line, cwd=self.artifacts_dir,
                                  stdout=self.opened_descriptors["std_out"],
                                  stderr=self.opened_descriptors["std_err"])


class NoseTester(AbstractTestRunner):
    """
    Python selenium tests runner
    """

    def __init__(self, nose_config, scenario, parent_logger):
        super(NoseTester, self).__init__(nose_config, scenario)
        self.log = parent_logger.getChild(self.__class__.__name__)
        self.plugin_path = os.path.join(os.path.dirname(__file__), "resources", "nose_plugin.py")

    def prepare(self, std_out, std_err):
        self.run_checklist()
        std_out_desc = open(std_out, "wt")
        std_err_desc = open(std_err, "wt")
        self.opened_descriptors["std_err"] = std_err_desc
        self.opened_descriptors["std_out"] = std_out_desc

    def run_checklist(self):
        """
        we need installed nose plugin
        """
        if sys.version >= '3':
            self.log.warn("You are using python3, make sure that your scripts are able to run in python3!")

        self.required_tools.append(
            TaurusNosePlugin(self.plugin_path, ""))

        self.check_tools()

    def run_tests(self):
        """
        run python tests
        """
        executable = self.settings.get("interpreter", sys.executable)
        nose_command_line = [executable, self.plugin_path, self.report_file, self.working_dir]

        self.process = shell_exec(nose_command_line, cwd=self.artifacts_dir,
                                  stdout=self.opened_descriptors["std_out"],
                                  stderr=self.opened_descriptors["std_err"])


class SeleniumWidget(urwid.Pile):
    def __init__(self, script, runner_output):
        widgets = []
        self.script_name = urwid.Text("Tests: %s" % script)
        self.summary_stats = urwid.Text("")
        self.current_test = urwid.Text("")
        self.runner_output = runner_output
        self.position = 0
        widgets.append(self.script_name)
        widgets.append(self.summary_stats)
        widgets.append(self.current_test)
        super(SeleniumWidget, self).__init__(widgets)

    def update(self):
        cur_test, reader_summary = ["No data received yet"] * 2
        if os.path.exists(self.runner_output):
            with open(self.runner_output, "rt") as fds:
                fds.seek(self.position)
                line = fds.readline()

                if line and "," in line:
                    cur_test, reader_summary = line.split(",")

        self.current_test.set_text(cur_test)
        self.summary_stats.set_text(reader_summary)
        self._invalidate()

class SeleniumServerJar(RequiredTool):
    def __init__(self, tool_path, download_link, parent_logger):
        super(SeleniumServerJar, self).__init__("Selenium server", tool_path, download_link)
        self.log = parent_logger.getChild(self.__class__.__name__)

    def check_if_installed(self):
        self.log.debug("%s path: %s", self.tool_name, self.tool_path)
        selenium_launch_command = ["java", "-jar", self.tool_path, "-help"]
        selenium_subproc = shell_exec(selenium_launch_command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        output = selenium_subproc.communicate()
        self.log.debug("%s output: %s", self.tool_name, output)
        if selenium_subproc.returncode == 0:
            self.already_installed = True
            return True
        else:
            return False


class JUnitJar(RequiredTool):
    def __init__(self, tool_path, download_link):
        super(JUnitJar, self).__init__("JUnit", tool_path, download_link)


class JavaC(RequiredTool):
    def __init__(self, tool_path, download_link, parent_logger):
        super(JavaC, self).__init__("JavaC", tool_path, download_link)
        self.log = parent_logger.getChild(self.__class__.__name__)

    def check_if_installed(self):
        try:
            output = subprocess.check_output(["javac", '-version'], stderr=subprocess.STDOUT)
            self.log.debug("%s output: %s", self.tool_name, output)
            return True
        except BaseException:
            raise RuntimeError("The %s is not operable or not available. Consider installing it" % self.tool_name)

    def install(self):
        raise NotImplementedError()


class JUnitListenerJar(RequiredTool):
    def __init__(self, tool_path, download_link):
        super(JUnitListenerJar, self).__init__("JUnitListener", tool_path, download_link)

    def install(self):
        raise NotImplementedError()


class TaurusNosePlugin(RequiredTool):
    def __init__(self, tool_path, download_link):
        super(TaurusNosePlugin, self).__init__("TaurusNosePlugin", tool_path, download_link)

    def install(self):
        raise NotImplementedError()
