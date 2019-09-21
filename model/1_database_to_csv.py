#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Dec 12 12:27:28 2018

@author: Néstor Suat-Rojas
"""

############################################################
# Import dataset from database

"""
    Objective: Connect to the mongo database and return the data of some table
"""

# Libreries
#import numpy as np
import pandas as pd
import multiprocessing

from pymongo import MongoClient
from datetime import datetime
from classes.parallel.DatabaseToCSV import DatabaseToCSV
from classes.DatabaseToCSV import DatabaseToCSV as DBToCSV

client = MongoClient('localhost', 27017) # Conecting database
db = client.dataset # Created instance of database

"""
|------------------------------------------------------------------------------------------------------------------------|
|-----------------------------------------------SERVER_TOKEN_USER--------------------------------------------------------|
|-----------------------------------------------SERVER_TOKEN_USER--------------------------------------------------------|
|-----------------------------------------------SERVER_TOKEN_USER--------------------------------------------------------|
|-----------------------------------------------SERVER_TOKEN_USER--------------------------------------------------------|
|------------------------------------------------------------------------------------------------------------------------|
"""
NAME = 'search_user'
DIR_SAVE = "data/database/server_token_user/"
NAME_EXPORT = "data/database/server_token_user.tsv"
collection = db.server_token_user

start = end = 0
token_user = DatabaseToCSV()
token_user.config_collection(collection_name=NAME,
                             dir_save=DIR_SAVE,
                             host='localhost', port=27017)


n_cores = multiprocessing.cpu_count()
collection_size = collection.count_documents({})
batch_size = round(collection_size/n_cores+0.5)
skips = range(0, n_cores*batch_size, batch_size)

#token_user.build_df(start, end)

processes = [ multiprocessing.Process(target=token_user.build_df, args=(collection, start, end,skip_n,batch_size,100000)) for skip_n in skips]


for process in processes:
    process.start()

for process in processes:
    process.join()
    
dataset = pd.read_csv("data/database/template.tsv", delimiter = "\t", quoting = 3)
for skip in skips:
    dataset = pd.concat([dataset,pd.read_csv(DIR_SAVE+str(skip)+".tsv", delimiter = "\t", quoting = 3)])
    
#dataset = dataset.drop_duplicates(['id_tweet'],keep='first')
dataset.sort_values('created_at').to_csv(NAME_EXPORT,sep='\t',index=False)
#data = pd.read_csv(NAME_EXPORT, delimiter = "\t", quoting = 3)

"""
|------------------------------------------------------------------------------------------------------------------------|
|-----------------------------------------------SERVER_TOKEN_SEARCH------------------------------------------------------|
|-----------------------------------------------SERVER_TOKEN_SEARCH------------------------------------------------------|
|-----------------------------------------------SERVER_TOKEN_SEARCH------------------------------------------------------|
|-----------------------------------------------SERVER_TOKEN_SEARCH------------------------------------------------------|
|------------------------------------------------------------------------------------------------------------------------|
"""


collection = db.server_token_search

start = end = 0
token_user = DatabaseToCSV()
token_user.config_collection(collection_name='search',
                             dir_save="data/database/server_token_search/",
                             host='localhost', port=27017)


n_cores = multiprocessing.cpu_count()
collection_size = collection.count_documents({})
batch_size = round(collection_size/n_cores+0.5)
skips = range(0, n_cores*batch_size, batch_size)

#token_user.build_df(start, end)

processes = [ multiprocessing.Process(target=token_user.build_df, args=(collection, start, end,skip_n,batch_size)) for skip_n in skips]

for process in processes:
    process.start()

for process in processes:
    process.join()
  
dataset_1 = pd.read_csv("data/database/server_token_search/0.tsv", delimiter = "\t", quoting = 3)
dataset_2 = pd.read_csv("data/database/server_token_search/67789.tsv", delimiter = "\t", quoting = 3)
dataset_3 = pd.read_csv("data/database/server_token_search/135578.tsv", delimiter = "\t", quoting = 3)
dataset_4 = pd.read_csv("data/database/server_token_search/203367.tsv", delimiter = "\t", quoting = 3)
dataset_union = pd.concat([dataset_1, dataset_2, dataset_3,dataset_4])    
dataset_union = dataset_union.drop_duplicates(['id_tweet'],keep='first')
dataset_union.sort_values('created_at').to_csv("data/database/server_token_search.tsv",sep='\t',index=False)
data = pd.read_csv("data/database/server_token_search.tsv", delimiter = "\t", quoting = 3)


"""
|------------------------------------------------------------------------------------------------------------------------|
|---------------------------------------SERVER_FOLLOW_TIMELINE_USER------------------------------------------------------|
|---------------------------------------SERVER_FOLLOW_TIMELINE_USER------------------------------------------------------|
|---------------------------------------SERVER_FOLLOW_TIMELINE_USER------------------------------------------------------|
|---------------------------------------SERVER_FOLLOW_TIMELINE_USER------------------------------------------------------|
|------------------------------------------------------------------------------------------------------------------------|
"""

NAME = 'timeline_user'
DIR_SAVE = "data/database/server_follow_timeline_user/"
NAME_EXPORT = "data/database/server_follow_timeline_user.tsv"
collection = db.server_follow_timeline_user

start = end = 0
token_user = DatabaseToCSV()
token_user.config_collection(collection_name=NAME,
                             dir_save=DIR_SAVE,
                             host='localhost', port=27017)


n_cores = multiprocessing.cpu_count()
collection_size = collection.count_documents({})
batch_size = round(collection_size/n_cores+0.5)
skips = range(0, n_cores*batch_size, batch_size)

#token_user.build_df(start, end)

processes = [ multiprocessing.Process(target=token_user.build_df, args=(collection, start, end,skip_n,batch_size,100000)) for skip_n in skips]

for process in processes:
    process.start()

for process in processes:
    process.join()

dataset = pd.read_csv("data/database/template.tsv", delimiter = "\t", quoting = 3)
for skip in skips:
    dataset = pd.concat([dataset,pd.read_csv(DIR_SAVE+str(skip)+".tsv", delimiter = "\t", quoting = 3)])
    
#dataset = dataset.drop_duplicates(['id_tweet'],keep='first')
dataset.sort_values('created_at').to_csv(NAME_EXPORT,sep='\t',index=False)
#data = pd.read_csv(NAME_EXPORT, delimiter = "\t", quoting = 3)




"""
|------------------------------------------------------------------------------------------------------------------------|
|------------------------------------------------SERVER_BOGOTA-----------------------------------------------------------|
|------------------------------------------------SERVER_BOGOTA-----------------------------------------------------------|
|------------------------------------------------SERVER_BOGOTA-----------------------------------------------------------|
|------------------------------------------------SERVER_BOGOTA-----------------------------------------------------------|
|------------------------------------------------------------------------------------------------------------------------|
"""

import pandas as pd
import multiprocessing

from pymongo import MongoClient
from datetime import datetime
from classes.parallel.DatabaseToCSV import DatabaseToCSV
#from classes.DatabaseToCSV import DatabaseToCSV as DBToCSV

client = MongoClient('localhost', 27017) # Conecting database
db = client.dataset # Created instance of database

NAME = 'bogota'
MONTH = "noviembre/"
DIR_SAVE = "data/database/server_bogota/"+MONTH
#NAME_EXPORT = "data/database/server_bogota.tsv"
collection = db.server_bogota

#start = end = 0
token_user = DatabaseToCSV()
token_user.config_collection(collection_name=NAME,
                             dir_save=DIR_SAVE,
                             host='localhost', port=27017)

start = datetime(2018, 10, 1, 0, 0, 0)
end = datetime(2018, 11, 1, 0, 0, 0)

n_cores = multiprocessing.cpu_count()
#collection_size = collection.count_documents({ 'created_at': {'$gte': start, '$lt': end}  })
collection_size = 403656
batch_size = round(collection_size/n_cores+0.5)
skips = range(0, n_cores*batch_size, batch_size)

#token_user.build_df(start, end)

processes = [ multiprocessing.Process(target=token_user.build_df_iter, args=(collection, start, end,skip_n,batch_size,10000)) for skip_n in skips]

for process in processes:    
    process.start()

for process in processes:    
    process.join()

dataset = pd.read_csv("example.tsv", delimiter = "\t", quoting = 3)

dataset = pd.read_csv("data/database/template.tsv", delimiter = "\t", quoting = 3)
for skip in skips:
    dataset = pd.concat([dataset,pd.read_csv(DIR_SAVE+str(skip)+".tsv", delimiter = "\t", quoting = 3)])
    
#dataset = dataset.drop_duplicates(['id_tweet'],keep='first')
dataset.sort_values('created_at').to_csv(NAME_EXPORT,sep='\t',index=False)
#data = pd.read_csv(NAME_EXPORT, delimiter = "\t", quoting = 3)




"""
|------------------------------------------------------------------------------------------------------------------------|
|------------------------------------------------SERVER_BOGOTA-----------------------------------------------------------|
|------------------------------------------------SERVER_BOGOTA-----------------------------------------------------------|
|------------------------------------------------SERVER_BOGOTA-----------------------------------------------------------|
|------------------------------------------------SERVER_BOGOTA-----------------------------------------------------------|
|------------------------------------------------------------------------------------------------------------------------|
"""
from classes.DatabaseToCSV import DatabaseToCSV as DBToCSV

NAME = 'bogota'
MONTH = "noviembre/"
DIR_SAVE = "data/database/server_bogota/"+MONTH
NAME_EXPORT = "data/database/server_bogota.tsv"
collection = db.server_bogota

#start = end = 0
token_user = DBToCSV()
token_user.config_collection(dir_save=DIR_SAVE)

start = datetime(2018, 11, 1, 0, 0, 0)
end = datetime(2018, 12, 1, 0, 0, 0)

n_cores = multiprocessing.cpu_count()
#collection_size = collection.count_documents({})
collection_size = 403656
batch_size = round(collection_size/n_cores+0.5)
iterations = range(0, n_cores)

token_user.build_df(collection, start, end)
processes = [ multiprocessing.Process(target=token_user.first_preprocessing_paralleling, args=(batch_size,threadId,collection_size,10000)) for threadId in iterations]


for process in processes:    
    process.start()

for process in processes:    
    process.join()

dataset = pd.read_csv("data/database/template.tsv", delimiter = "\t", quoting = 3)
for skip in skips:
    dataset = pd.concat([dataset,pd.read_csv(DIR_SAVE+str(skip)+".tsv", delimiter = "\t", quoting = 3)])
    
#dataset = dataset.drop_duplicates(['id_tweet'],keep='first')
dataset.sort_values('created_at').to_csv(NAME_EXPORT,sep='\t',index=False)
#data = pd.read_csv(NAME_EXPORT, delimiter = "\t", quoting = 3)





for process in range(0,4):    
    processes[process].start()

for process in range(0,4):
    processes[process].join()


for process in range(4,8):    
    processes[process].start()

for process in range(4,8):
    processes[process].join()


n_cores = multiprocessing.cpu_count()
collection_size = collection.count_documents({})
batch_size = round(collection_size/n_cores+0.5)
iterations = range(0, n_cores)

processes = [ multiprocessing.Process(target=token_user.first_preprocessing_paralleling, args=(batch_size,threadId,collection_size,10000)) for threadId in iterations]


for process in processes:
    process.start()

for process in processes:
    process.join()

import threading

threads = [ threading.Thread(target=token_user.first_preprocessing_paralleling, args=(batch_size,threadId,collection_size,10000)) for threadId in iterations]


for thread in threads:
    thread.start()

for thread in threads:
    thread.join()


token_user.first_preprocessing(loader=10000)
"""
##https://stackoverflow.com/questions/44073393/parallelizing-loading-data-from-mongodb-into-python




