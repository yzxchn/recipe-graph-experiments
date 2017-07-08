#!/usr/bin/env python3
import unittest
import os

from ..doc_reader import *

class DocReaderTestCases(unittest.TestCase):
    def setUp(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        test_file_dir = os.path.join(this_dir, 
                                     "test_data/amish_white_bread.txt.entity")
        self.rd = RecipeEntityReader(test_file_dir)

    def test_entities_loaded(self):
        self.assertEqual(len(self.rd.entities.values()), 33)
