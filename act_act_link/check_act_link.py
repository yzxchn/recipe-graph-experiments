from get_samples import find_act_act_pairs
from doc_reader.recipe_data_reader import PreprocessedRecipe
from doc_reader.entity_classes import *
from collections import Counter
import os

train_names = [l.strip() for l in open("./data/train/names.txt")]
dev_names = [l.strip() for l in open("./data/dev/names.txt")]
test_names = [l.strip() for l in open("./data/test/names.txt")]
DATA_ROOT = "./data"

def sample(dataset_path, names):
    pairs = []
    for n in names:
        ing_path = os.path.join(dataset_path, "ing_entity", n+".ient")
        ins_path = os.path.join(dataset_path, "instruct_entity", 
                                n+".entity")
        link_path = os.path.join(dataset_path, "link", n+".link")
        atts_path = os.path.join(dataset_path, "atts", n+".atts")
        with open(ing_path) as ing, \
             open(ins_path) as ins, \
             open(link_path) as link, \
             open(atts_path) as atts:
            recipe = PreprocessedRecipe(ing, ins, link, atts)
            pairs.extend(find_act_act_pairs(recipe))
    return pairs

dataset_names = zip(("train", "test", "dev"), 
                    (train_names, test_names, dev_names))

act_act_pairs = []
for n, nameset in dataset_names:
    act_act_pairs.extend(sample(os.path.join(DATA_ROOT, n), nameset))

def act_act_distance(ent1, ent2, recipe):
    entities = recipe.get_ins_entities()
    act_num_between = 0
    seen_ent1 = False
    for i in range(len(entities)):
        if entities[i] is ent2:
            break
        elif entities[i] is ent1:
            seen_ent1 = True
        elif seen_ent1 and isinstance(entities[i], Action):
            act_num_between += 1
    return act_num_between

counts = Counter()
for pair, recipe in act_act_pairs:
    ent1, ent2 = pair
    dist = act_act_distance(ent1, ent2, recipe)
    counts[dist] += 1

    if dist != 0:
        for l in recipe.ins_lines:
            print(" ".join(l))
        print(ent1.text)
        print(ent2.text)
        print('------------------------------------')