filename = "data/database/server_token_user.tsv"
token_user.df_to_csv(filename)

len(token_user.df)
df = pd.read_csv(filename, delimiter = "\t", quoting = 3)



""" SERVER_TOKEN_SEARCH """
collection = db.server_token_search
start = datetime(2018, 10, 1, 5, 0, 0)
end = datetime(2019, 8, 1, 5, 0, 0)

token_user = DatabaseToCSV()
token_user.build_df(collection, start, end)
token_user.first_preprocessing()
filename = "data/database/server_token_user.tsv"
token_user.df_to_csv(filename)

len(token_user.df)
df = pd.read_csv(filename, delimiter = "\t", quoting = 3)







start = datetime(2018, 10, 26, 5, 0, 0)
end = datetime(2018, 10, 28, 5, 0, 0)


# Save dataset in file
#columns = ["id_tweet", "text", "created_at", "user_name"]
#df = pd.DataFrame(dataset, columns=columns)
        
filename = "stream_track_dic_25_31.tsv"
df.sort_values('created_at').to_csv(filename,sep='\t')

#test
dataset_1 = pd.read_csv(filename, delimiter = "\t", quoting = 3)

dataset_1 = pd.read_csv("stream_bogota-oct.tsv", delimiter = "\t", quoting = 3)
dataset_2 = pd.read_csv("stream_bogota-nov.tsv", delimiter = "\t", quoting = 3)
dataset_3 = pd.read_csv("stream_bogota-dic.tsv", delimiter = "\t", quoting = 3)

dataset_union = pd.concat([dataset_1, dataset_2, dataset_3])    
dataset_union.to_csv("stream_bogota.tsv",sep='\t')


