#!/usr/bin/env python3
from feature_functions import *
from doc_reader.recipe_data_reader import PreprocessedRecipe
from generate_samples import generate_samples
from linear_svm_classifier import LinearSVMClassifier
from evaluation import *
import os

train_names = [l.strip() for l in open("./ing_link_data/train/names.txt")]
dev_names = [l.strip() for l in open("./ing_link_data/dev/names.txt")]
test_names = [l.strip() for l in open("./ing_link_data/test/names.txt")]
DATA_ROOT = "./ing_link_data"
baseline_features = [nl_before_comma_distance,
                     nl_before_comma_vector_similarity, 
                     num_noun_lemma_matches,  
                     lemma_match_frequency_sum, 
                     contain_measurement, 
                     freq_sum_inst_position_similarity, 
                     relative_position_similarity]

extractor = FeatureExtractor(feature_functions=baseline_features)

# get training samples
sample_labels = []
sample_pairs = []
sample_recipes = []
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
        samples_in_recipe = generate_samples(recipe)
        for label, pair in samples_in_recipe:
            sample_labels.append(label)
            sample_pairs.append(pair)
            sample_recipes.append(recipe)

# Extract Features
features = extractor.extract_features(sample_pairs, sample_recipes)

# Training
cls = LinearSVMClassifier()
cls.train(sample_labels, features)

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
dev_features = extractor.extract_features(dev_pairs, dev_recipes)
predicted_labels = cls.classify(dev_features)

print("Dev Test Errors:")
false_negatives, false_positives = get_error_indexes(dev_labels, 
                                                    predicted_labels)
print("False Negatives:")
for i in false_negatives:
    ent1, ent2 = dev_pairs[i]
    print("{} | {} Predicted: {}".format(ent1.text, ent2.text, 
                                       predicted_labels[i]))
print()
print("False Positives:")
for j in false_positives:
    ent1, ent2 = dev_pairs[j]
    print("{} | {} Predicted: {}".format(ent1.text, ent2.text, 
                                       predicted_labels[j]))

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
test_features = extractor.extract_features(test_pairs, test_recipes)
predicted_labels = cls.classify(test_features)


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
