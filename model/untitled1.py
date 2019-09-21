#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 19:42:20 2019

@author: hat
"""
from pymongo import MongoClient
from datetime import datetime
import pandas as pd
from datetime import timedelta
import multiprocessing

def process_cursor(skip_n,limit_n):
    client = MongoClient('localhost', 27017) # Conecting database
    db = client.dataset # Created instance of database
    collection = db.server_token_user
    
    start = datetime(2018, 10, 1, 5, 0, 0)
    end = datetime(2019, 10, 1, 19, 0, 0)
    
    
    cursor = collection.find({ 'created_at': {'$gte': start, '$lt': end}  }, no_cursor_timeout=True).skip(skip_n).limit(limit_n)    
    df = pd.DataFrame(list(cursor))
    
    #df = pd.DataFrame()
    """count = 0
    for doc in cursor:
        count += 1 
        df = df.append(pd.Series(doc),ignore_index=True)
        if count % 10000 == 0:
            print(count)
        #print(doc)
        """

n_cores = 4
collection_size = 100618
batch_size = round(collection_size/n_cores+0.5)
skips = range(0, n_cores*batch_size, batch_size)

for skip_n in skips:
    print(skip_n)
processes = [ multiprocessing.Process(target=process_cursor, args=(skip_n,batch_size)) for skip_n in skips]

for process in processes:
    process.start()

for process in processes:
    process.join()
    
    
for i in range(3,10,4):
    print(i)

n = 4027313
lista = [0] * n
n_cores = 4
batch_size = round(n/n_cores+0.5)
cores = range(n_cores)
for c in cores:
    init = batch_size * c
    end = init + (batch_size)
    end = end if end <= n else n
    print("init: %s, end: %s" %(init,end))    
    for i in range(init,end):
        lista[i] = 1
        
zeros = [i for i in lista if i==0]