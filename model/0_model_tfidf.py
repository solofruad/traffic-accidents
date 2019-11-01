#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
    URL de Interes:
        https://scikit-learn.org/stable/modules/cross_validation.html        
        https://towardsdatascience.com/train-test-split-and-cross-validation-in-python-80b61beca4b6
        https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_validate.html
        https://scikit-learn.org/stable/auto_examples/model_selection/plot_grid_search_digits.html        
"""


import pandas as pd  # For data handling
#import numpy as np

from classes.tfidf.preprocessing import Preprocessing as tfidf
from classes.tfidf.preprocessing_lemma import Preprocessing as tfidf_lemma

"""-------------------------------DATASETS-----------------------------------------------"""

train = pd.read_csv("data/v1/7030/train70.tsv", delimiter = "\t", quoting = 3)
train['dataset'] = "train"
test = pd.read_csv("data/v1/7030/test30.tsv", delimiter = "\t", quoting = 3)
test['dataset'] = "test"
#dataset = pd.concat([train,test])
"""-------------------------------PREPROCESSING-----------------------------------------------"""

#clean = tfidf(train)
#clean.fit_clean()
clean = tfidf_lemma(train)
train = clean.fit_clean()
#embendding = clean.feature_extraction(ngram_range=(1,2), max_df=0.45, min_df=0.001, max_features=None)
embendding, vectorizer = clean.feature_extraction(ngram_range=(1,2), max_df=0.5, min_df=0.001, max_features=None)

#print(train_clean.getWordFeatures)

"""-------------------------------TRAIN & TEST-----------------------------------------------"""
vecs_train = embendding[embendding[:,0] == 'train',:]
vecs_test = embendding[embendding[:,0] == 'test',:]

X_train = vecs_train[:,2:]
X_train=X_train.astype('float')

y_train = vecs_train[:,1]
y_train=y_train.astype('int')

#X_test = vecs_test[:,2:]
#X_test=X_test.astype('float')
#y_test = vecs_test[:,1]
#y_test=y_test.astype('int')


clean = tfidf_lemma(test)
test = clean.fit_clean()
#clean = tfidf(test)
#clean.fit_clean()
#doc = test.iloc[1][3]
X_test, y_test = vectorizer.transform(test.clean).toarray(), test.label

#X = embendding[:,1:]
#y = embendding[:,0]
# Splitting the dataset into the Training set and Test set
#from sklearn.model_selection import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 123)

"""----------------------------------MODEL---------------------------------------------------"""

"""----------------------------------NAIVE BAYES---------------------------------------------------"""

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB

classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results

y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

cm_nb = confusion_matrix(y_test, y_pred)

metrics_nb = []
metrics = {}
metrics['accuracy'] = accuracy_score(y_test, y_pred)
metrics['recall'] = recall_score(y_test, y_pred)
metrics['precision'] = precision_score(y_test, y_pred)
metrics['f1'] = f1_score(y_test, y_pred)
metrics_nb.append(metrics)
metrics_nb = pd.DataFrame(metrics_nb)

"""----------------------------------LINEAR SVM---------------------------------------------------"""

#from sklearn.svm import LinearSVC
#classifier = LinearSVC(random_state=123, tol=1e-4)
#classifier = LinearSVC(random_state=123, tol=1)

from sklearn.svm import SVC
classifier = SVC(random_state=123, kernel='rbf', gamma=0.7, C=5)

classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

cm_svm = confusion_matrix(y_test, y_pred)

metrics_svm = []
metrics = {}    
metrics['accuracy'] = accuracy_score(y_test, y_pred)
metrics['recall'] = recall_score(y_test, y_pred)
metrics['precision'] = precision_score(y_test, y_pred)
metrics['f1'] = f1_score(y_test, y_pred)
metrics_svm.append(metrics)
metrics_svm = pd.DataFrame(metrics_svm)

"""----------------------------------Graficando---------------------------------------------------"""

import numpy as np
X = np.concatenate((X_train, X_test), axis=0)
y = np.concatenate((y_train, y_test), axis=0)

from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA(n_components=2).fit(X)
datapoint = pca.transform(X)

plt.figure

label1 = ["#32C12C", #0. GREEN
          "#009888", #1. TEAL
          "#3E49BB", #2. INDIGO
          "#526EFF",#3. AZUL
          "#7F4FC9", #4. purple
          "#FFEF00", #5. YELOW
          "#FF9A00", #6. ORANGE
          "#7C5547", #7. BROWN
          "#5F7D8E", #8. BLUE GREY
          "#FF5500", #9. DEEP ORANGE
          "#87C735", #10. LIGHT GREEN
          "#CDE000", #11. LIME
          "#00A5F9", #12. LIGHT BLUE
          "#00BCD9",  #13. CYAN
          "#682CBF"] #14. DEEP PURPLE          

color = [label1[int(i)] for i in y]
plt.scatter(datapoint[:, 0], datapoint[:, 1], alpha=0.7, c=color)

plt.show()