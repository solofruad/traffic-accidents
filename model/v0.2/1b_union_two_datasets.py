#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 15 16:40:02 2019

@author: hat
"""

import pandas as pd
import re

positive_excel = pd.read_csv("data/tagg/labeling/positive-excel-complete.tsv",delimiter="\t",quoting=3)
positive_tagenta = pd.read_csv("data/tagg/labeling/positive-tagenta-complete.tsv", delimiter="\t", quoting=3)

negative_excel = pd.read_csv("data/tagg/labeling/negative-excel-complete.tsv", delimiter="\t", quoting=3)
del negative_excel['Unnamed: 0']
negative_tagenta = pd.read_csv("data/tagg/labeling/negative-tagenta-complete.tsv",delimiter="\t", quoting=3)
negative_tagenta.rename(columns={'yes': 'si'}, inplace=True)

count_tweet_by_username = positive_excel['user_name'].value_counts() # Show distribution of tweets by user

"""
sub = positive_excel[positive_excel['user_name'] != 'BogotaTransito']
sub = sub[sub['user_name'] != 'rutassitp']
sub = sub[sub['user_name'] != 'WazeTrafficBOG']

sub["discard"] = ''
"""

positive_tagenta.rename(columns={'yes': 'si'}, inplace=True)
positive = pd.concat([positive_excel,positive_tagenta])
positive.to_csv("data/tagg/labeling/positive_complete.tsv",sep='\t', index=False)
positive['id_tweet'] = positive.id_tweet.apply(str)
positive['discard'] = ''
positive.to_excel("data/tagg/positive_complete.xlsx", index=False)

count_tweet_by_username = positive['user_name'].value_counts() # Show distribution of tweets by user


negative_tagenta.rename(columns={'yes': 'si'}, inplace=True)
del negative_excel['Unnamed: 0']
negative = pd.concat([negative_excel,negative_tagenta])
negative.to_csv("data/tagg/labeling/negative_complete.tsv",sep='\t', index=False)

count_tweet_by_username = negative['user_name'].value_counts() # Show distribution of tweets by user


"""
    Descartando tweets
"""
#Estos ya son tweets depurados
#positive_review = pd.read_excel("data/tagg/positive_complete.xlsx")
#positive = positive_review[positive_review['discard']!=1]

positive = pd.read_csv("data/positive_complete.tsv", delimiter = "\t",quoting = 3)
#positive.to_csv("data/positive_complete.tsv",sep='\t', index=False)

count_tweet_by_username = positive['user_name'].value_counts() # Show distribution of tweets by user

count_tweet_by_username.head(20)

del positive['discard']

bogotatransito = positive[positive['user_name'] == 'BogotaTransito']
rutassitp = positive[positive['user_name'] == 'rutassitp']

positive_repeat = pd.concat([bogotatransito, rutassitp])
positive_unique = positive[positive['user_name'] != 'BogotaTransito']
positive_unique = positive_unique[positive_unique['user_name'] != 'rutassitp']

"""
    División
"""
#Barajar las filas del dataframe
positive_repeat = positive_repeat.sample(frac=1).reset_index(drop=True)

#Partes iguales
positive_repeat = positive_repeat.drop_duplicates(['text'],keep='first')
positive_repeat = positive_repeat.sample(n=736).reset_index(drop=True)
positive_5050 = pd.concat([positive_unique, positive_repeat])
count_tweet_by_username = positive_5050['user_name'].value_counts() # Show distribution of tweets by user
positive_5050.to_csv("data/positive_5050.tsv",sep='\t', index=False)
count_tweet_by_username.head(20)


#70/30
positive_repeat = positive_repeat.drop_duplicates(['text'],keep='first')
positive_repeat = positive_repeat.sample(n=314).reset_index(drop=True)
positive_7030 = pd.concat([positive_unique, positive_repeat])
count_tweet_by_username = positive_7030['user_name'].value_counts() # Show distribution of tweets by user
positive_7030.to_csv("data/positive_7030.tsv",sep='\t', index=False)
count_tweet_by_username.head(20)

#Completo
positive_repeat = positive_repeat.drop_duplicates(['text'],keep='first')
positive_complete = pd.concat([positive_unique, positive_repeat])
positive_complete.to_csv("data/positive_100.tsv",sep='\t', index=False)
positive_complete = positive_complete.drop_duplicates(['text'],keep='first')

#Positivos del etiquetado por clusters

positive_cluster = pd.read_csv("data/v0/ok_positive.tsv", delimiter="\t", quoting=3)
positive_complete = pd.read_csv("data/positive_100.tsv",delimiter="\t", quoting=3)

diff = []
for index, row in positive_cluster.iterrows():    
    data = positive_complete[positive_complete['id_tweet'] == row['id_tweet']]
    if data.empty == True:
        tweet = {}
        tweet['created_at'] = row['created_at']
        tweet['id_tweet'] = row['id_tweet']
        tweet['user_name'] = row['user_name']
        tweet['text'] = row['text']
        diff.append(tweet)
        
result = pd.DataFrame(diff)
result['accident'] = ''
result['id_tweet'] = result.id_tweet.apply(str)
result = result[['id_tweet','user_name','created_at','text', 'accident']]
result.to_excel("data/tagg/positive_cluster.xlsx", index=False)
result.to_csv("data/dataset_cluster.tsv",sep='\t', index=False)


total = pd.concat([result,positive_complete])
total = total.drop_duplicates(['id_tweet'],keep='first')
aux = result.drop_duplicates(['id_tweet'],keep='first')


"""
    Después del filtrado manual del conjunto de datos por cluster
