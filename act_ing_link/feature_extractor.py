#!/usr/bin/env python3

class FeatureExtractor:
    def __init__(self, feature_functions=[]):
        self.feature_functions = feature_functions

    def add_feature_function(self, feature_function):
        self.feature_functions.append(feature_function)

    def extract_features(self, entity_pairs, recipes):
        """Extract features from samples.
        entity_pairs: a list of tuples of two Entity objects.
        recipes: a list of RecipeReader objects
        len(entity_pairs) should equal len(recipes), each pair of entities 
        correspond to a recipe object they are in.
        """
        samples = zip(entity_pairs, recipes)
        features = []
        for pair, recipe in samples:
            entity1, entity2 = pair
            feature_set = {}
            for f in self.feature_functions:
                feature_name, feature_value = f(entity1, entity2, recipe)
                feature_set[feature_name] = feature_value
            features.append(feature_set)
        return features

