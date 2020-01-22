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

#client = MongoClient('localhost', 27017) # Conecting database
#db = client.dataset # Created instance of database

NAME = 'bogota'
MONTH = "julio"
start = datetime(2019, 7, 1, 0, 0, 0)
end = datetime(2019, 8, 1, 0, 0, 0)
collection_size = 409580
#collection = db.server_bogota
#start = end = 0

DIR_SAVE = "data/database/server_bogota/"+MONTH+"/"
NAME_EXPORT = "data/database/server_bogota_"+MONTH+".tsv"

token_user = DatabaseToCSV()
token_user.config_collection(collection_name=NAME,
                             dir_save=DIR_SAVE,
                             host='localhost', port=27017)

n_cores = multiprocessing.cpu_count()
#collection_size = collection.count_documents({ 'created_at': {'$gte': start, '$lt': end}  })

batch_size = round(collection_size/n_cores+0.5)
skips = range(0, n_cores*batch_size, batch_size)

#token_user.build_df(start, end)

processes = [ multiprocessing.Process(target=token_user.build_df, args=(start, end,skip_n,batch_size,100000)) for skip_n in skips]

for process in processes:    
    process.start()

for process in processes:    
    process.join()

#dataset = pd.read_csv("example.tsv", delimiter = "\t", quoting = 3)

dataset = pd.read_csv("data/database/template.tsv", delimiter = "\t", quoting = 3)
for skip in skips:
    dataset = pd.concat([dataset,pd.read_csv(DIR_SAVE+str(skip)+".tsv", delimiter = "\t", quoting = 3)])
    
#dataset = dataset.drop_duplicates(['id_tweet'],keep='first')
dataset.sort_values('created_at').to_csv(NAME_EXPORT,sep='\t',index=False)
#data = pd.read_csv(NAME_EXPORT, delimiter = "\t", quoting = 3)

octubre = pd.read_csv("data/database/server_bogota/server_bogota_octubre.tsv", delimiter = "\t", quoting = 3)
noviembre = pd.read_csv("data/database/server_bogota/server_bogota_noviembre.tsv", delimiter = "\t", quoting = 3)
diciembre = pd.read_csv("data/database/server_bogota/server_bogota_diciembre.tsv", delimiter = "\t", quoting = 3)
enero = pd.read_csv("data/database/server_bogota/server_bogota_enero.tsv", delimiter = "\t", quoting = 3)
febrero = pd.read_csv("data/database/server_bogota/server_bogota_febrero.tsv", delimiter = "\t", quoting = 3)
marzo = pd.read_csv("data/database/server_bogota/server_bogota_marzo.tsv", delimiter = "\t", quoting = 3)
abril = pd.read_csv("data/database/server_bogota/server_bogota_abril.tsv", delimiter = "\t", quoting = 3)
mayo = pd.read_csv("data/database/server_bogota/server_bogota_mayo.tsv", delimiter = "\t", quoting = 3)
junio = pd.read_csv("data/database/server_bogota/server_bogota_junio.tsv", delimiter = "\t", quoting = 3)
julio = pd.read_csv("data/database/server_bogota/server_bogota_julio.tsv", delimiter = "\t", quoting = 3)

dataset = pd.concat([octubre, noviembre, diciembre, enero, febrero, marzo, abril, mayo, junio, julio])
dataset.sort_values('created_at').to_csv("data/database/server_bogota.tsv",sep='\t',index=False)

dataset = pd.read_csv("data/database/server_bogota.tsv", delimiter = "\t", quoting = 3)

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


"""
|------------------------------------------------------------------------------------------------------------------------|
|--------------------------------------------SERVER_TOKEN_KEYWORDS-------------------------------------------------------|
|--------------------------------------------SERVER_TOKEN_KEYWORDS-------------------------------------------------------|
|--------------------------------------------SERVER_TOKEN_KEYWORDS-------------------------------------------------------|
|--------------------------------------------SERVER_TOKEN_KEYWORDS-------------------------------------------------------|
|--------------------------------------------SERVER_TOKEN_KEYWORDS-------------------------------------------------------|
"""

