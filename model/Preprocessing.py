#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 23:14:50 2019

@author: hat
"""

import pandas as pd  # For data handling

import spacy  # For preprocessing
import re
import multiprocessing


CORES = multiprocessing.cpu_count() # Count the number of cores in a computer

def cleaning(doc):    
    txt = [token.lemma_ for token in doc if not token.is_stop]    
    if len(txt) > 2:
        return ' '.join(txt)

#######################################PARTE 1#####################################################

"""-------------------------------DATASETS-----------------------------------------------"""


positive = pd.read_csv("data/ok_positive.tsv", delimiter = "\t", quoting = 3)
positive = positive[['id_tweet','created_at','user_name','text']]

negative = pd.read_csv("data/ok_negative.tsv", delimiter = "\t", quoting = 3)
negative = negative[['id_tweet','created_at','user_name','text']]

"""-------------------------------LIMPIEZA-----------------------------------------------"""

#dataset = pd.read_csv("data/clean/"+FNAME, delimiter = "\t", quoting = 3)
#del dataset["Unnamed: 0"]

nlp = spacy.load("es_core_news_md",disabled=['ner','parser']) # disabling Named Entity Recognition for speed
nlp.vocab["rt"].is_stop = True #Add RT to Stopwords

brief_cleaning_p = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in positive['text'])

brief_cleaning_n = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in negative['text'])


txt_p = [cleaning(doc) for doc in nlp.pipe(brief_cleaning_p, batch_size=50, n_threads=CORES)]
positive['clean'] = txt_p
positive = positive[~positive['clean'].isnull()] #Elimina publicaciones que estan null al eliminarlo porque no generan valor en el proceso de limpieza
positive = positive.reset_index(drop=True) # if limited the amount tweets drop index so that it does not interfere later in te for_each 
positive.to_csv("data/clean/positive_clean.tsv",sep='\t')


txt_n = [cleaning(doc) for doc in nlp.pipe(brief_cleaning_n, batch_size=50, n_threads=CORES)]
negative['clean'] = txt_n
negative = negative[~negative['clean'].isnull()] #Elimina publicaciones que estan null al eliminarlo porque no generan valor en el proceso de limpieza
negative = negative.reset_index(drop=True) # if limited the amount tweets drop index so that it does not interfere later in te for_each 
negative.to_csv("data/clean/negative_clean.tsv",sep='\t')


"""-------------------------------UNION DATASET-----------------------------------------------"""

negative["label"] = 0
positive["label"] = 1

negative_def = negative.sample(n=2004)

dataset = pd.concat([positive,negative_def])
dataset.to_csv("data/dataset_accident_tweet.tsv",sep='\t')
