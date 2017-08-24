#!/usr/bin/env python3
from doc_reader.recipe_data_reader import PreprocessedRecipe
from doc_reader.entity_classes import *
from generate_samples import generate_samples
from evaluation import *
import os

train_names = [l.strip() for l in open("./data/train/names.txt")]
dev_names = [l.strip() for l in open("./data/dev/names.txt")]
test_names = [l.strip() for l in open("./data/test/names.txt")]
DATA_ROOT = "./data"

#extractor = FeatureExtractor(feature_functions=baseline_features)

## get training samples
#sample_labels = []
#sample_pairs = []
#sample_recipes = []
#for name in train_names: 
#    ing_path = os.path.join(DATA_ROOT, "train", "ing_entity", name+".ient")
#    ins_path = os.path.join(DATA_ROOT, "train", "instruct_entity", 
#                            name+".entity")
#    link_path = os.path.join(DATA_ROOT, "train", "link", name+".link")
#    atts_path = os.path.join(DATA_ROOT, "train", "atts", name+".atts")
#    with open(ing_path) as ing, \
#         open(ins_path) as ins, \
#         open(link_path) as link, \
#         open(atts_path) as atts:
#        recipe = PreprocessedRecipe(ing, ins, link, atts)
#        samples_in_recipe = generate_samples(recipe)
#        for label, pair in samples_in_recipe:
#            sample_labels.append(label)
#            sample_pairs.append(pair)
#            sample_recipes.append(recipe)
#
## Extract Features
#features = extractor.extract_features(sample_pairs, sample_recipes)
#
## Training
#cls = LinearSVMClassifier()
#cls.train(sample_labels, features)

def baseline_predictor(entity1, entity2, recipe_obj):
    """If entity1 and entity2 have exactly one other Action entity in between, 
    believe that they are connected"""
    entities = recipe_obj.get_ins_entities()
    ent1_i = -1
    ent2_i = -1
    for i in range(len(entities)):
        if entities[i] is entity1:
            ent1_i = i
        elif entities[i] is entity2:
            ent2_i = i
    assert ent1_i >=0 and ent2_i >= 0 and ent1_i < ent2_i
    act_count = 0
    for i in range(ent1_i+1, ent2_i):
        if isinstance(entities[i], Action):
            act_count += 1
    return act_count == 1

    
def predict(pair_list, recipe_list, predictor):
    assert len(pair_list) == len(recipe_list)
    result = []
    for i in range(len(pair_list)):
        e1, e2 = pair_list[i]
        result.append(predictor(e1, e2, recipe_list[i]))
    return result


# Dev Testing
dev_labels = []
dev_pairs = []
dev_recipes = []
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
        samples_in_recipe = generate_samples(recipe)
        for label, pair in samples_in_recipe:
            dev_labels.append(label)
            dev_pairs.append(pair)
            dev_recipes.append(recipe)
predicted_labels = predict(dev_pairs, dev_recipes, baseline_predictor)

print("Dev Test Errors:")
false_negatives, false_positives = get_error_indexes(dev_labels, 
                                                    predicted_labels)
print("False Negatives:")
for i in false_negatives:
    ent1, ent2 = dev_pairs[i]
    line = dev_recipes[i].ins_lines[ent1.sent_i]
    print(" ".join(line))
    print("{} | {} Predicted: {}".format(ent1.text, ent2.text, 
                                       predicted_labels[i]))
    print()
print()
print("False Positives:")
for j in false_positives:
    ent1, ent2 = dev_pairs[j]
    line = dev_recipes[j].ins_lines[ent1.sent_i]
    print(" ".join(line))
    print("{} | {} Predicted: {}".format(ent1.text, ent2.text, 
                                       predicted_labels[j]))
    print()

# Testing
test_labels = []
test_pairs = []
test_recipes = []
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
        samples_in_recipe = generate_samples(recipe)
        for label, pair in samples_in_recipe:
            test_labels.append(label)
            test_pairs.append(pair)
            test_recipes.append(recipe)
predicted_labels = predict(test_pairs, test_recipes, baseline_predictor)


# Evaluating
p, r, a, f = evaluate(test_labels, predicted_labels)

print("Precision: {} Recall: {} Accuracy: {} F-1 Score: {}".format(p, r, a, f))

# Get errors;
print("Errors:")
false_negatives, false_positives = get_error_indexes(test_labels, 
                                                    predicted_labels)
print("False Negatives:")
for i in false_negatives:
    ent1, ent2 = test_pairs[i]
    print("{} | {} Predicted: {}".format(ent1.text, ent2.text, 
                                       predicted_labels[i]))
print()
print("False Positives:")
for j in false_positives:
    ent1, ent2 = test_pairs[j]
    print("{} | {} Predicted: {}".format(ent1.text, ent2.text, 
                                       predicted_labels[j]))
