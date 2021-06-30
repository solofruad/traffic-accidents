#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 27 21:50:43 2021

@author: hat
"""

import math

lat1 = df_result.iloc[150]['lat_tweet']
lon1 = df_result.iloc[150]['lon_tweet']

print("Tweet = lat:",lat1,"lon:",lon1)

lat2 = df_result.iloc[150]['lat_oficial']
lon2 = df_result.iloc[150]['lon_oficial']

print("Oficial = lat:",lat2,"lon:",lon2)

lat1 = math.radians(lat1)
lon1 = math.radians(lon1)

lat2 = math.radians(lat2)
lon2 = math.radians(lon2)

sins = math.sin(lat1)*math.sin(lat2)
coss = math.cos(lat1)*math.cos(lat2)*math.cos(lon2-lon1)

acos = math.acos(sins+coss)

d = 6378.137 * acos
print(d)