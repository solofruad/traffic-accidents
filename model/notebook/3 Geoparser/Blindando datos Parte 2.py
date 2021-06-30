#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 17:02:46 2021

@author: hat
"""

import pandas as pd

#dir_ = "../../data/database/output_ml/M1/NER_extractor/"
dir_ = "../../data/database/output_ml/M1/NER_extractor/data_shielded_experiment/"
#file = 'accident_tweets_lat_lon_geocord_bogota_unique.tsv'
file = 'accident_tweets_unique.tsv'
dataset = pd.read_csv(dir_+file, delimiter = "\t", quoting = 3)

#### Filtrar por palabras claves
result = dataset[
        (dataset['clean'].str.contains("incidente", case=False)) |
        (dataset['clean'].str.contains("accident", case=False)) |
        (dataset['clean'].str.contains("choque", case=False)) |
        (dataset['clean'].str.contains("choc", case=False)) |
        (dataset['clean'].str.contains("atropell", case=False)) |
        (dataset['clean'].str.contains("arroll", case=False)) |
        (dataset['clean'].str.contains("siniestro", case=False)) |
        (dataset['clean'].str.contains("fallec", case=False)) |
        (dataset['clean'].str.contains("volca", case=False)) |
        (dataset['clean'].str.contains("colis", case=False)) 
    ]

#### Eliminar tweets RT de estos usuarios
result = result[result['text'].str.startswith('RT @BogotaTransito') == False]
result = result[result['text'].str.startswith('RT @Citytv') == False]
result = result[result['text'].str.startswith('RT @RedapBogota') == False]
result = result[result['text'].str.startswith('RT @rutassitp') == False]
result = result[result['text'].str.startswith('RT @SectorMovilidad') == False]

#### Los tweets de rutasstip son los mismos que @BogotaTransito, incluso con desfase de hasta 7 horas
##### Se eliminar estos tweets
result = result[(result['user_name'] != 'rutassitp')]

#### Aunque con eliminar RT nikolai desaparece, sin embargo se eliminan los tweets de este spambot.
result = result[result['user_name'].str.contains("nikolai", case=False) == False]

count_tweet_by_username = result['user_name'].value_counts() # Show distribution of tweets by user
count_tweet_by_username[0:40]

result.to_csv(dir_+"accident_tweets_unique_keywords.tsv",sep='\t',index=False)
