#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 23:38:36 2019

@author: hat
"""

import pandas as pd  # For data handling
import numpy as np


from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn import metrics

from gensim.models.doc2vec import Doc2Vec
from gensim.models.phrases import Phrases, Phraser

#######################################PARTE 1#####################################################

"""-------------------------------DATASETS-----------------------------------------------"""

dataset = pd.read_csv("data/dataset_accident_tweet.tsv", delimiter = "\t", quoting = 3)
dataset = dataset[['id_tweet','created_at','user_name','text','clean','label']]
#dataset = dataset.sort_values(by=['created_at'])

"""-------------------------------DOC2VEC-----------------------------------------------"""

#vecs = pd.read_csv("vector/vec-"+FNAME, delimiter = "\t", quoting = 3)
#del vecs["Unnamed: 0"]
#vecs = vecs.values

phraser_tg = Phraser.load("model/phraser_trigram-all-data.model")

dmm = Doc2Vec.load("model/dmm/5-d2v-dmm-trig-f200-w5.model")
dbow = Doc2Vec.load("model/dbow/5-d2v-dbow-unigram-f200-w5.model")

vecs_id_tweet = np.zeros((len(dataset.clean.values),1))
vecs_label = np.zeros((len(dataset.clean.values),1))
vecs_dbow = np.zeros((len(dataset.clean.values), 200))
vecs_dmm = np.zeros((len(dataset.clean.values), 200))
vecs = np.zeros((len(dataset.clean.values), 402))
n = 0    
for row in dataset.values:
    vecs_label[n] = row[5]
    vecs_id_tweet[n] = row[0]
    vecs_dbow[n] = dbow.infer_vector(row[4].split())        
    vecs_dmm[n] = dmm.infer_vector(phraser_tg[row[4].split()])
    vecs[n] = np.concatenate((vecs_id_tweet[n],vecs_label[n],vecs_dbow[n],vecs_dmm[n]))
    n=n+1
    

"""-------------------------------TRAIN & TEST-----------------------------------------------"""

X = vecs[:,2:]
y = vecs[:,1]
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)



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
cm = confusion_matrix(y_test, y_pred)

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)

from sklearn.metrics import recall_score
recall_score(y_test, y_pred)

from sklearn.metrics import precision_score
precision_score(y_test, y_pred)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred)


"""----------------------------------LINEAR SVM---------------------------------------------------"""

from sklearn.svm import LinearSVC
classifier = LinearSVC(random_state=0, tol=1e-4)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)

from sklearn.metrics import recall_score
recall_score(y_test, y_pred)

from sklearn.metrics import precision_score
precision_score(y_test, y_pred)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred)


"""----------------------------------Graficando---------------------------------------------------"""


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


dataset.iloc[243].id_tweet
dataset.iloc[243].text
vecs[243][0]
vecs[0][2:]
pred = classifier.predict([vecs[243][2:]])