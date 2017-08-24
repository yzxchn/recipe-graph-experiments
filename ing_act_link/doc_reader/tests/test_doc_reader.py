#!/usr/bin/env python3
import unittest
import os

from ..entity_reader import *
from ..attribute_reader import *
from ..recipe_data_reader import *

class RecipeReaderTestCases(unittest.TestCase):
    def setUp(self):
        this_dir = os.path.dirname(os.path.realpath(__file__))
        test_ent_file_dir = os.path.join(this_dir, 
                                     "test_data/amish_white_bread.txt.entity")
        test_atts_file_dir = os.path.join(this_dir, 
                                     "test_data/amish_white_bread.txt.atts")
        test_ing_file_dir = os.path.join(this_dir, 
                                    "test_data/amish_white_bread.txt.ient")
        test_link_file_dir = os.path.join(this_dir, 
                                     "test_data/amish_white_bread.txt.link")

        self.atts_reader = AttributeReader(open(test_atts_file_dir))
        self.rd = RecipeEntityReader(open(test_ent_file_dir), 
                                          self.atts_reader)
        self.recipe = PreprocessedRecipe(open(test_ing_file_dir), 
                                         open(test_ent_file_dir), 
                                         open(test_link_file_dir), 
                                         open(test_atts_file_dir))
        
    def test_attributes_loaded(self):
        self.assertEqual(len(self.atts_reader.act_atts), 17)
        self.assertEqual(len(self.atts_reader.ing_atts), 17)

    def test_entities_loaded(self):
        self.assertEqual(len(self.rd.entities.values()), 33)
