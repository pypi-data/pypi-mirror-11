# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function

import nose
from nose.tools import *
import unittest
import time

from collections import OrderedDict

from pksci.tools.datautils import TextLogGenerator


#class GeneratorTestFixtures(unittest.TestCase):
#    """Mixin unittest.TestCase class defining setUp/tearDown methods to
#    keep track of and delete the structure data files generated by the
#    sknano.generators classes."""
#
#    def setUp(self):
#        self.tmpdata = []
#
#    def tearDown(self):
#        for f in self.tmpdata:
#            try:
#                os.remove(f)
#            except IOError:
#                continue

test_fields_list = [{'directory': {'type': str, 'ptype': 's', 'width': 12}},
                    {'file': {'type': str, 'ptype': 's', 'width': 20}},
                    {'int': {'type': int, 'ptype': 'd', 'width': 10,
                             'precision': 8}},
                    {'bool': {'type': bool, 'width': 8}},
                    {'float': {'type': float, 'ptype': 'f', 'width': 15,
                               'precision':6}}]

test_log_fields = OrderedDict()

for field in test_fields_list:
    test_log_fields.update(field)


class TestTextLogGenerator(unittest.TestCase):

    def test1(self):
        txtlog = TextLogGenerator(fields=test_log_fields)
        print(txtlog)

        fields = {}
        fields.update({'directory': 'testdir1'})
        fields.update({'file': 'testfile1.txt'})
        fields.update({'int': 25})
        fields.update({'float': 3.14159})
        txtlog.write_fields(fields)

        fields.update({'directory': 'testdir2'})
        fields.update({'file': 'testfile2.txt'})
        fields.update({'int': 69})
        fields.update({'float': 2.71828})
        txtlog.write_fields(fields)

        #fields.update({'directory': 'testdir2'})
        fields.update({'file': 'testfile3.txt'})
        fields.update({'int': 0})
        fields.update({'float': 1.61803})
        txtlog.write_fields(fields)

        txtlog2 = TextLogGenerator(fields=test_log_fields,
                                   logfile=txtlog.logfile)
        print(txtlog2)

        fields = {}
        fields.update({'directory': 'testdir1'})
        fields.update({'file': 'testfile1.txt'})
        fields.update({'int': 25})
        fields.update({'float': 3.14159})
        txtlog2.write_fields(fields)

        fields.update({'directory': 'testdir2'})
        fields.update({'file': 'testfile2.txt'})
        fields.update({'int': 69})
        fields.update({'float': 2.71828})
        txtlog2.write_fields(fields)

        #fields.update({'directory': 'testdir2'})
        fields.update({'file': 'testfile3.txt'})
        fields.update({'int': 0})
        fields.update({'float': 1.61803})
        txtlog2.write_fields(fields)

        fields.update({'directory': 'testdir3'})
        fields.update({'file': 'testfile4.txt'})
        fields.update({'int': 0})
        fields.update({'float': 'nan'})
        txtlog2.write_fields(fields)

        time.sleep(1)
        txtlog3 = TextLogGenerator(fields=test_log_fields)
        fields.update({'bool': False})
        txtlog3.write_fields(fields)


if __name__ == '__main__':
    nose.runmodule()
