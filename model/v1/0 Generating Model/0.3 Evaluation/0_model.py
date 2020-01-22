#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd  # For data handling


from classes.doc2vec.preprocessing import Preprocessing as doc2vec

"""-------------------------------DATASETS-----------------------------------------------"""

"""positive = pd.read_csv("data/positive/positive_7030.tsv", delimiter = "\t", quoting = 3)
negative = pd.read_csv("data/negative/negative_7030.tsv", delimiter = "\t", quoting = 3)

positive['label'] = 1
negative['label'] = 0

#positive = positive.sample(n=20)
#negative = negative.sample(n=20)

dataset = pd.concat([positive,negative])
dataset = dataset.sample(frac=1)"""

train = pd.read_csv("data/v1/7030/train70.tsv", delimiter = "\t", quoting = 3)
train['dataset'] = 99 # train = 1
test = pd.read_csv("data/v1/7030/test30.tsv", delimiter = "\t", quoting = 3)
test['dataset'] = 100 # test = 0
dataset = pd.concat([train,test])
dataset = dataset.reset_index(drop=True)

"""-------------------------------PREPROCESSING-----------------------------------------------"""

clean = doc2vec(dataset)
clean.fit_clean()
embendding = clean.feature_extraction(200,200,402)

"""-------------------------------TRAIN & TEST-----------------------------------------------"""
vecs_train = embendding[embendding[:,0] == 99.0,:]
vecs_test = embendding[embendding[:,0] == 100.0,:]

X_train = vecs_train[:,2:]
y_train = vecs_train[:,1]
X_test = vecs_test[:,2:]
y_test = vecs_test[:,1]


#X = embendding[:,2:]
#y = embendding[:,1]
# Splitting the dataset into the Training set and Test set
#from sklearn.model_selection import train_test_split
#X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

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
#classifier = LinearSVC(random_state=0, tol=1e-4)

from sklearn.svm import SVC
classifier = SVC(random_state=123, kernel='linear', gamma=0.7, C=0.1)
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

X = embendding[:,2:]
y = embendding[:,1]

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
