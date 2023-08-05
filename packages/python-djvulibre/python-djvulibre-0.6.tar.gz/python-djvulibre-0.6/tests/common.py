# encoding=UTF-8

# Copyright © 2010-2015 Jakub Wilk <jwilk@jwilk.net>
#
# This package is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; version 2 dated June, 1991.
#
# This package is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.

import codecs
import contextlib
import locale
import os
import re
import sys

from nose.tools import (
    assert_true,
    assert_false,
    assert_equal,
    assert_not_equal,
)
from nose import SkipTest

if sys.version_info >= (2, 7):
    from nose.tools import (
        assert_in,
        assert_is,
        assert_is_instance,
        assert_less,
        assert_list_equal,
        assert_multi_line_equal,
        assert_not_in,
        assert_raises,
    )
    if sys.version_info >= (3, 2):
        from nose.tools import assert_raises_regex
        from nose.tools import assert_regex
    else:
        from nose.tools import assert_raises_regexp as assert_raises_regex
        from nose.tools import assert_regexp_matches as assert_regex
    type(assert_multi_line_equal.__self__).maxDiff = None
else:
    def assert_in(x, y):
        assert_true(
            x in y,
            msg='{0!r} not found in {1!r}'.format(x, y)
        )
    def assert_is(x, y):
        assert_true(
            x is y,
            msg='{0!r} is not {1!r}'.format(x, y)
        )
    def assert_is_instance(obj, cls):
        assert_true(
            isinstance(obj, cls),
            msg='{0!r} is not an instance of {1!r}'.format(obj, cls)
        )
    def assert_less(x, y):
        assert_true(
            x < y,
            msg='{0!r} not less than {1!r}'.format(x, y)
        )
    assert_list_equal = assert_equal
    assert_multi_line_equal = assert_equal
    def assert_not_in(x, y):
        assert_true(
            x not in y,
            msg='{0!r} unexpectedly found in {1!r}'.format(x, y)
        )
    class assert_raises(object):
        def __init__(self, exc_type):
            self._exc_type = exc_type
            self.exception = None
        def __enter__(self):
            return self
        def __exit__(self, exc_type, exc_value, tb):
            if exc_type is None:
                assert_true(False, '{0} not raised'.format(self._exc_type.__name__))
            if not issubclass(exc_type, self._exc_type):
                return False
            if isinstance(exc_value, exc_type):
                pass
                # This branch is not always taken in Python 2.6:
                # https://bugs.python.org/issue7853
            elif isinstance(exc_value, tuple):
                exc_value = exc_type(*exc_value)
            else:
                exc_value = exc_type(exc_value)
            self.exception = exc_value
            return True
    @contextlib.contextmanager
    def assert_raises_regex(exc_type, regex):
        with assert_raises(exc_type) as ecm:
            yield
        assert_regex(str(ecm.exception), regex)
    def assert_regex(text, regex):
        if isinstance(regex, basestring):
            regex = re.compile(regex)
        if not regex.search(text):
            message = "Regex didn't match: {0!r} not found in {1!r}".format(regex.pattern, text)
            assert_true(False, msg=message)

@contextlib.contextmanager
def assert_raises_str(exc_type, s):
    with assert_raises(exc_type) as ecm:
        yield
    assert_equal(str(ecm.exception), s)

try:
    locale.LC_MESSAGES
except AttributeError:
    # A non-POSIX system.
    locale.LC_MESSAGES = locale.LC_ALL

locale_encoding = locale.getpreferredencoding()
if codecs.lookup(locale_encoding) == codecs.lookup('US-ASCII'):
    locale_encoding = 'UTF-8'

py3k = sys.version_info >= (3, 0)

if py3k:
    def u(s):
        return s
else:
    def u(s):
        return s.decode('UTF-8')

if py3k:
    def b(s):
        return s.encode('UTF-8')
else:
    def b(s):
        return s

if py3k:
    def L(i):
        return i
else:
    def L(i):
        return long(i)

if py3k:
    def cmp(x, y):
        if x == y:
            return 0
        if x < y:
            return -1
        if x > y:
            return 1
        assert 0
else:
    cmp = cmp

if py3k:
    def blob(*args):
        return bytes(args)
else:
    def blob(*args):
        return ''.join(map(chr, args))

if py3k:
    from io import StringIO
else:
    from io import BytesIO as StringIO

if py3k:
    unicode = str
else:
    unicode = unicode

if py3k:
    maxsize = sys.maxsize
else:
    maxsize = sys.maxint

@contextlib.contextmanager
def interim(obj, **override):
    copy = dict((key, getattr(obj, key)) for key in override)
    for key, value in override.items():
        setattr(obj, key, value)
    try:
        yield
    finally:
        for key, value in copy.items():
            setattr(obj, key, value)

@contextlib.contextmanager
def interim_locale(**kwargs):
    old_locale = locale.setlocale(locale.LC_ALL)
    try:
        for category, value in kwargs.items():
            category = getattr(locale, category)
            try:
                locale.setlocale(category, value)
            except locale.Error:
                _, exc, _ = sys.exc_info()
                raise SkipTest(exc)
        yield
    finally:
        locale.setlocale(locale.LC_ALL, old_locale)

def assert_repr(self, expected):
    return assert_equal(repr(self), expected)

def skip_unless_c_messages():
    if locale.setlocale(locale.LC_MESSAGES) != 'C':
        raise SkipTest('you need to run this test with LC_MESSAGES=C')
    if os.getenv('LANGUAGE', '') != '':
        raise SkipTest('you need to run this test with LANGUAGE unset')

def skip_unless_translation_exists(lang):
    messages = {}
    langs = ['C', lang]
    for lang in langs:
        with interim_locale(LC_ALL=lang):
            try:
                open(__file__ + '/')
            except EnvironmentError:
                _, exc, _ = sys.exc_info()
                messages[lang] = str(exc)
    messages = set(messages.values())
    assert 1 <= len(messages) <= 2
    if len(messages) == 1:
        raise SkipTest('libc translation not found: ' + lang)

def skip_unless_command_exists(command):
    directories = os.environ['PATH'].split(os.pathsep)
    for directory in directories:
        path = os.path.join(directory, command)
        if os.access(path, os.X_OK):
            return
    raise SkipTest('command not found: ' + command)

def wildcard_import(mod):
    ns_orig = {}
    exec('', ns_orig)
    ns = {}
    exec('from {mod} import *'.format(mod=mod), ns)
    for key in ns_orig:
        del ns[key]
    return ns

__all__ = [
    # Python 2/3 compat:
    'L',
    'StringIO',
    'b',
    'blob',
    'cmp',
    'maxsize',
    'py3k',
    'u',
    'unicode',
    # nose
    'SkipTest',
    'assert_equal',
    'assert_false',
    'assert_in',
    'assert_is',
    'assert_is_instance',
    'assert_less',
    'assert_list_equal',
    'assert_multi_line_equal',
    'assert_not_equal',
    'assert_not_in',
    'assert_raises',
    'assert_raises_regex',
    'assert_regex',
    'assert_true',
    # misc
    'assert_raises_str',
    'assert_repr',
    'interim',
    'interim_locale',
    'locale_encoding',
    'skip_unless_c_messages',
    'skip_unless_command_exists',
    'skip_unless_translation_exists',
    'wildcard_import',
]

# vim:ts=4 sts=4 sw=4 et
