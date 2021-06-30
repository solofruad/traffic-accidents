#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 21 11:42:02 2021

@author: hat
"""

import pandas as pd
import datetime
from shapely.geometry import Point
import math

import warnings
warnings.filterwarnings('ignore')


fecha_inicio = '2019-07-01'
fecha_final = '2019-08-01'

###### Importando tweets
dirname_tweets = "../../data/database/output_ml/M1/NER_extractor/"
filename_tweets = 'accident_tweets_lat_lon_geocord_bogota_unique_keywords.tsv'
#filename_tweets = '100_accident_tweets_test.tsv'
#filename_tweets = '280_accident_tweets_test.tsv'
#filename_tweets = '100_accident_tweets_test_less_1km.tsv'
#filename_tweets = '280_accident_tweets_test_less_1km.tsv'

#filename_tweets = '100_accident_tweets_test_v4.tsv'

df_tweets = pd.read_csv(dirname_tweets+filename_tweets, delimiter = "\t", quoting = 3)
#df_tweets = df_tweets[df_tweets['lat_manual'] != 'error']
#df_tweets.rename(columns={"lat_manual": "lat", "lon_manual":"lon"}, inplace = True)
#df_tweets.rename(columns={"lat_tweet": "lat", "lon_tweet":"lon"}, inplace = True)
#df_tweets.rename(columns={"best_lat": "lat", "best_long":"lon"}, inplace = True)
#df_tweets = aux
#df_tweets = df_tweets[(df_tweets['created_at'] >= fecha_inicio) & (df_tweets['created_at'] < fecha_final)]
df_tweets = df_tweets[df_tweets['user_name'] != 'BogotaTransito']
#df_tweets = df_tweets[:10000]
points = df_tweets.apply(
    lambda srs: Point(float(srs['lon']), float(srs['lat'])),
    axis='columns'
)

df_tweets['geometry'] = points

###### Importando base de datos oficial
dirname_oficial = "../../data/database/"
filename_oficial = 'historico_oficial_accidentes_bogota.tsv'

df_oficial = pd.read_csv(dirname_oficial+filename_oficial, delimiter = "\t", quoting = 3)
#df_oficial = df_oficial[(df_oficial['FECHA_HORA_ACC'] >= fecha_inicio) & (df_oficial['FECHA_HORA_ACC'] < fecha_final)]

points_oficial = df_oficial.apply(
    lambda srs: Point(float(srs['lon']), float(srs['lat'])),
    axis='columns'
)

df_oficial['geometry'] = points_oficial

def distance_fn(point_tweet, point_oficial):
    return 6378.137*math.acos(
        math.sin(math.radians(point_tweet.y))*math.sin(math.radians(point_oficial.y))
        +math.cos(math.radians(point_tweet.y))*math.cos(math.radians(point_oficial.y))
        *math.cos(math.radians(point_oficial.x)-math.radians(point_tweet.x)))
################ TEST % Tweets con match en BD oficial
def cobertura_tweets(df_tweets, df_oficial, distance_match, time_match) :
    data_list = []    
    for tweet in range(len(df_tweets)):
        if tweet%1000==0:
            print(tweet)
        
        #print(df_tweets.iloc[tweet]['address_normalization'])
        
        date = datetime.datetime.strptime(df_tweets.iloc[tweet]['created_at'], '%Y-%m-%d %H:%M:%S')
                
        start = date - datetime.timedelta(hours=time_match)
        start = start.strftime('%Y-%m-%dT%H:%M:%S')
        
        end = date + datetime.timedelta(hours=time_match)
        end = end.strftime('%Y-%m-%dT%H:%M:%S')
        
        df = df_oficial[(df_oficial['FECHA_HORA_ACC'] >= start) & (df_oficial['FECHA_HORA_ACC'] <= end)]
        df['match'] = False
        df['distance'] = 1000.0
        df['diff_time'] = datetime.timedelta(seconds=86400)
        df['diff_time_str'] = ''
        for i in df.index.tolist():
            tweet_selected =  df_tweets.iloc[tweet]
            oficial_selected = df.loc[i]
            
            point_tweet = tweet_selected['geometry']
            point_oficial = oficial_selected['geometry']
            
            date_tweet = datetime.datetime.strptime(tweet_selected['created_at'], '%Y-%m-%d %H:%M:%S')
            date_oficial = datetime.datetime.strptime(oficial_selected['FECHA_HORA_ACC'], '%Y-%m-%dT%H:%M:%S+00:00')
            #print("Coordenadas Tweet",point_tweet)
            #print("Coordenadas Tweet",point_oficial)
            
            #point_tweet.distance(point_oficial)
            
            # law of cosines
            # In Km
            distance = distance_fn(point_tweet, point_oficial)
            df.at[i, 'distance'] = distance
            df.at[i, 'match'] = True if distance <= distance_match else False
            df.at[i, 'diff_time'] = abs(date_tweet - date_oficial)
            df.at[i, 'diff_time_str'] = 'Earlier or equal' if date_tweet <= date_oficial else 'Later'
            
            #print(distance)
            
        result = df[df['match'] == True]
        result = result.sort_values(by=['distance','diff_time'])
        
        if len(result) > 0:
            result_index = result.index.tolist()[0]
            result = result.loc[result_index]
            
            data = {
                'id_tweet': tweet_selected['id_tweet'],
                'formulario': result['FORMULARIO'],
                'text': tweet_selected['text'],
                'user_name': tweet_selected['user_name'],
                'gravedad': result['GRAVEDAD'],
                'clase_acc': result['CLASE_ACC'],
                'address_tweet': tweet_selected['address_normalization'],
                'address_oficial': result['DIRECCION'],
                'created_tweet': tweet_selected['created_at'],
                'created_oficial': result['FECHA_HORA_ACC'],
                'lat_tweet': tweet_selected['lat'],
                'lon_tweet': tweet_selected['lon'],        
                'lat_oficial': result['lat'],
                'lon_oficial': result['lon'],
                'distance': result['distance'],
                'match': result['match'],
                'diff_time': result['diff_time'].seconds,
                'diff_time_str': result['diff_time_str'],
            }
            
            data_list.append(data)
            #df_oficial = df_oficial.drop(result_index)
            
    return data_list   

################ % Registros de BD oficial en Twitter
def cobertura_oficial(df_tweets, df_oficial, distance_match, time_match) :
    data_list = []    
    for oficial in range(len(df_oficial)):
        if oficial%1000==0:
            print(oficial)
        
        #print(df_oficial.iloc[oficial]['DIRECCION'])
        
        date = datetime.datetime.strptime(df_oficial.iloc[oficial]['FECHA_HORA_ACC'], '%Y-%m-%dT%H:%M:%S+00:00')
                
        start = date - datetime.timedelta(hours=time_match)
        start = start.strftime('%Y-%m-%d %H:%M:%S')
        
        end = date + datetime.timedelta(hours=time_match)
        end = end.strftime('%Y-%m-%d %H:%M:%S')
        
        df = df_tweets[(df_tweets['created_at'] >= start) & (df_tweets['created_at'] <= end)]
        df['match'] = False
        df['distance'] = 1000.0
        df['diff_time'] = datetime.timedelta(seconds=86400)
        df['diff_time_str'] = ''
        for i in df.index.tolist():
            tweet_selected =  df.loc[i]
            oficial_selected = df_oficial.iloc[oficial]
            
            point_tweet = tweet_selected['geometry']
            point_oficial = oficial_selected['geometry']
            
            date_tweet = datetime.datetime.strptime(tweet_selected['created_at'], '%Y-%m-%d %H:%M:%S')
            date_oficial = datetime.datetime.strptime(oficial_selected['FECHA_HORA_ACC'], '%Y-%m-%dT%H:%M:%S+00:00')
            #print("Coordenadas Tweet",point_tweet)
            #print("Coordenadas Tweet",point_oficial)
                        
            # law of cosines
            # In Km
            distance = distance_fn(point_tweet, point_oficial)
            df.at[i, 'distance'] = distance
            df.at[i, 'match'] = True if distance <= distance_match else False
            df.at[i, 'diff_time'] = abs(date_tweet - date_oficial)
            df.at[i, 'diff_time_str'] = 'Earlier or equal' if date_tweet <= date_oficial else 'Later'
            
            #print(distance)
            
        result = df[df['match'] == True]
        result = result.sort_values(by=['distance','diff_time'])
        
        if len(result) > 0:
            result_index = result.index.tolist()[0]
            result = result.loc[result_index]
            
            data = {
                'id_tweet': result['id_tweet'],
                'formulario': oficial_selected['FORMULARIO'],
                'text': result['text'],
                'user_name': result['user_name'],
                'gravedad': oficial_selected['GRAVEDAD'],
                'clase_acc': oficial_selected['CLASE_ACC'],
                'address_tweet': result['address_normalization'],
                'address_oficial': oficial_selected['DIRECCION'],
                'created_tweet': result['created_at'],
                'created_oficial': oficial_selected['FECHA_HORA_ACC'],
                'lat_tweet': result['lat'],
                'lon_tweet': result['lon'],
                'lat_oficial': oficial_selected['lat'],
                'lon_oficial': oficial_selected['lon'],
                'distance': result['distance'],
                'match': result['match'],
                'diff_time': result['diff_time'].seconds,
                'diff_time_str': result['diff_time_str'],
            }
            
            data_list.append(data)
            df_tweets = df_tweets.drop(result_index)
    return data_list 

distance_match = 1 # kms
time_match = 2 # hours
data_list = cobertura_tweets(df_tweets, df_oficial, distance_match, time_match)
#data_list = cobertura_oficial(df_tweets, df_oficial, distance_match, time_match)
df_result = pd.DataFrame(data_list)
    
count_tweet_by_username = df_tweets['id_tweet'].value_counts() # Show distribution of tweets by user
types_accidents = df_result['diff_time_str'].value_counts()

aux = df_result[df_result['diff_time_str'] == 'Later']
aux.describe()


df_result['id_tweet'].tolist()

aux = df_tweets.apply(
    lambda t: True if t['id_tweet'] in df_result['id_tweet'].tolist() else False,
    axis='columns'
)

df_tweets['matched'] = aux

aux = df_tweets[df_tweets['matched'] == False]
aux.describe()

"aux = df_tweets.sample(frac=1)
aux = df_tweets.sample(n=100)
aux = aux[['id_tweet','text','user_name','created_at','address_normalization','lat','lon']]
aux = aux.sort_values(by=['created_at'])
aux.to_csv(dirname_tweets+"77_accident_tweets_test.tsv",sep='\t',index=False)
"""
"""
https://keisan.casio.com/exec/system/1224587128
"""
