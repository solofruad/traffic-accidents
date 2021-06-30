#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 09:28:34 2021

@author: hat
"""

import pandas as pd
from ast import literal_eval

from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


def isBogotaGmap(loc):
    point = Point(loc["lng"], loc["lat"])
    polygon = Polygon([(-74.2306435108,4.4863006081),
                  (-74.0110886097,4.4863006081),
                  (-74.0110886097,4.8330709005),
                  (-74.2306435108,4.8330709005),
                  (-74.2306435108,4.4863006081)])
    return polygon.contains(point)

def isBogota(loc):    
    point = Point(loc["lon"], loc["lat"])
    polygon = Polygon([(-74.2306435108,4.4863006081), #Bogota
                  (-74.0110886097,4.4863006081),
                  (-74.0110886097,4.8330709005),
                  (-74.2306435108,4.8330709005),
                  (-74.2306435108,4.4863006081)])
    return polygon.contains(point)


#dir_ = "../../data/v1/NER/"
#file = "ner_dataset_norm_lat_lon.tsv"

### Oficial database
#dir_ = "../../data/database/"
#file = "historico_oficial_accidentes.tsv"

dir_ = '../../data/database/output_ml/M1/NER_extractor/'
#file = 'accident_tweets_lat_lon_3_months.tsv'
file = 'accident_tweets_lat_lon_geocord_bogota.tsv'


dataset = pd.read_csv(dir_+file,sep="\t")
del dataset["Unnamed: 0"]
#aux = dataset.drop_duplicates(subset=['id_tweet'])
#dataset.gmap = dataset.gmap.apply(literal_eval)


#lat, lon = 4.142, -73.62664 #Villavo
#lat, lon = 4.596434285798705, -74.10952117387987 # Bogota
#lat, lon = 4.669607377456717, -74.01611284069145
#loc = (lon,lat)

#print(isBogota(loc))


aux = dataset.apply(isBogota, axis=1)

#dataset = dataset[dataset.gmap.apply(isBogotaGmap)]
dataset = dataset[dataset.apply(isBogota, axis=1)]

dataset.to_csv(dir_+"historico_oficial_accidentes_bogota.tsv",sep='\t',index=False)



