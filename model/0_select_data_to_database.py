#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 16 10:38:17 2019

@author: hat
"""

import pandas as pd  # For data handling

data = pd.read_csv("data/v0/1_search_shuffle.tsv", delimiter = "\t", quoting = 3)
data = data[['id_tweet','text','created_at']]

#Seleccionar la muestra
data = data.reset_index(drop=True)
subdataset = data.iloc[0:20]

subdataset['source'] = 'twitter'
subdataset['complete'] = 0

subdataset = subdataset.rename(columns={'id_tweet':'id_source'})

subdataset.to_json("data/subdataset_to_database_sailsj.csv",sep='\t',index=False)
