#!/usr/bin/env python3

"""An interface for Scikit-learn Linear SVM classifier.
"""

from sklearn.svm import LinearSVC
from sklearn.feature_extraction import DictVectorizer
import pickle

class LinearSVMClassifier:
    def __init__(self, model=None, vectorizer=None):
        """Initialize the classifier.

        model: a previously trained LinearSVC object
        vectorizer: an exisiting DictVectorizer object
        """
        if vectorizer:
            self.vectorizer = vectorizer
        else:
            self.vectorizer = DictVectorizer()
        self.model = model

    def train(self, labels, features):
        """Train a LinearSVM classifier
        labels: a list of class labels
        features: a list of python dictionary of (feature_name, feature_value) 
                  pairs. features[i] is the collection of features that 
                  corresponds with labels[i]
        """
        self.model = LinearSVC()
        feature_vectors = self.vectorizer.fit_transform(features)
        self.model.fit(feature_vectors, labels)

    def classify(self, features):
        feature_vectors = self.vectorizer.transform(features)
        return self.model.predict(feature_vectors)

    def dump(self, out_file):
        pickle.dump(self.model, out_file)
        

        