"""

cluster_filtro = pd.read_excel("data/tagg/positive_cluster.xlsx")
positive_cluster_filtro = cluster_filtro[cluster_filtro["accident"]==1]
del positive_cluster_filtro["accident"]
positive_cluster_filtro.to_csv("data/positive_cluster.tsv",sep='\t', index=False)
aux = pd.read_csv("data/positive_cluster.tsv", delimiter="\t", quoting=3)

##Unión de positive100 con el conjunto de positivos del cluster
positive_complete = pd.read_csv("data/positive_100.tsv",delimiter="\t", quoting=3)
positive_complete = positive_complete[['id_tweet','user_name','created_at','text']]
positive_union = pd.concat([positive_cluster_filtro,positive_complete])
positive_union = positive_union.drop_duplicates(['id_tweet'],keep='first')

count_tweet_by_username = positive_union['user_name'].value_counts() # Show distribution of tweets by user

#Eliminar los tweets parecidos que contienen "incidente vial entre"

data = positive_union[positive_union['text'].str.contains("Incidente vial entre")]
dataNo = positive_union[~positive_union['text'].str.contains("Incidente vial entre")]


#Propuesta 3
positive_union = positive_union[['id_tweet','user_name','created_at','text']]
positive_union.to_csv("data/positive/positive_100.tsv",sep='\t', index=False)
aux = pd.read_csv("data/positive/positive_100.tsv",delimiter="\t", quoting=3)


#Propuesta 1: 50/50

data = data.drop_duplicates(['text'],keep='first')
data = data.sample(frac=1).reset_index(drop=True)
data = data.sample(n=1332).reset_index(drop=True)
positive_5050 = pd.concat([dataNo, data])
positive_5050 = positive_5050[['id_tweet','user_name','created_at','text']]
positive_5050.to_csv("data/positive/positive_5050.tsv",sep='\t', index=False)
aux = pd.read_csv("data/positive/positive_5050.tsv",delimiter="\t", quoting=3)

count_tweet_by_username = positive_5050['user_name'].value_counts() # Show distribution of tweets by user

#Propuesta 2: 70/30

data = data.drop_duplicates(['text'],keep='first')
data = data.sample(frac=1).reset_index(drop=True)
data = data.sample(n=570).reset_index(drop=True)
positive_7030 = pd.concat([dataNo, data])
positive_7030 = positive_7030[['id_tweet','user_name','created_at','text']]
positive_7030.to_csv("data/positive/positive_7030.tsv",sep='\t', index=False)
aux = pd.read_csv("data/positive/positive_7030.tsv",delimiter="\t", quoting=3)

count_tweet_by_username = positive_7030['user_name'].value_counts() # Show distribution of tweets by user


"""
    Conjunto de datos negativo
"""
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

bogota = pd.read_csv("data/v0/4_stream_bogota.tsv",delimiter="\t",quoting=3)
#Barajar
bogota = bogota.sample(frac=1).reset_index(drop=True) #Barajar
bogota = bogota.sample(n=1800).reset_index(drop=True)
bogota = bogota[['id_tweet','user_name','created_at','text']]

bogota = removeRepeatText(bogota)
bogota = bogota.sample(n=1400).reset_index(drop=True)

bogota['discard'] = ''
bogota['id_tweet'] = bogota.id_tweet.apply(str)
bogota.to_excel("data/tagg/bogota_negative.xlsx", index=False)
bogota.to_csv("data/bogota_negative.tsv",sep='\t', index=False)


"""
    TAMBIEN DEDO HACER LIMPIEZA (LENGHT > 3) PARA EL DATASET NEGATIVE_EXCEL
