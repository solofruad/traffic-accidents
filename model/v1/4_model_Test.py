#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 17:58:26 2020

@author: hat
"""

import pandas as pd
import numpy as np
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import SVC

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

import pickle

from classes.tweet2accident.preprocessing import Preprocessing

train = pd.read_csv("data/v1/7030/train70.tsv", delimiter = "\t", quoting = 3)
test = pd.read_csv("data/v1/7030/test30.tsv", delimiter = "\t", quoting = 3)

X, y = train.text, train.label
X_test, y_test = test.text, test.label

type_clean = 5 # The type clean in this case 5 corresponding to 5_steam

#TFIDF
max_df = 0.5    
max_features = 800
min_df = 0.001
ngram_range= (1, 1)

#SVM
C=4
gamma=0.7
kernel= 'rbf'

pipeline = Pipeline([
    ('transform', Preprocessing(type_clean=type_clean, njobs=4)),
    ('tfidf', TfidfVectorizer(ngram_range=ngram_range, max_df=max_df, min_df=min_df, max_features=max_features)),
    ('clf', SVC(random_state=123, kernel=kernel, C=C, gamma=gamma))
])

pipeline.fit(X, y)
#aux2 = pipeline.transform(X)

y_pred = pipeline.predict(X_test)
#y_pred = pipeline.predict(["Accidente en la callse 100"])

#text_pref = pipeline.predict(["accidente calle"])

cm_svm = confusion_matrix(y_test, y_pred)

metrics_svm = []
metrics = {}
metrics['accuracy'] = accuracy_score(y_test, y_pred)
metrics['recall'] = recall_score(y_test, y_pred)
metrics['precision'] = precision_score(y_test, y_pred)
metrics['f1'] = f1_score(y_test, y_pred)
metrics_svm.append(metrics)
metrics_svm = pd.DataFrame(metrics_svm)

print(metrics_svm)
print(cm_svm)


# save the model to disk
filename = 'accident_clasification_model.pkl'
with open(filename, 'wb') as model_file:
      pickle.dump(pipeline, model_file)


# load the model from disk
accident_clasification_model = pickle.load(open(filename, 'rb'))
result = accident_clasification_model.score(X_test, y_test)
print(result)

text_pred = accident_clasification_model.predict(["choque entre camion y carro particular"])