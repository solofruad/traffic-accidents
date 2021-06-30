#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 18 21:06:28 2021

@author: hat
"""

import pandas as pd
import numpy as np
import spacy

import datetime
from scipy.spatial import distance

nlp = spacy.load("es_core_news_lg")


dir_ = "../../data/database/output_ml/M1/NER_extractor/"
file = 'accidents_tweets.tsv'

dataset = pd.read_csv(dir_+file, delimiter = "\t", quoting = 3)

dataset = dataset.sort_values(by=['address_normalization'])
dataset = dataset.reset_index(drop=True)
#dataset = dataset[:10000]

vectors = {}
for row in range(len(dataset)):
    address = dataset.iloc[row]['address_normalization'].lower()[7:]
    doc1 = nlp(address)
    vector = np.zeros(300)
    for token in doc1:
        vector += token.vector
    vector /= len(doc1)
    vectors[row] = vector
    if row%1000==0:
        print(row)
    

dataset['similarity'] = False

for tweet in range(len(dataset)):
    if tweet%1000==0:
        print(tweet)
    if dataset.iloc[tweet]['similarity'] == False:
        #tweet = 21
        
        date = datetime.datetime.strptime(dataset.iloc[tweet]['created_at'], '%Y-%m-%d %H:%M:%S')
        
        start = date - datetime.timedelta(hours=1)
        start = start.strftime('%Y-%m-%d %H:%M:%S')
        
        end = date + datetime.timedelta(hours=1)
        end = end.strftime('%Y-%m-%d %H:%M:%S')
        
        df = dataset[(dataset['created_at'] >= start) & (dataset['created_at'] <= end) & (dataset['similarity'] == False)]
        
        similarity = df.index.tolist()
        
        # Calculando la similitud de todos los tweets cercanos a la fecha, incluso si mismo.
        # Todos los tweets menores a la distancia 0.05 pasan a True es decir si encontró similitud
        for i in similarity:
            df.at[i,'similarity'] = True if distance.cosine(vectors[tweet],vectors[i]) < 0.01 else False
            
        # Quiero tomar el primer tweet que se publicó por lo tanto selecciono el tweets más viejo
        # Para esto creo un dataframe temporal, es necesario para pasar a False el tweet más viejo dentro del grupo de match
        df_ = df[df['similarity'] == True]
        df_ = df_.sort_values(by=['created_at'])
        #Solo debo pasar a False el primer tweet publicado del accidente, más adelante elimino los True
        df.at[df_.index.tolist()[0],'similarity'] = False
        
        # Ahora necesito asignar los valores True o False de emparejamiento al dataset original
        for i in  df.index.tolist():
            selected = df[df['id_tweet'] == dataset.iloc[i]['id_tweet']]
            dataset.at[i, 'similarity'] = selected.iloc[0]['similarity']

result = dataset[dataset['similarity'] == False]
del result['similarity']

result = result.reset_index(drop=True)

result.to_csv(dir_+"data_shielded_experiment/accident_tweets_unique.tsv",sep='\t',index=False)



t1 = nlp('AVENIDA BOYACA AVENIDA CALLE 166')
t2 = nlp('AVENIDA BOYACA AVENIDA CALLE 168')
t1.similarity(t2)


"""----------------------------------------------------------------------------------------------"""

tweet = 55
        
date = datetime.datetime.strptime(dataset.iloc[tweet]['created_at'], '%Y-%m-%d %H:%M:%S')

start = date - datetime.timedelta(hours=12)
start = start.strftime('%Y-%m-%d %H:%M:%S')

end = date + datetime.timedelta(hours=12)
end = end.strftime('%Y-%m-%d %H:%M:%S')

df = dataset[(dataset['created_at'] >= start) & (dataset['created_at'] <= end) & (dataset['similarity'] == False)]
#df = df.drop(tweet)

similarity = df.index.tolist()

for i in similarity:
    df.at[i,'similarity'] = True if distance.cosine(vectors[tweet],vectors[i]) < 0.05 else False


df_ = df[df['similarity'] == True]
df_ = df_.sort_values(by=['created_at'])
tweet_selected = df_.index.tolist()[0]
df.at[tweet_selected,'similarity'] = False

tweets_index = df.index.tolist()
for i in tweets_index:
    selected = df[df['id_tweet'] == dataset.iloc[i]['id_tweet']]
    dataset.at[i, 'similarity'] = selected.iloc[0]['similarity']






for i in range(len(df)):
    print(df.iloc[i]['id_tweet'])














