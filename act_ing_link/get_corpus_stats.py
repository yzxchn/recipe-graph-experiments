#!/usr/bin/env python3

from doc_reader.recipe_data_reader import PreprocessedRecipe
from collections import Counter
import os

train_names = [l.strip() for l in open("./data/train/names.txt")]
dev_names = [l.strip() for l in open("./data/dev/names.txt")]
test_names = [l.strip() for l in open("./data/test/names.txt")]
DATA_ROOT = "./data"

recipes = []

for name in train_names:
    ing_path = os.path.join(DATA_ROOT, "train", "ing_entity", name+".ient")
    ins_path = os.path.join(DATA_ROOT, "train", "instruct_entity", 
                            name+".entity")
    link_path = os.path.join(DATA_ROOT, "train", "link", name+".link")
    atts_path = os.path.join(DATA_ROOT, "train", "atts", name+".atts")
    with open(ing_path) as ing, \
         open(ins_path) as ins, \
         open(link_path) as link, \
         open(atts_path) as atts:
        recipe = PreprocessedRecipe(ing, ins, link, atts)
        recipes.append(recipe)

for name in test_names:
    ing_path = os.path.join(DATA_ROOT, "test", "ing_entity", name+".ient")
    ins_path = os.path.join(DATA_ROOT, "test", "instruct_entity", 
                            name+".entity")
    link_path = os.path.join(DATA_ROOT, "test", "link", name+".link")
    atts_path = os.path.join(DATA_ROOT, "test", "atts", name+".atts")
    with open(ing_path) as ing, \
         open(ins_path) as ins, \
         open(link_path) as link, \
         open(atts_path) as atts:
        recipe = PreprocessedRecipe(ing, ins, link, atts)
        recipes.append(recipe)

for name in dev_names: 
    ing_path = os.path.join(DATA_ROOT, "dev", "ing_entity", name+".ient")
    ins_path = os.path.join(DATA_ROOT, "dev", "instruct_entity", 
                            name+".entity")
    link_path = os.path.join(DATA_ROOT, "dev", "link", name+".link")
    atts_path = os.path.join(DATA_ROOT, "dev", "atts", name+".atts")
    with open(ing_path) as ing, \
         open(ins_path) as ins, \
         open(link_path) as link, \
         open(atts_path) as atts:
        recipe = PreprocessedRecipe(ing, ins, link, atts)
        recipes.append(recipe)
ent_count = Counter()
flow_count = Counter()
coref_count = Counter()
for r in recipes:
    ing_entities = r.get_ing_entities()
    ins_entities = r.get_ins_entities()
    for e in ing_entities:
        ent_count[e.id[0]] += 1
    for e in ins_entities:
        ent_count[e.id[0]] += 1

    coref_links = r.coref_links
    flow_links = r.flow_links
    for c1, c2 in coref_links:
        k1 = c1[0]
        k2 = c2[0]
        coref_count["{}-{}".format(k1, k2)] += 1
    for f1, f2 in flow_links:
        k1 = f1[0]
        k2 = f2[0]
        flow_count["{}-{}".format(k1, k2)] += 1

print(ent_count)
print(flow_count)
print(coref_count)





