#!/usr/bin/env python3

from doc_reader.entity_classes import *
from collections import defaultdict

"""Given a recipe, generate positive and negative samples for training and
testing"""

def generate_samples(recipe_obj):
    """
    recipe_obj: a PreprocessedRecipe object
    
    returns: a list of (boolean, (entity1, entity2)) tuples, each boolean value
    is a label indicating whether the two entities are related.
    """
    ins_entities = recipe_obj.get_ins_entities()
    samples = []
    entities_by_sent = defaultdict(list)
    for ent in ins_entities:
        entities_by_sent[ent.sent_i].append(ent)
    for sent in entities_by_sent.values():
        samples.extend(generate_samples_in_sent(sent, recipe_obj))
    return samples

def generate_samples_in_sent(sent, recipe_obj):
    samples = []
    for ent in sent:
        if isinstance(ent, Action):
            for ent_ in sent:
                if not isinstance(ent_, Action):
                    samples.append((recipe_obj.are_related(ent_, ent), 
                                   (ent_, ent)))
    return samples

