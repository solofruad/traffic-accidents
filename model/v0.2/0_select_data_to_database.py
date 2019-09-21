#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 10:38:17 2019

@author: hat
"""

import pandas as pd  # For data handling
import re


"""
Search (Keywords & bogotá) 1_search_shuffle
"""
def selectData(filename,opt,query):
    data = pd.read_csv("data/v0/"+filename, delimiter = "\t", quoting = 3)
    data = data[['id_tweet','text','created_at', 'user_name']]
    
    #Seleccionar la muestra
    if opt==1:
        data = data.reset_index(drop=True)
        data = data.iloc[15000:87772]
        data = data.reset_index(drop=True)
    
    data = data[~((data['user_name'] == 'BogotaTransito') | (data['user_name'] =='rutassitp') | (data['user_name'] =='WazeTrafficBOG') | (data['user_name'] =='sitpbogota'))]
    
    data = data[data['text'].str.contains(query)]

    data = data.drop_duplicates(['id_tweet'],keep='first')
    data = data.drop_duplicates(['text'],keep='first')

    data = removeRepeatText(data)

    return data

def removeRepeatText(data):
    data['text_secundary'] = ''
    data = data.reset_index(drop=True) # if limited the amount tweets drop index so that it does not interfere later in te for_each 
    
    corpus = [] # Array with clenased tweets 
    tweets = data["text"]
    for i in range(0,len(data)):       
        review = tweets[i]    
        
        # Clean tweets of links, username mentions, emoticons, others specials characters, numbers, split Hashtags
        review = re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",' ', review)
    
        # Changes tweets to lowercase
        review = review.lower()
        
        review = review.split()    
            
        review = ' '.join(review) #Concatenate all in one text
        # First eliminate the stopwords, then apply the SnowballStemmer    
        # Add each tweet to array
        corpus.append(review)    
    
    data["text_secundary"] = corpus
    
    data = data[data["text_secundary"].str.split().apply(len) > 3]
    
    data = data.drop_duplicates(['text_secundary'],keep='first')
    
    return data



query ="accidente|incidente|choque|incidente vial|atropell*|tránsito|transito|trafico|tráfico"

search = selectData('1_search_shuffle.tsv',1,query)

opt = 0

timeline = selectData('2_search_timeline_user.tsv',opt,query)
follow = selectData('3_stream_follow_user.tsv',opt,query)
bogota = selectData('4_stream_bogota.tsv',opt,query)


query ="accidente"
track_spanish = selectData('5_dataset-track-filter.tsv',opt,query)


dataset = pd.concat([search,timeline,follow,bogota,track_spanish])
dataset = dataset.drop_duplicates(['id_tweet'],keep='first')

dataset = dataset.drop_duplicates(['text'],keep='first')

dataset = dataset[['id_tweet','text','created_at']]
dataset['source'] = 'twitter'
dataset['complete'] = 0
dataset = dataset.rename(columns={'id_tweet':'id_source'})
dataset['id_source'] = dataset['id_source'].astype(str)
dataset.to_json("data/dataset_to_database.json",force_ascii=False, orient='records')



"""
    #TRAER TODOS LOS DATOS Y PASARLOS A LA BASE DE DATOS
"""
search = pd.read_csv("data/v0/1_search.tsv", delimiter = "\t", quoting = 3)
search = search[['id_tweet','text','created_at', 'user_name']]


timeline = pd.read_csv("data/v0/2_search_timeline_user.tsv", delimiter = "\t", quoting = 3)
timeline = timeline[['id_tweet','text','created_at', 'user_name']]

follow = pd.read_csv("data/v0/3_stream_follow_user.tsv", delimiter = "\t", quoting = 3)
follow = follow[['id_tweet','text','created_at', 'user_name']]

bogota = pd.read_csv("data/v0/4_stream_bogota.tsv", delimiter = "\t", quoting = 3)
bogota = bogota[['id_tweet','text','created_at', 'user_name']]

track_spanish = pd.read_csv("data/v0/5_dataset-track-filter.tsv", delimiter = "\t", quoting = 3)
track_spanish = track_spanish[['id_tweet','text','created_at', 'user_name']]

dataset = pd.concat([search,timeline,follow,bogota,track_spanish])
dataset = dataset.drop_duplicates(['id_tweet'],keep='first')
dataset['id_tweet'] = dataset['id_tweet'].astype(str)
dataset.to_json("data/dataset_to_database_complete.json",force_ascii=False, orient='records')
