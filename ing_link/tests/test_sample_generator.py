from ..generate_samples import generate_samples
from ..doc_reader.recipe_data_reader import PreprocessedRecipe

import unittest, os

class SampleGeneratorTestCases(unittest.TestCase):
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

        with open(test_ing_file_dir) as test_ing_file, \
             open(test_ent_file_dir) as test_ent_file, \
             open(test_link_file_dir) as test_link_file,\
             open(test_atts_file_dir) as test_atts_file:
            self.recipe = PreprocessedRecipe(test_ing_file,
                                             test_ent_file, 
                                             test_link_file, 
                                             test_atts_file)

    def test_generate_samples(self):
        self.assertEqual(len(generate_samples(self.recipe)), 66)

    def test_sample_correctness(self):
        related_pairs = [p for v, p in generate_samples(self.recipe) if v]
        self.assertEqual(len(related_pairs), 6)
