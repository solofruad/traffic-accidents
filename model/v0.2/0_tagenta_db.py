#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul 14 14:49:18 2019

@author: hat
"""

import pandas as pd
from pymongo import MongoClient

client = MongoClient('localhost', 27017) # Conecting database
db = client.accident # Created instance of database

cursor = db.post.find({'complete':1}, no_cursor_timeout=True)

post = pd.DataFrame(list(cursor))

cursor = db.score.find({}, no_cursor_timeout=True)
score = pd.DataFrame(list(cursor))




post['_id'] = post['_id'].astype('str')
score['post'] = score['post'].astype('str')
score['_id'] = score['_id'].astype('str')

score['post'].astype('str')


dataset = []

for index, row in post.iterrows():    
    sub = score[score['post']==row['_id']]
    yes = 0
    no = 0
    none = 0    
    for i, r in sub.iterrows():    
        if r['label'] == 0:
            no = no + 1
        elif r['label'] == 1:
            yes = yes + 1
        else:
            none = none + 1    
    tweet = {}
    tweet['id_tweet'] = row['id_source']
    tweet['text'] = row['text']
    tweet['no'] = no
    tweet['none'] = none
    tweet['yes'] = yes
    dataset.append(tweet)    
    
        
result = pd.DataFrame(dataset)
        

yes = result[result['yes']>=2]
no = result[result['no']>=2]
no = no[no['yes']==0]
none = result[result['none']>=2]

yes.to_csv("data/tagg/labeling/positive-tagenta.tsv",sep='\t', index=False)
no.to_csv("data/tagg/labeling/negative-tagenta.tsv",sep='\t', index=False)


positive = pd.read_csv("data/tagg/labeling/positive-tagenta.tsv", delimiter = "\t",quoting = 3)
negative = pd.read_csv("data/tagg/labeling/negative-tagenta.tsv", delimiter = "\t",quoting = 3)






















        
        
        
        
        
        
        
        
        
        
        