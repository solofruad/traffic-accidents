#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 15 11:26:25 2019

@author: hat
"""

import pandas as pd  # For data handling
#from classes.tfidf.preprocessing import Preprocessing as tfidf
from sklearn.model_selection import train_test_split

names = ['7030','5050','100']

for name in names:
    filename = "data/v1/dataset_"+name+".tsv"
    dataset = pd.read_csv(filename, delimiter = "\t", quoting = 3)
    
    #clean = tfidf(dataset)
    #clean.fit_clean()
    
    X, y = dataset.text, dataset.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 123)

    train = pd.concat([X_train,y_train],axis=1)
    train.to_csv("data/v1/"+name+"/train70.tsv",sep='\t', index=False)

    test = pd.concat([X_test,y_test],axis=1)
    test.to_csv("data/v1/"+name+"/test30.tsv",sep='\t', index=False)


#Test
for name in names:
    print("#Dataset "+name)
    aux = pd.read_csv("data/v1/dataset_"+name+".tsv", delimiter = "\t", quoting = 3)
    X, y = aux.text, aux.label
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.30, random_state = 123)
    X_train.shape
    aux70 = pd.read_csv("data/v1/"+name+"/train70.tsv", delimiter = "\t", quoting = 3)
    print("Train comparation: "+str(aux70.shape[0] == X_train.shape[0]))
    aux30 = pd.read_csv("data/v1/"+name+"/test30.tsv", delimiter = "\t", quoting = 3)
    print("Test comparation: "+str(aux30.shape[0] == X_test.shape[0]))
    print("\n")