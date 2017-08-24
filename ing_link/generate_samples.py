#!/usr/bin/env python3

from doc_reader.entity_classes import *

"""Given a recipe, generate positive and negative samples for training and
testing"""

def generate_samples(recipe_obj):
    """
    recipe_obj: a PreprocessedRecipe object
    
    returns: a list of (boolean, (entity1, entity2)) tuples, each boolean value
    is a label indicating whether the two entities are related.
    """
    ing_ing_entities = [ent for ent in recipe_obj.get_ing_entities() 
                            if isinstance(ent, Ingredient)]
    ins_ing_entities = [ent for ent in recipe_obj.get_ins_entities() 
                            if isinstance(ent, Ingredient)]
    samples = []
    for ing_ing_ent in ing_ing_entities:
        for ins_ing_ent in ins_ing_entities:
            samples.append((recipe_obj.are_related(ing_ing_ent, ins_ing_ent), 
                           (ing_ing_ent, ins_ing_ent)))
    return samples
