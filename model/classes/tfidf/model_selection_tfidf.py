#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 18:11:02 2019

@author: hat
"""

import pandas as pd  # For data handling
import numpy as np

from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import LinearSVC
from sklearn.feature_extraction.text import TfidfVectorizer

from classes.tfidf.preprocessing import Preprocessing as tfidf


from pprint import pprint
from time import time


"""-------------------------------DATASETS-----------------------------------------------"""

#positive = pd.read_csv("data/positive/positive_7030.tsv", delimiter = "\t", quoting = 3)
#negative = pd.read_csv("data/negative/negative_7030.tsv", delimiter = "\t", quoting = 3)

#positive['label'] = 1
#negative['label'] = 0

##positive = positive.sample(n=40)
##negative = negative.sample(n=40)

#dataset = pd.concat([positive,negative])
#dataset = dataset.sample(frac=1)

dataset = pd.read_csv("data/v1/dataset_7030.tsv", delimiter = "\t", quoting = 3)

clean = tfidf(dataset)
clean.fit_clean()

"""pipeline = Pipeline([    
    ('tfidf', TfidfVectorizer()),
    ('clf', LinearSVC(random_state=123, tol=1e-4)),
])"""

from sklearn.svm import SVC
pipeline = Pipeline([
    ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_df=0.45, min_df=0.001, max_features=None)),
    ('clf', SVC(random_state=123)),   
])

"""parameters = {
        'tfidf__ngram_range': ((1,1),(1,2),(1,3)),
        'tfidf__max_df': (0.25,0.3, 0.35, 0.4, 0.45, 0.5, 0.6),
        'tfidf__min_df': (0.001,0.01,0.2),
        'tfidf__max_features': (None, 800, 1000, 1200, 1500, 1800, 2000),    
}"""

parameters = {
        'clf__C': (1,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,3),
        'clf__gamma': (0,6,0.7,0.8,0.9,1,2,3),
        'clf__kernel': ('linear', 'rbf')
}


print("Performing grid search...")
print("pipeline:", [name for name, _ in pipeline.steps])
print("parameters:")
pprint(parameters)
t0 = time()
grid_search = GridSearchCV(pipeline, parameters, cv=5, n_jobs=-1, verbose=1)
grid_search.fit(dataset.clean, dataset.label)
print("done in %0.3fs" % (time() - t0))
print()

print("Best score: %0.3f" % grid_search.best_score_)
print("Best parameters set:")
best_parameters = grid_search.best_estimator_.get_params()
for param_name in sorted(parameters.keys()):
    print("\t%s: %r" % (param_name, best_parameters[param_name]))
