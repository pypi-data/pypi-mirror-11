#!/usr/bin/env python
# encoding: utf-8

import os
try:
	from StringIO import StringIO

# StringIO does not exist in python3
except ImportError as e:
	from io import StringIO
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pfp
import pfp.fields
import pfp.interp
import pfp.utils

import utils

class TestFunctions(unittest.TestCase, utils.UtilsMixin):
	def setUp(self):
		pass
	
	def tearDown(self):
		pass
	
	def test_function(self):
		dom = self._test_parse_build(
			"",
			"""
				void func(int a, int b) {
					local int c = a + b;
				}

				func(10, 20);
			"""
		)
	
	def test_builtin(self):
		dom = self._test_parse_build(
			"",
			"""
				Printf("hello there");
				Printf("%d", 10);
			""",
			stdout="hello there10"
		)
	
	def test_custom_func(self):
		dom = self._test_parse_build(
			"",
			"""
				int add(int n1, int n2) {
					return n1 + n2;
				}

				Printf("%d", add(5, 8));
			""",
			stdout="13"
		)
	
	def test_custom_func2(self):
		dom = self._test_parse_build(
			"",
			"""
				string prepend(string orig) {
					return "blah: " + orig;
				}

				Printf(prepend("hello"));
			""",
			stdout="blah: hello"
		)
	
	def test_native_func(self):
		func_called = False
		def func(params, ctxt, scope, stream, coord):
			func_called = True
			return 555

		interp = pfp.interp.PfpInterp()
		interp.add_native(name="func", func=func, ret=pfp.fields.Int)

		dom = self._test_parse_build(
			"",
			"""
			Printf("%d", func());
			""",
			stdout="555"
		)
	
	def test_lazy_type_checking(self):
		dom = self._test_parse_build(
			"\x0a",
			"""
				void lazy_type_checking_function(LazyType &blah) {
					Printf("blah.var1 = %d", blah.var1);
				}

				typedef struct LazyType {
					uchar var1;
				} LAZY_TYPE_TYPE;

				LAZY_TYPE_TYPE a;
				lazy_type_checking_function(a);
			""",
			stdout="blah.var1 = 10"
		)
	
	def test_function_string_return(self):
		dom = self._test_parse_build(
			"abcd\x00",
			"""
				string ReadStringN(int64 pos, int n) {
					local uchar s[n];
					ReadBytes(s, pos, n);
					return s;
				}
				if(ReadStringN(FTell(), 5) == "abcd") {
					Printf("true");
				} else {
					Printf("false");
				}
			""",
			verify=False,
			stdout="true"
		)
	
if __name__ == "__main__":
	unittest.main()