import pandas as pd
import multiprocessing

from pymongo import MongoClient
from datetime import datetime
from classes.parallel.DatabaseToCSV import DatabaseToCSV
#from classes.DatabaseToCSV import DatabaseToCSV as DBToCSV

#client = MongoClient('localhost', 27017) # Conecting database
#db = client.dataset # Created instance of database

NAME = 'stream_keywords_julio'
MONTH = "julio"
RANGE = "29_to_31"
start = datetime(2019, 7, 29, 0, 0, 0)
end = datetime(2019, 7, 31, 0, 0, 0)
collection_size = 355923

#collection = db.server_bogota
#start = end = 0

DIR_SAVE = "data/database/server_token_keywords/"+MONTH+"/batch/"+RANGE+"_"
NAME_EXPORT = "data/database/server_token_keywords/"+MONTH+"/"+"server_token_keywords_"+MONTH+"_"+RANGE+".tsv"

token_user = DatabaseToCSV()
token_user.config_collection(collection_name=NAME,
                             dir_save=DIR_SAVE,
                             host='localhost', port=27017)

n_cores = multiprocessing.cpu_count()
#collection_size = collection.count_documents({ 'created_at': {'$gte': start, '$lt': end}  })

batch_size = round(collection_size/n_cores+0.5)
skips = range(0, n_cores*batch_size, batch_size)

#token_user.build_df(start, end)

processes = [ multiprocessing.Process(target=token_user.build_df, args=(start, end,skip_n,batch_size,100000)) for skip_n in skips]

for process in processes:    
    process.start()

for process in processes:    
    process.join()

#dataset = pd.read_csv("example.tsv", delimiter = "\t", quoting = 3)

dataset = pd.read_csv("data/database/template.tsv", delimiter = "\t", quoting = 3)
for skip in skips:
    dataset = pd.concat([dataset,pd.read_csv(DIR_SAVE+str(skip)+".tsv", delimiter = "\t", quoting = 3)])

print(RANGE)
print(dataset.iloc[0][4])
print(dataset.iloc[-1][4])
print(collection_size == len(dataset))
#dataset = dataset.drop_duplicates(['id_tweet'],keep='first')
dataset.sort_values('created_at').to_csv(NAME_EXPORT,sep='\t',index=False)
#data = pd.read_csv(NAME_EXPORT, delimiter = "\t", quoting = 3)


noviembre = pd.read_csv("data/database/server_token_keywords/noviembre/server_token_keywords_noviembre_19_to_20.tsv", delimiter = "\t", quoting = 3)
noviembre = pd.read_csv("data/database/server_bogota/server_bogota_noviembre.tsv", delimiter = "\t", quoting = 3)
diciembre = pd.read_csv("data/database/server_bogota/server_bogota_diciembre.tsv", delimiter = "\t", quoting = 3)
enero = pd.read_csv("data/database/server_bogota/server_bogota_enero.tsv", delimiter = "\t", quoting = 3)
febrero = pd.read_csv("data/database/server_bogota/server_bogota_febrero.tsv", delimiter = "\t", quoting = 3)
marzo = pd.read_csv("data/database/server_bogota/server_bogota_marzo.tsv", delimiter = "\t", quoting = 3)
abril = pd.read_csv("data/database/server_bogota/server_bogota_abril.tsv", delimiter = "\t", quoting = 3)
mayo = pd.read_csv("data/database/server_bogota/server_bogota_mayo.tsv", delimiter = "\t", quoting = 3)
junio = pd.read_csv("data/database/server_bogota/server_bogota_junio.tsv", delimiter = "\t", quoting = 3)
julio = pd.read_csv("data/database/server_bogota/server_bogota_julio.tsv", delimiter = "\t", quoting = 3)

dataset = pd.concat([octubre, noviembre, diciembre, enero, febrero, marzo, abril, mayo, junio, julio])
dataset.sort_values('created_at').to_csv("data/database/server_bogota.tsv",sep='\t',index=False)

dataset = pd.read_csv("data/database/server_bogota.tsv", delimiter = "\t", quoting = 3)



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


