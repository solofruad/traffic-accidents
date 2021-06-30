#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 18 15:07:48 2021

@author: hat
"""

import geopandas as gpd


dir_ = "../../data/database/"
file = "historico_accidentes.geojson"

accidentes = gpd.read_file(dir_+file)

#lat = accidentes.iloc[0]['geometry'].y
#lon = accidentes.iqgis<loc[0]['geometry'].x

#accidentes['FECHA_HORA_ACC']
accidentes = accidentes[(accidentes['FECHA_HORA_ACC'] >= '2018-10-01') & (accidentes['FECHA_HORA_ACC'] < '2019-08-01')]

accidentes = accidentes.reset_index(drop=True)


accidentes['lat'] = ''
accidentes['lon'] = ''

#accidentes.at[0,'lat'] = accidentes.iloc[0]['geometry'].y
#accidentes.at[0,'lon'] = accidentes.iloc[0]['geometry'].x


i = 0
for i in range(len(accidentes)):
    accidentes.at[i,'lat'] = accidentes.iloc[i]['geometry'].y
    accidentes.at[i,'lon'] = accidentes.iloc[i]['geometry'].x

accidentes.head(-5)

accidentes.to_csv(dir_+"historico_oficial_accidentes.tsv",sep='\t')
