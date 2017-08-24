#!/usr/bin/env python3

from doc_reader.entity_classes import *

def generate_samples(recipe_obj):
    ins_entities = recipe_obj.get_ins_entities()
    samples = []
    for i in range(len(ins_entities)):
        # if ent is Ingredient and is not in start state
        ent = ins_entities[i]
        if isinstance(ent, Ingredient) and \
            recipe_obj.atts.get_ing_att(ent.id)[0] == "No":
            samples.extend(samples_from_ent(i, ins_entities, recipe_obj))
    return samples

def samples_from_ent(ent_index, entities, recipe_obj):
    ing_ent = entities[ent_index]
    samples = []
    connecting_act_indexes = []
    for i in range(ent_index):
        current_ent = entities[i]
        if isinstance(current_ent, Action) and \
            recipe_obj.are_related(current_ent, ing_ent):
                connecting_act_indexes.append(i)
    for i in connecting_act_indexes:
        samples.append((True, (entities[i], ing_ent)))
    # use Action-ing_ent pairs between the farthest Action entity connected to 
    # ing_ent as negative examples
    if connecting_act_indexes:
        for i in range(connecting_act_indexes[0], ent_index):
            if isinstance(entities[i], Action) and \
                i not in connecting_act_indexes:
                samples.append((False, (entities[i], ing_ent))) 
    return samples
