"""
Module for reporting into http://www.blazemeter.com/ service

Copyright 2015 BlazeMeter Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
# pylint: skip-file

import types
import urllib
import urllib2
import urlparse
import operator
import ConfigParser
import Tkinter
import tkFont
import UserDict
import StringIO
import collections

string_types = basestring,
integer_types = (int, long)
class_types = (type, types.ClassType)
text_type = unicode
binary_type = str

configparser = ConfigParser
tkinter = Tkinter
Tk = Tkinter.Tk
Text = Tkinter.Text
tkfont = tkFont
UserDict = UserDict.UserDict
BytesIO = StringIO.StringIO
StringIO = StringIO.StringIO

parse = urlparse
request = urllib
urlopen = urllib2.urlopen
urlencode = urllib.urlencode
build_opener = urllib2.build_opener
install_opener = urllib2.install_opener
ProxyHandler = urllib2.ProxyHandler
Request = urllib2.Request

viewvalues = operator.methodcaller("viewvalues")


def iteritems(dictionary, **kw):
    return iter(dictionary.iteritems(**kw))


def b(string):
    return string


def u(string):
    return unicode(string.replace(r'\\', r'\\\\'), "unicode_escape")