"""
negative_excel = removeRepeatText(negative_excel)
negative_excel = negative_excel.sample(frac=1).reset_index(drop=True) #Barajar
negative_excel = negative_excel.sample(n=700).reset_index(drop=True)
negative_excel = negative_excel[['id_tweet','user_name','created_at','text']]
negative_excel['discard'] = ''
negative_excel['id_tweet'] = negative_excel.id_tweet.apply(str)
negative_excel.to_excel("data/tagg/excel_negative.xlsx", index=False)
negative_excel.to_csv("data/excel_negative.tsv",sep='\t', index=False)

###Despues de revisar los tweets uno por uno
negative_excel = pd.read_excel("data/tagg/excel_negative.xlsx")
negative_excel.to_csv("data/excel_negative.tsv",sep='\t', index=False)


negative_tagenta = removeRepeatText(negative_tagenta)
negative_tagenta = negative_tagenta.sample(frac=1).reset_index(drop=True) #Barajar
negative_tagenta = negative_tagenta.sample(n=1500).reset_index(drop=True)
negative_tagenta = negative_tagenta[['id_tweet','user_name','created_at','text']]
negative_tagenta['discard'] = ''
negative_tagenta['id_tweet'] = negative_tagenta.id_tweet.apply(str)
negative_tagenta.to_excel("data/tagg/tagenta_negative.xlsx", index=False)
negative_tagenta.to_csv("data/tagenta_negative.tsv",sep='\t', index=False)

negative_tagenta = pd.read_excel("data/tagg/tagenta_negative.xlsx")
negative_tagenta.to_csv("data/tagenta_negative.tsv",sep='\t', index=False)


###Los no relacionados del dataset que se hizo por cluster
negative_cluster_filtro = cluster_filtro[cluster_filtro["accident"]!=1]
del negative_cluster_filtro['accident']
negative_cluster_filtro.to_csv("data/negative_cluster.tsv",sep='\t', index=False)
aux = pd.read_csv("data/negative_cluster.tsv",delimiter="\t", quoting=3)


"""
    IMPORTAR CONJUNTO DE DATOS NEGATIVO
"""

negative_bogota = pd.read_csv("data/bogota_negative.tsv",delimiter="\t", quoting=3)
negative_excel = pd.read_csv("data/excel_negative.tsv",delimiter="\t", quoting=3)
negative_tagenta = pd.read_csv("data/tagenta_negative.tsv",delimiter="\t", quoting=3)
negative_cluster_filtro = pd.read_csv("data/negative_cluster.tsv",delimiter="\t", quoting=3)

#Propuesta 3: Este conjunto es para acompañar la propuesta 1 de arriba que es completo

negative_tagenta = negative_tagenta.sample(frac=1).reset_index(drop=True) #Barajar
negative_tagenta = negative_tagenta.sample(n=1151).reset_index(drop=True)
negative_tagenta = negative_tagenta[['id_tweet','user_name','created_at','text']]

negative = pd.concat([negative_cluster_filtro, negative_tagenta, negative_excel, negative_bogota])
negative = negative[['id_tweet','user_name','created_at','text']]
negative = negative.drop_duplicates(['text'],keep='first')
negative = negative.drop_duplicates(['id_tweet'],keep='first')

negative.to_csv("data/negative/negative_100.tsv",sep='\t', index=False)

#Propuesta 2: Este conjunto es para acompañar la propuesta 1 de arriba que es 70/30

negative_cluster_filtro = negative_cluster_filtro.sample(frac=1).reset_index(drop=True)
negative_tagenta = negative_tagenta.sample(frac=1).reset_index(drop=True)
negative_excel = negative_excel.sample(frac=1).reset_index(drop=True)
negative_bogota = negative_bogota.sample(frac=1).reset_index(drop=True)

negative_cluster_filtro = negative_cluster_filtro.sample(n=475).reset_index(drop=True)
negative_tagenta = negative_tagenta.sample(n=570).reset_index(drop=True)
negative_excel = negative_excel.sample(n=286).reset_index(drop=True)
negative_bogota = negative_bogota.sample(n=571).reset_index(drop=True)


negative_7030 = pd.concat([negative_cluster_filtro, negative_tagenta, negative_excel, negative_bogota])
negative_7030 = negative_7030[['id_tweet','user_name','created_at','text']]
negative_7030.to_csv("data/negative/negative_7030.tsv",sep='\t', index=False)


#Propuesta 1: Este conjunto es para acompañar la propuesta 1 de arriba que es 50/50

negative_cluster_filtro = negative_cluster_filtro.sample(frac=1).reset_index(drop=True)
negative_tagenta = negative_tagenta.sample(frac=1).reset_index(drop=True)
negative_excel = negative_excel.sample(frac=1).reset_index(drop=True)
negative_bogota = negative_bogota.sample(frac=1).reset_index(drop=True)

negative_cluster_filtro = negative_cluster_filtro.sample(n=665).reset_index(drop=True)
negative_tagenta = negative_tagenta.sample(n=799).reset_index(drop=True)
negative_excel = negative_excel.sample(n=400).reset_index(drop=True)
negative_bogota = negative_bogota.sample(n=800).reset_index(drop=True)


negative_5050 = pd.concat([negative_cluster_filtro, negative_tagenta, negative_excel, negative_bogota])
negative_5050 = negative_5050[['id_tweet','user_name','created_at','text']]
negative_5050.to_csv("data/negative/negative_5050.tsv",sep='\t', index=False)
aux = pd.read_csv("data/negative/negative_5050.tsv",delimiter="\t", quoting=3)



"""
    EXPORTAR A EXCEL EL CONJUNTO DE DATOS VERSION 2 COMPLETO
"""
positive_union['id_tweet'] = positive_union.id_tweet.apply(str)
positive_union.to_excel("data/positive/positive_100.xlsx", index=False)


negative.to_csv("data/negative/negative_100.tsv",sep='\t', index=False)

negative['id_tweet'] = negative.id_tweet.apply(str)
negative.to_excel("data/negative/negative_100.xlsx", index=False)

