#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 09:31:23 2021

@author: hat
"""

import pandas as pd
import datetime
import matplotlib.pyplot as plt
import seaborn as sns

from shapely.geometry import Point
import math

def distance_fn(point_tweet, point_oficial):
    return 6378.137*math.acos(
        math.sin(math.radians(point_tweet.y))*math.sin(math.radians(point_oficial.y))
        +math.cos(math.radians(point_tweet.y))*math.cos(math.radians(point_oficial.y))
        *math.cos(math.radians(point_oficial.x)-math.radians(point_tweet.x)))

dirname_tweets = "../../data/database/output_ml/M1/NER_extractor/"
filename_tweets = 'accident_tweets_lat_lon_geocord_bogota_unique_keywords.tsv'


df_tweets = pd.read_csv(dirname_tweets+filename_tweets, delimiter = "\t", quoting = 3)

###### Importando base de datos oficial
dirname_oficial = "../../data/database/"
filename_oficial = 'historico_oficial_accidentes_bogota.tsv'

df_oficial = pd.read_csv(dirname_oficial+filename_oficial, delimiter = "\t", quoting = 3)


df_tweets.iloc[0]['created_at']
date = datetime.datetime.strptime(df_tweets.iloc[1]['created_at'], '%Y-%m-%d %H:%M:%S')
date.isoweekday()

time = df_tweets.apply(
    lambda tweet: datetime.datetime.strptime(tweet['created_at'], '%Y-%m-%d %H:%M:%S').hour,
    axis='columns'
)

time_oficial = df_oficial.apply(
    lambda oficial: datetime.datetime.strptime(oficial['FECHA_HORA_ACC'], '%Y-%m-%dT%H:%M:%S+00:00').hour,
    axis='columns'
)

weekday = df_tweets.apply(
    lambda tweet: datetime.datetime.strptime(tweet['created_at'], '%Y-%m-%d %H:%M:%S').isoweekday(),
    axis='columns'
)

weekday_oficial = df_oficial.apply(
    lambda oficial: datetime.datetime.strptime(oficial['FECHA_HORA_ACC'], '%Y-%m-%dT%H:%M:%S+00:00').isoweekday(),
    axis='columns'
)

df_tweets['time'] = time
df_oficial['time'] = time_oficial

df_tweets['weekday'] = weekday
df_oficial['weekday'] = weekday_oficial

df_tweets_oficial = df_tweets[df_tweets['user_name'] == "BogotaTransito"]
df_tweets_individual = df_tweets[df_tweets['user_name'] != "BogotaTransito"]


for i in range(len(df_tweets)):
    print(df_tweets.iloc[i]['created_at'], df_tweets.iloc[i]['weekday'])

count_tweet_by_time = df_tweets['time'].value_counts() # Show distribution of tweets by user

sns.distplot(df_tweets['time'], bins=47, label="Twitter")
plt.legend(prop={'size': 12})
plt.title('Twitter data')
plt.xlabel('Time of day (hour)')
plt.ylabel('Density')  

#sns.histplot(data=df_tweets, x="time", binwidth=3)

font = {'family' : 'normal',
        'weight' : 'normal',
        'size'   : 20}

plt.rc('font', **font)

fig_dims = (14, 8)
fig, ax = plt.subplots(figsize=fig_dims)

sns.distplot(df_oficial['time'], bins=47, hist=False, label="Oficial data", kde_kws={"lw": 3}, ax=ax)
plt.legend(prop={'size': 16})
plt.title('Official data')
plt.xlabel('Time of day (hour)')
plt.ylabel('Density')  

sns.distplot(df_tweets_oficial['time'], bins=47, hist=False, label="BogotaTransito", kde_kws={"lw": 3}, ax=ax)
plt.legend(prop={'size': 16})
plt.title('Twitter data')
plt.xlabel('Time of day (hour)')
plt.ylabel('Density')  

sns.distplot(df_tweets_individual['time'], bins=47, hist=False, label="Individual tweets", kde_kws={"lw": 3}, ax=ax)
plt.legend(prop={'size': 16})
plt.title('Time of day distribution of accidents on Twitter and official record ')
plt.xlabel('Time of day (hour)')
plt.ylabel('Density')  

ax.set_xticks(range(0,24))
plt.xlim(0, 24)

"""
weekday
"""


sns.distplot(df_tweets['weekday'], bins=13, norm_hist=True, kde=False, label="Twitter")
plt.legend(prop={'size': 12})
plt.title('Twitter data')
plt.xlabel('Weekday')
plt.ylabel('Density')  

fig_dims = (10, 8)
fig, ax = plt.subplots(figsize=fig_dims)
sns.distplot(df_oficial['weekday'], bins=13, norm_hist=True, kde=False, label="Oficial data", ax=ax)
plt.legend(prop={'size': 12})
plt.title('Oficial data')
plt.xlabel('Weekday')
plt.ylabel('Density')
ax.set_xticklabels(["","Mon","Tue", "Wed", "Thu", "Fri","Sat", "Sun"])
  

fig_dims = (10, 8)
fig, ax = plt.subplots(figsize=fig_dims)
sns.distplot(df_tweets_oficial['weekday'], bins=13, norm_hist=True, kde=False, label="Oficial tweets")
plt.legend(prop={'size': 12})
plt.title('Official data')
plt.xlabel('Weekday')
plt.ylabel('Density')  

sns.distplot(df_tweets_individual['weekday'], bins=13, norm_hist=True, kde=False, label="Individual tweets")
plt.legend(prop={'size': 12})
plt.title('Twitter data')
plt.xlabel('Weekday')
plt.ylabel('Density')  
ax.set_xticklabels(["","Mon","Tue", "Wed", "Thu", "Fri","Sat", "Sun"])




"""
Centro de Bogotá: 
    4.620087707451305, -74.06925517383849 (Centro Internacional de Bogotá)
    4.598670140670007, -74.07609571312378 (Plaza Bolivar)
