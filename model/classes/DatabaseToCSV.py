#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  8 16:39:16 2019

@author: hat
"""

import pandas as pd
from datetime import timedelta
import re

class DatabaseToCSV:
    def __init__(self):        
        self.df = pd.DataFrame()
        self.dir_save = ''

    def get_cursor(self,collection, start, end):    
        if start == 0 and end == 0:
            cursor = collection.find({}, no_cursor_timeout=True)
            print("No date")
        else:
            cursor = collection.find({ 'created_at': {'$gte': start, '$lt': end}  }, no_cursor_timeout=True)        
            print("Yes date")
        return cursor
    
    def build_df(self, collection, start, end):
        cursor = self.get_cursor(collection, start,end)
        self.df = pd.DataFrame(list(cursor))    
        
    def config_collection(self,dir_save):        
        self.dir_save = dir_save        
    
    
    def first_preprocessing(self,loader=0):    
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
        filename = self.dir_save + str(threadId)+".tsv"
        self.df_to_csv(filename)
                    
    
    def df_to_csv(self,filename):
        #filename = "data/database/server_token_user.tsv"
        self.df.sort_values('created_at').to_csv(filename,sep='\t',index=False)
            