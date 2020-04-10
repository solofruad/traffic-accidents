#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 13 14:41:57 2020

@author: hat
"""

import pandas as pd
import numpy as np

import pickle
import time


token_user = pd.read_csv("data/database/server_token_user.tsv", delimiter = "\t", quoting = 3)
token_user = token_user.sample(n=1000)

filename = 'notebook/0 Generating Model/accident_clasification_model.pkl'
accident_clasification_model = pickle.load(open(filename, 'rb'))

text_test = [
    "choque entre camion y carro particular",
    "caí por accidente en tu corazón", 
    "accidente aereo deja 100 muertos en australia"
]
start = time.perf_counter()

text_predict = accident_clasification_model.predict(token_user['text'])
token_user['label'] = text_predict

end = time.perf_counter()
print(end - start)



accident = token_user[token_user['label'] == 1 ]
no_accident = token_user[token_user['label'] == 0 ]


accident.to_csv("data/database/output_ml/accident_3_server_token_user.tsv",sep='\t')
no_accident.to_csv("data/database/output_ml/no_accident_3_server_token_user.tsv",sep='\t')


count_tweet_by_username = accident['user_name'].value_counts() # Show distribution of tweets by user

#text_predict = text_predict.reshape(1000,1)



#tweet = np.asarray(text_test)
#tweet = tweet.reshape(1000,1)

#data = np.concatenate((tweet, text_predict), axis=1)

#df = pd.DataFrame(data, columns=["text","label"])




