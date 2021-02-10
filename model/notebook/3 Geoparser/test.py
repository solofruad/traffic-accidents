#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  7 11:00:55 2021

@author: hat
"""
from ast import literal_eval
import pandas as pd
import sys
sys.path.insert(0, '../../')

from classes.tweet2accident.enviroments import Global

## Variables para importar modelos y demás
dir_ = "../../data/v1/NER/"

file = 'ner_dataset_geocoding.tsv' # Dataset

api_key = Global()

## Importando Dataset
dataset = pd.read_csv(dir_+file, delimiter = "\t", quoting = 3)
dataset.entities = dataset.entities.apply(literal_eval)
dataset = dataset[dataset['location'] != 'Ningún resultado encontrado']
dataset.location = dataset.location.apply(literal_eval)
del dataset['Unnamed: 0']

dataset = dataset[['id_tweet','text','created_at','entities','location']]

dataset['gmap'] = dataset['location']
del dataset['location']

id_tweets_bad = ['1011937096179896320','1058331896298520576','1060077229043052545','1060683217383182338',
                 '1066203076254679040','1074991662848446464','1092759433795522560','1099689733956034561',
                 '1099717090376728577','1125722482059763713','1131707280767033344','1147555712521908225',
                 '1149638960328478721','761823976700121088','770763722210045956','873824438684311552',        
             ]

id_tweets_ok = ['1010197757360001025','1021753857746116609','1047450565284958210','1050724915425566720',
                '1050208800685400064','1059258607672410118','1059771773003223040','1066228060381503490',
                '1076644756803993601','1083002766476394496','1096749778036240386','1102902768514359296',
                '1139518874150494208','1141675891917041664','1142074258413301761','970736094978433025',                
                ]


def select_rows_bad(id_tweet):
    if id_tweet in id_tweets_bad:
        return True
    else:
        return False
    
def select_rows_ok(id_tweet):
    if id_tweet in id_tweets_ok:
        return True
    else:
        return False
    
tweets_bad = dataset[dataset['id_tweet'].apply(select_rows_bad)]
tweets_ok = dataset[dataset['id_tweet'].apply(select_rows_ok)]


tweets_ok.to_csv(dir_+"ner_dataset_test_ok.tsv",sep='\t')
tweets_bad.to_csv(dir_+"ner_dataset_test_bad.tsv",sep='\t')