"""

cib = Point(float(-74.06925517383849), float(4.620087707451305))
plaza = Point(float(-74.07609571312378), float(4.598670140670007))

points = df_tweets.apply(
    lambda srs: Point(float(srs['lon']), float(srs['lat'])),
    axis='columns'
)
df_tweets['geometry'] = points

points_oficial = df_oficial.apply(
    lambda srs: Point(float(srs['lon']), float(srs['lat'])),
    axis='columns'
)

df_oficial['geometry'] = points_oficial


df_tweets['distance'] = 1000.0
df_oficial['distance'] = 1000.0

for i in df_tweets.index.tolist():
    df_tweets.at[i, 'distance'] = distance_fn(cib, df_tweets.loc[i]['geometry'])

for i in df_oficial.index.tolist():
    df_oficial.at[i, 'distance'] = distance_fn(cib, df_oficial.loc[i]['geometry'])

fig_dims = (11, 8)
fig, ax = plt.subplots(figsize=fig_dims)
sns.distplot(df_tweets['distance'], bins=12)
plt.legend(prop={'size': 12})
plt.title('Twitter data')
plt.xlabel('Distance radius (km)')
plt.ylabel('Density')  

fig_dims = (11, 8)
fig, ax = plt.subplots(figsize=fig_dims)
sns.distplot(df_oficial['distance'], bins=12)
plt.legend(prop={'size': 12})
plt.title('Official data')
plt.xlabel('Distance radius (km)')
plt.ylabel('Density') 

df_tweets_oficial = df_tweets[df_tweets['user_name'] == "BogotaTransito"]
df_tweets_individual = df_tweets[df_tweets['user_name'] != "BogotaTransito"]

fig_dims = (12, 8)
fig, ax = plt.subplots(figsize=fig_dims)
sns.distplot(df_oficial['distance'], bins=12, hist=False, label="Official data", kde_kws={"lw": 3})
plt.legend(prop={'size': 16})
plt.title('Official data')
plt.xlabel('Distance radius (km)')
plt.ylabel('Density') 


sns.distplot(df_tweets_oficial['distance'], bins=12,  hist=False,label="BogotaTransito", kde_kws={"lw": 3})
plt.legend(prop={'size': 16})
plt.title('Twitter data')
plt.xlabel('Distance radius (km)')
plt.ylabel('Density')  

sns.distplot(df_tweets_individual['distance'], bins=12,  hist=False,label="Individual tweets", kde_kws={"lw": 3})
plt.legend(prop={'size': 16})
plt.title('Spatial distribution of accidents reported by Twitter and Official Record ')
plt.xlabel('Distance radius (km)')
plt.ylabel('Density')  
