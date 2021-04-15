#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar 29 18:34:00 2021

@author: hat

@description:
    Uniendo los resultados del geocoding de batch geocoding, como anteriormente tocó dividirlos por meses
    y cada mil muestras
"""

import pandas as pd
import os
import math

def get_dataset_results(dir_results):
    dfs = []
    for root, directories, filenames in os.walk(dir_results):    
        for filename in filenames:
            root += "/" if root[-1] != "/" else ""        
            df = pd.read_csv(root+filename)
            dfs.append(df)
    return pd.concat(dfs)
    


dir_ = '../../data/database/output_ml/M1/NER_extractor/'
file = 'accidents_tweets.tsv'


dataset = pd.read_csv(dir_+file, delimiter = "\t", quoting = 3)
dataset = dataset.sort_values(['id_tweet'])
dataset = dataset.reset_index(drop=True)

dataset['lat'] = math.nan
dataset['lon'] = math.nan


dir_results = dir_+"split/results_geocoding/"

geocoding = get_dataset_results(dir_results)
geocoding = geocoding.sort_values(['id_tweet'])
geocoding = geocoding.reset_index(drop=True)


for row in range(len(geocoding)):
    _id = geocoding.iloc[row]['id_tweet']
    lat, lon = geocoding.iloc[row]['best_lat'], geocoding.iloc[row]['best_long']
    
    index = dataset[dataset['id_tweet'] == _id].index.tolist()[0]
    dataset.at[index,'lat'] = lat
    dataset.at[index,'lon'] = lon
    
    if row % 1000 == 0:
        print("Progress... ", row)



"""
@Section: Filtrando tweets geolocalizados.
"""

dataset.info()

df_oct_nov_dic_ = dataset.dropna(subset=['lat','lon'])
df_oct_nov_dic_.to_csv(dir_+"accident_tweets_lat_lon_3_months.tsv",sep='\t',index=False)


#Guardando dataset original con lat y lon agregado
dataset.to_csv(dir_+"accident_tweets_lat_lon.tsv",sep='\t',index=False)









