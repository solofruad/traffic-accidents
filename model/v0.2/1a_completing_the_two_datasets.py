#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:40:02 2019

@author: hat
"""

import pandas as pd
from pymongo import MongoClient
import datetime

positive_excel = pd.read_csv("data/tagg/labeling/positive.tsv",delimiter="\t",quoting=3)
positive_tagenta = pd.read_csv("data/tagg/labeling/positive-tagenta.tsv", delimiter="\t", quoting=3)

negative_excel = pd.read_csv("data/tagg/labeling/negative.tsv", delimiter="\t", quoting=3)
negative_tagenta = pd.read_csv("data/tagg/labeling/negative-tagenta.tsv",delimiter="\t", quoting=3)


client = MongoClient('localhost', 27017) # Conecting database
db = client.accident # Created instance of database

positive_tagenta["created_at"] = ""
positive_tagenta["user_name"] = ""

for index, row in positive_tagenta.iterrows():   
    cursor = db.complete.find({'id_tweet':str(row['id_tweet'])}, no_cursor_timeout=True)
    tweet = list(cursor)
    positive_tagenta.at[index,'created_at'] = tweet[0]['created_at']
    positive_tagenta.at[index,'user_name'] = tweet[0]['user_name']
    if index%100==0:
        print(index)
    

positive_tagenta.to_csv("data/tagg/labeling/positive-tagenta-complete.tsv",sep='\t', index=False)
positive = pd.read_csv("data/tagg/labeling/positive-tagenta-complete.tsv", delimiter = "\t",quoting = 3)

"""
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
"""
client = MongoClient('localhost', 27017) # Conecting database
db = client.accident # Created instance of database


positive_excel = pd.read_csv("data/tagg/labeling/positive.tsv",delimiter="\t",quoting=3)

positive_excel["created_at"] = ""
positive_excel["user_name"] = ""

for index, row in positive_excel.iterrows():   
    cursor = db.complete.find({'id_tweet':str(row['id_tweet'])}, no_cursor_timeout=True)
    tweet = list(cursor)
    positive_excel.at[index,'created_at'] = tweet[0]['created_at']
    positive_excel.at[index,'user_name'] = tweet[0]['user_name']
    if index%500==0:
        print(index)
    

positive_excel.to_csv("data/tagg/labeling/positive-excel-complete.tsv",sep='\t', index=False)
positive = pd.read_csv("data/tagg/labeling/positive-excel-complete.tsv", delimiter = "\t",quoting = 3)


"""
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
"""
client = MongoClient('localhost', 27017) # Conecting database
db = client.accident # Created instance of database


negative_excel = pd.read_csv("data/tagg/labeling/negative.tsv",delimiter="\t",quoting=3)

negative_excel["created_at"] = ""
negative_excel["user_name"] = ""

for index, row in negative_excel.iterrows():   
    cursor = db.complete.find({'id_tweet':str(row['id_tweet'])}, no_cursor_timeout=True)
    tweet = list(cursor)
    negative_excel.at[index,'created_at'] = tweet[0]['created_at']
    negative_excel.at[index,'user_name'] = tweet[0]['user_name']
    if index%1000==0:
        print(datetime.datetime.now())
        print(index)
    

negative_excel.to_csv("data/tagg/labeling/negative-excel-complete.tsv",sep='\t', index=False)
negative = pd.read_csv("data/tagg/labeling/negative-excel-complete.tsv", delimiter = "\t",quoting = 3)

"""
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
----------------------------------------------------------------------------------------
"""
client = MongoClient('localhost', 27017) # Conecting database
db = client.accident # Created instance of database


negative_tagenta = pd.read_csv("data/tagg/labeling/negative-tagenta.tsv",delimiter="\t",quoting=3)

negative_tagenta["created_at"] = ""
negative_tagenta["user_name"] = ""

for index, row in negative_tagenta.iterrows():   
    cursor = db.complete.find({'id_tweet':str(row['id_tweet'])}, no_cursor_timeout=True)
    tweet = list(cursor)
    negative_tagenta.at[index,'created_at'] = tweet[0]['created_at']
    negative_tagenta.at[index,'user_name'] = tweet[0]['user_name']
    if index%1000==0:
        print(datetime.datetime.now())
        print(index)
    

negative_tagenta.to_csv("data/tagg/labeling/negative-tagenta-complete.tsv",sep='\t', index=False)
negative = pd.read_csv("data/tagg/labeling/negative-tagenta-complete.tsv", delimiter = "\t",quoting = 3)