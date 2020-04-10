#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 13:20:07 2020

@author: hat
"""

import pandas as pd

filename = "server_bogota.tsv"
token_user = pd.read_csv("data/database/"+filename, delimiter = "\t", quoting = 3)

df1 = pd.read_csv("data/database/output_ml/accident_1_server_bogota_part1.tsv", delimiter = "\t", quoting = 3)
df2 = pd.read_csv("data/database/output_ml/accident_1_server_bogota_part2.tsv", delimiter = "\t", quoting = 3)
df3 = pd.read_csv("data/database/output_ml/accident_1_server_bogota_part3.tsv", delimiter = "\t", quoting = 3)
df4 = pd.read_csv("data/database/output_ml/accident_1_server_bogota_part4.tsv", delimiter = "\t", quoting = 3)
print("aa\\naa")

df = pd.concat([df1,df2,df3,df4])
df.to_csv("data/database/output_ml/accident_1_server_bogota.tsv",sep='\t', index=False)

camilo = df[df['user_name']=='jcontrerasa']
dataset1 = token_user[0:1000000]

dataset1.to_csv("data/database/server_bogota/server_bogota_part1.tsv",sep='\t', index=False)

dataset2 = token_user[1000000:2000000]
dataset2.to_csv("data/database/server_bogota/server_bogota_part2.tsv",sep='\t', index=False)


dataset3 = token_user[2000000:3000000]
dataset3.to_csv("data/database/server_bogota/server_bogota_part3.tsv",sep='\t', index=False)


dataset4 = token_user[3000000:]
dataset4.to_csv("data/database/server_bogota/server_bogota_part4.tsv",sep='\t', index=False)



df1 = pd.read_csv("data/database/output_ml/accident_1_server_bogota.tsv", delimiter = "\t", quoting = 3)
df2 = pd.read_csv("data/database/output_ml/accident_1_server_bogota_v2.tsv", delimiter = "\t", quoting = 3)
df3 = pd.read_csv("data/database/output_ml/accident_1_server_bogota_v3.tsv", delimiter = "\t", quoting = 3)

df = df3[['user_name','text','label', 'label_2','label_3']]