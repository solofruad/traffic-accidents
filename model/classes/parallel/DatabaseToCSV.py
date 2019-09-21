#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:39:16 2019

@author: hat
"""

import pandas as pd
from datetime import timedelta
from pymongo import MongoClient
import re

class DatabaseToCSV: #Paralleling Process
    def __init__(self):        
        self.df = pd.DataFrame()     
        self.dir_save = ''
        self.database = {
                'host': 'localhost',
                'port': 27017
        }
        self.collection_name = ''        

    def get_cursor(self, collection, start, end, skip_n, limit_n):   
        if start == 0 and end == 0:
            cursor = collection.find({}, no_cursor_timeout=True).skip(skip_n).limit(limit_n)            
        else:
            cursor = collection.find({ 'created_at': {'$gte': start, '$lt': end}  }, no_cursor_timeout=True).skip(skip_n).limit(limit_n)            
        return cursor
    
    def build_df(self,collection, start, end, skip_n, limit_n,loader=0):
        collection = self.get_collection()        
        cursor = self.get_cursor(collection, start,end, skip_n, limit_n)    
        self.df = pd.DataFrame(list(cursor))        
        self.first_preprocessing(skip_n=skip_n,loader=loader)
    
    
    def build_df_iter(self,collection, start, end, skip_n, limit_n,loader=0):
        collection = self.get_collection()
        
        cursor = self.get_cursor(collection, start,end, skip_n, limit_n)
        output = pd.DataFrame()
        cont = 0
        for doc in cursor:                               
            output = output.append(self.first_preprocessing_iter(doc), ignore_index=True)
            if loader:
                if cont % loader == 0:
                    print(cont)
            cont += 1
        cont = 0
        self.df = output
        self.df.sort_values('created_at').to_csv("example.tsv",sep='\t',index=False)
        filename = self.dir_save + str(skip_n)+".tsv"
        self.df_to_csv(filename)        
        
    def get_collection(self):
        client = MongoClient(self.database['host'], self.database['port']) # Conecting database
        db = client.dataset # Created instance of database
        if self.collection_name == 'search_user':
            collection = db.server_token_user
        elif self.collection_name == 'search':
            collection = db.server_token_search
        elif self.collection_name == 'bogota':
            collection = db.server_bogota
        elif self.collection_name == 'timeline_user':
            collection = db.server_follow_timeline_user
        elif self.collection_name == 'stream_keywords':
            collection = db.server_token_keywords
        else:
            collection = None
        return collection
    
    def config_collection(self,collection_name,dir_save,host,port):
        self.collection_name = collection_name
        self.dir_save = dir_save
        self.database['host'] = host
        self.database['port'] = port
    
    def first_preprocessing_iter(self, doc):
        date = doc['created_at'] - timedelta(hours=5)
        doc['created_at'] = date.strftime("%Y-%m-%d %H:%M:%S")
        doc['text'] = re.sub("[\t\n\r]",'',doc['text'])
        doc['place_name'] = re.sub("[\t\n\r]",'',doc['place_name'])
        if doc['user_location'] != None :
            doc['user_location'] = re.sub("[\t\n\r]",'',doc['user_location'])     
        return doc
        
    
    def first_preprocessing(self,skip_n, loader=0):    
        for i in range(0,len(self.df)):
            date = self.df.iloc[i]['created_at'] - timedelta(hours=5)
            self.df.at[i,'created_at'] = date.strftime("%Y-%m-%d %H:%M:%S")
            self.df.at[i, 'text'] = re.sub("[\t\n\r]",'',self.df.iloc[i]['text'])
            self.df.at[i, 'place_name'] = re.sub("[\t\n\r]",'',self.df.iloc[i]['place_name'])
        
            if self.df.iloc[i]['user_location'] != None :
                self.df.at[i, 'user_location'] = re.sub("[\t\n\r]",'',self.df.iloc[i]['user_location'])
            
            #i = i +1 # This is only visualize the progress
            if loader:
                if i%loader == 0:
                    print(i)                
        filename = self.dir_save + str(skip_n)+".tsv"
        self.df_to_csv(filename)
    
    def first_preprocessing_paralleling(self,batch_size,threadId,collection_size,loader=0):    
        init = batch_size * threadId
        end = init + (batch_size)
        end = end if end <= collection_size else collection_size
        for i in range(init,end):
            date = self.df.iloc[i]['created_at'] - timedelta(hours=5)
            self.df.at[i,'created_at'] = date.strftime("%Y-%m-%d %H:%M:%S")
            self.df.at[i, 'text'] = re.sub("[\t\n\r]",'',self.df.iloc[i]['text'])
            self.df.at[i, 'place_name'] = re.sub("[\t\n\r]",'',self.df.iloc[i]['place_name'])
        
            if self.df.iloc[i]['user_location'] != None :
                self.df.at[i, 'user_location'] = re.sub("[\t\n\r]",'',self.df.iloc[i]['user_location'])
            
            #i = i +1 # This is only visualize the progress
            if loader:
                if i%loader == 0:
                    print("%s : thread [%s]" %(i,threadId))    
                    
    
    def df_to_csv(self,filename):
        #filename = "data/database/server_token_user.tsv"
        self.df.sort_values('created_at').to_csv(filename,sep='\t',index=False)
            