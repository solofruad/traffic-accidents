#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 09:55:59 2020

@author: hat
"""

import pandas as pd
import numpy as np

import multiprocessing
import threading

#from classes.tweet2accident.preprocessing import Preprocessing
import time

import pickle

filename = "server_token_user.tsv"
token_user = pd.read_csv("data/database/"+filename, delimiter = "\t", quoting = 3)
token_user = token_user.sample(n=1000)
token_user = token_user.reset_index(drop=True)

cores = multiprocessing.cpu_count()

token_user['label'] = -1

#4027313

filename = 'notebook/0 Generating Model/accident_clasification_model.pkl'
accident_clasification_model = pickle.load(open(filename, 'rb'))

def iter_fn(threadId):    
    size = int(len(token_user)/cores)
    init = threadId*size
    end = len(token_user) if threadId == (cores-1) else size*(threadId+1)            
    for i in range(init,end):
        #token_user.at[i,'label'] = 0                
        token_user.at[i,'label'] = accident_clasification_model.predict([token_user.iloc[i]['text']])
        #token_user.set_value(i, 'label', 0)        
    print("Hilo ("+str(threadId)+"): "+str(init)+" - "+str(end) )    
    

threads = []
start = time.perf_counter()
for t in range(cores):        
    thread = threading.Thread(target=iter_fn, args=(t,))
    thread.start()
    threads.append(thread)
    #print(init,end)

for t in threads:
    t.join()
end = time.perf_counter()
print(end - start)


fake = token_user[token_user['label'] == -1 ]
"""token_user['label'] = text_predict

accident = token_user[token_user['label'] == 1 ]
no_accident = token_user[token_user['label'] == 0 ]

output_filename = "0_"+filename
accident.to_csv("data/database/output_ml/accident_"+output_filename,sep='\t')
no_accident.to_csv("data/database/output_ml/no_accident_"+output_filename,sep='\t')


count_tweet_by_username = accident['user_name'].value_counts() # Show distribution of tweets by user

"""