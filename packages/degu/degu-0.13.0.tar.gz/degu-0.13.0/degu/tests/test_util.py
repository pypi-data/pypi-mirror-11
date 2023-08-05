# degu: an embedded HTTP server and client library
# Copyright (C) 2014 Novacut Inc
#
# This file is part of `degu`.
#
# `degu` is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.
#
# `degu` is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with `degu`.  If not, see <http://www.gnu.org/licenses/>.
#
# Authors:
#   Jason Gerard DeRose <jderose@novacut.com>

"""
Unit tests for the `degu.util` module`
"""

from unittest import TestCase
from collections import namedtuple

from degu import util


class TestFunctions(TestCase):
    def test_shift_path(self):
        Request = namedtuple('Request', 'script path')

        # both script and path are empty:
        request = Request([], [])
        with self.assertRaises(IndexError):
            util.shift_path(request)
        self.assertEqual(request.script, [])
        self.assertEqual(request.path, [])

        # path is empty:
        request = Request(['foo'], [])
        with self.assertRaises(IndexError):
            util.shift_path(request)
        self.assertEqual(request.script, ['foo'])
        self.assertEqual(request.path, [])

        # start with populated path:
        request = Request([], ['foo', 'bar', 'baz'])
        self.assertEqual(util.shift_path(request), 'foo')
        self.assertEqual(request.script, ['foo'])
        self.assertEqual(request.path, ['bar', 'baz'])

        self.assertEqual(util.shift_path(request), 'bar')
        self.assertEqual(request.script, ['foo', 'bar'])
        self.assertEqual(request.path, ['baz'])

        self.assertEqual(util.shift_path(request), 'baz')
        self.assertEqual(request.script, ['foo', 'bar', 'baz'])
        self.assertEqual(request.path, [])

        with self.assertRaises(IndexError):
            util.shift_path(request)
        self.assertEqual(request.script, ['foo', 'bar', 'baz'])
        self.assertEqual(request.path, [])

    def test_relative_uri(self):
        Request = namedtuple('Request', 'path query')

        path_permutations = (
            (tuple(),            '/'),
            (('',),              '/'),
            (('foo',),           '/foo'),
            (('foo', ''),        '/foo/'),
            (('foo', 'bar'),     '/foo/bar'),
            (('foo', 'bar', ''), '/foo/bar/'),
        )
        query_permutations = (
            (None,      ''),
            ('',        '?'),
            ('foo',     '?foo'),
            ('foo=bar', '?foo=bar'),
        )
        for (path, uri) in path_permutations:
            request = Request(list(path), None)
            self.assertEqual(util.relative_uri(request), uri)
            self.assertEqual(request.path, list(path))
        for (query, end) in query_permutations:
            request = Request([], query)
            self.assertEqual(util.relative_uri(request), '/' + end)
            self.assertEqual(request.path, [])
        for (path, uri) in path_permutations:
            for (query, end) in query_permutations:
                request = Request(list(path), query)
                self.assertEqual(util.relative_uri(request), uri + end)
                self.assertEqual(request.path, list(path))

        # path is empty:
        request = Request([], None)
        self.assertEqual(util.relative_uri(request), '/')
        self.assertEqual(request.path, [])

        request = Request([], '')
        self.assertEqual(util.relative_uri(request), '/?')
        self.assertEqual(request.path, [])

        request = Request([], 'foo')
        self.assertEqual(util.relative_uri(request), '/?foo')
        self.assertEqual(request.path, [])

        request = Request([], 'foo=bar')
        self.assertEqual(util.relative_uri(request), '/?foo=bar')
        self.assertEqual(request.path, [])

        # No query
        request = Request([''], None)
        self.assertEqual(util.relative_uri(request), '/')
        self.assertEqual(request.path, [''])

        request = Request(['foo'], None)
        self.assertEqual(util.relative_uri(request), '/foo')
        self.assertEqual(request.path, ['foo'])

        request = Request(['foo', ''], None)
        self.assertEqual(util.relative_uri(request), '/foo/')
        self.assertEqual(request.path, ['foo', ''])

        request = Request(['foo', 'bar'], None)
        self.assertEqual(util.relative_uri(request), '/foo/bar')
        self.assertEqual(request.path, ['foo', 'bar'])

        request = Request(['foo', 'bar', ''], None)
        self.assertEqual(util.relative_uri(request), '/foo/bar/')
        self.assertEqual(request.path, ['foo', 'bar', ''])

    def test_absolute_uri(self):
        Request = namedtuple('Request', 'script path query')

        path_permutations = (
            (tuple(),            '/'),
            (('',),              '/'),
            (('foo',),           '/foo'),
            (('foo', ''),        '/foo/'),
            (('foo', 'bar'),     '/foo/bar'),
            (('foo', 'bar', ''), '/foo/bar/'),
        )
        query_permutations = (
            (None,      ''),
            ('',        '?'),
            ('foo',     '?foo'),
            ('foo=bar', '?foo=bar'),
        )

        for (path, uri) in path_permutations:
            request = Request([], list(path), None)
            self.assertEqual(util.absolute_uri(request), uri)
            self.assertEqual(request.script, [])
            self.assertEqual(request.path, list(path))
            s = []
            p = list(path)
            while p:
                s.append(p.pop(0))
                request = Request(list(s), list(p), None)
                self.assertEqual(util.absolute_uri(request), uri)
                self.assertEqual(request.script, s)
                self.assertEqual(request.path, p)

        for (query, end) in query_permutations:
            request = Request([], [], query)
            self.assertEqual(util.absolute_uri(request), '/' + end)
            self.assertEqual(request.script, [])
            self.assertEqual(request.path, [])

        for (path, uri) in path_permutations:
            for (query, end) in query_permutations:
                request = Request([], list(path), query)
                self.assertEqual(util.absolute_uri(request), uri + end)
                self.assertEqual(request.script, [])
                self.assertEqual(request.path, list(path))
                s = []
                p = list(path)
                while p:
                    s.append(p.pop(0))
                    request = Request(list(s), list(p), query)
                    self.assertEqual(util.absolute_uri(request), uri + end)
                    self.assertEqual(request.script, s)
                    self.assertEqual(request.path, p)

        # script, path, and query are all empty:
        request = Request([], [], None)
        self.assertEqual(util.absolute_uri(request), '/')
        self.assertEqual(request.script, [])
        self.assertEqual(request.path, [])

        # only script:
        request = Request(['foo'], [], None)
        self.assertEqual(util.absolute_uri(request), '/foo')
        self.assertEqual(request.script, ['foo'])
        self.assertEqual(request.path, [])

        request = Request(['foo', ''], [], None)
        self.assertEqual(util.absolute_uri(request), '/foo/')
        self.assertEqual(request.script, ['foo', ''])
        self.assertEqual(request.path, [])

        request = Request(['foo', 'bar'], [], None)
        self.assertEqual(util.absolute_uri(request), '/foo/bar')
        self.assertEqual(request.script, ['foo', 'bar'])
        self.assertEqual(request.path, [])

        request = Request(['foo', 'bar', ''], [], None)
        self.assertEqual(util.absolute_uri(request), '/foo/bar/')
        self.assertEqual(request.script, ['foo', 'bar', ''])
        self.assertEqual(request.path, [])

        # only path:
        request = Request([], ['foo'], None)
        self.assertEqual(util.absolute_uri(request), '/foo')
        self.assertEqual(request.script, [])
        self.assertEqual(request.path, ['foo'])

        request = Request([], ['foo', ''], None)
        self.assertEqual(util.absolute_uri(request), '/foo/')
        self.assertEqual(request.script, [])
        self.assertEqual(request.path, ['foo', ''])

        request = Request([], ['foo', 'bar'], None)
        self.assertEqual(util.absolute_uri(request), '/foo/bar')
        self.assertEqual(request.script, [])
        self.assertEqual(request.path, ['foo', 'bar'])

        request = Request([], ['foo', 'bar', ''], None)
        self.assertEqual(util.absolute_uri(request), '/foo/bar/')
        self.assertEqual(request.script, [])
        self.assertEqual(request.path, ['foo', 'bar', ''])

        # only query:
        request = Request([], [], 'hello')
        self.assertEqual(util.absolute_uri(request), '/?hello')
        self.assertEqual(request.script, [])
        self.assertEqual(request.path, [])

        request = Request([], [], 'stuff=junk')
        self.assertEqual(util.absolute_uri(request), '/?stuff=junk')
        self.assertEqual(request.script, [])
        self.assertEqual(request.path, [])

        # All of the above:
        request = Request(['foo'], ['bar'], 'hello')
        self.assertEqual(util.absolute_uri(request), '/foo/bar?hello')
        self.assertEqual(request.script, ['foo'])
        self.assertEqual(request.path, ['bar'])

        request = Request(['foo'], ['bar', ''], 'hello')
        self.assertEqual(util.absolute_uri(request), '/foo/bar/?hello')
        self.assertEqual(request.script, ['foo'])
        self.assertEqual(request.path, ['bar', ''])

        request = Request(['foo'], ['bar'], 'one=two')
        self.assertEqual(util.absolute_uri(request), '/foo/bar?one=two')
        self.assertEqual(request.script, ['foo'])
        self.assertEqual(request.path, ['bar'])

        request = Request(['foo'], ['bar', ''], 'one=two')
        self.assertEqual(util.absolute_uri(request), '/foo/bar/?one=two')
        self.assertEqual(request.script, ['foo'])
        self.assertEqual(request.path, ['bar', ''])

