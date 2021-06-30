#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 31 20:41:36 2021

@author: hat
"""

import pandas as pd
import datetime
from shapely.geometry import Point
import math

import warnings
warnings.filterwarnings('ignore')

def distance_fn(point1, point2):
    return 6378.137*math.acos(
        math.sin(math.radians(point1.y))*math.sin(math.radians(point2.y))
        +math.cos(math.radians(point1.y))*math.cos(math.radians(point2.y))
        *math.cos(math.radians(point2.x)-math.radians(point1.x)))

dirname_tweets = "../../data/database/output_ml/M1/NER_extractor/"
filename_tweets = '280_accident_tweets_test.tsv'
#filename_tweets = '/test/geocode_results_2021_06_01_r4_b5.csv'

df_tweets = pd.read_csv(dirname_tweets+filename_tweets, delimiter = "\t", quoting = 3)
#df_tweets = pd.read_csv(dirname_tweets+filename_tweets)
df_tweets = df_tweets[df_tweets['lat_manual'] != 'error']

#df_tweets['iso2'] = 'CO'

#df_tweets.to_csv(dirname_tweets+"100_accident_tweets_test_format.csv",index=False)

#df_tweets = df_tweets[df_tweets['best_name'] == 'Vetted']
"""points = df_tweets.apply(
    lambda srs: Point(float(srs['best_long']), float(srs['best_lat'])),
    axis='columns'
)"""


points = df_tweets.apply(
    lambda srs: Point(float(srs['lon_tweet']), float(srs['lat_tweet'])),
    axis='columns'
)

df_tweets['point_tweet'] = points

points = df_tweets.apply(
    lambda srs: Point(float(srs['lon_manual']), float(srs['lat_manual'])),
    axis='columns'
)

df_tweets['point_manual'] = points
df_tweets['distance'] = 1000.0

df_tweets.reset_index(drop=True, inplace=True)


for tweet in range(len(df_tweets)):
    distance = distance_fn(df_tweets.iloc[tweet]['point_tweet'],df_tweets.iloc[tweet]['point_manual'])
    df_tweets.at[tweet, 'distance'] = distance

result = df_tweets[df_tweets['distance'] <= 1.0]
result.to_csv(dirname_tweets+"280_accident_tweets_test_less_1km.tsv",sep='\t',index=False)



















