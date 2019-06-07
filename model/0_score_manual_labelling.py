#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  5 08:14:10 2019

@author: hat
"""

import pandas as pd  # For data handling


def corregir_label(label):
    if label == "No" or label == "no":   
        return "no"
    elif label == "Si" or label == "si":
        return "si"
    else:
        return "none";


alejandraPOO = "alejandraPOO"
arteagaGUI = "arteagaGUI"
belloGUI = "belloGUI"
cardonaGUI = "cardonaGUI"
durangoGUI = "durangoGUI"
galindezStruct = "galindezStruct"
hernandezParraGUI = "hernandezParraGUI"
murciaGUI = "murciaGUI"
noreniaGUI = "noreniaGUI"
ospinaGUI = "ospinaGUI"
pedroPOO = "pedroPOO"
rubioGUI = "rubioGUI"
nestor = "nestor"


#1_10
alejandraPOO_data_1_10 = pd.read_excel("data/tagg/labeling/"+alejandraPOO+"/1_search_1_10.xlsx")
alejandraPOO_data_1_10.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

arteagaGUI_data_1_10 = pd.read_excel("data/tagg/labeling/"+arteagaGUI+"/1_search_1_10.xlsx")
arteagaGUI_data_1_10.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

data_1_10 = pd.concat([alejandraPOO_data_1_10,arteagaGUI_data_1_10])


#10_20
alejandraPOO_data_10_20 = pd.read_excel("data/tagg/labeling/"+alejandraPOO+"/1_search_10_20.xlsx")
alejandraPOO_data_10_20.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

belloGUI_data_10_20 = pd.read_excel("data/tagg/labeling/"+belloGUI+"/1_search_10_20.xlsx")
belloGUI_data_10_20.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

noreniaGUI_data_10_20 = pd.read_excel("data/tagg/labeling/"+noreniaGUI+"/1_search_10_20.xlsx")
noreniaGUI_data_10_20.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_10_20 = pd.concat([alejandraPOO_data_10_20,belloGUI_data_10_20,noreniaGUI_data_10_20])


#20_30
alejandraPOO_data_20_30 = pd.read_excel("data/tagg/labeling/"+alejandraPOO+"/1_search_20_30.xlsx")
alejandraPOO_data_20_30.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

murciaGUI_data_20_30 = pd.read_excel("data/tagg/labeling/"+murciaGUI+"/1_search_20_30.xlsx")
murciaGUI_data_20_30.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

cardonaGUI_data_20_30 = pd.read_excel("data/tagg/labeling/"+cardonaGUI+"/1_search_20_30.xlsx")
cardonaGUI_data_20_30.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_20_30 = pd.concat([alejandraPOO_data_20_30,murciaGUI_data_20_30,cardonaGUI_data_20_30])


#30_40
pedroPOO_data_30_40 = pd.read_excel("data/tagg/labeling/"+pedroPOO+"/1_search_30_40.xlsx")
pedroPOO_data_30_40.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

durangoGUI_data_30_40 = pd.read_excel("data/tagg/labeling/"+durangoGUI+"/1_search_30_40.xlsx")
durangoGUI_data_30_40.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

hernandezParraGUI_data_30_40 = pd.read_excel("data/tagg/labeling/"+hernandezParraGUI+"/1_search_30_40.xlsx")
hernandezParraGUI_data_30_40.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_30_40 = pd.concat([pedroPOO_data_30_40,durangoGUI_data_30_40,hernandezParraGUI_data_30_40])


#40_50
pedroPOO_data_40_50 = pd.read_excel("data/tagg/labeling/"+pedroPOO+"/1_search_40_50.xlsx")
pedroPOO_data_40_50.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

rubioGUI_data_40_50 = pd.read_excel("data/tagg/labeling/"+rubioGUI+"/1_search_40_50.xlsx")
rubioGUI_data_40_50.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

ospinaGUI_data_40_50 = pd.read_excel("data/tagg/labeling/"+ospinaGUI+"/1_search_40_50.xlsx")
ospinaGUI_data_40_50.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_40_50 = pd.concat([pedroPOO_data_40_50,rubioGUI_data_40_50,ospinaGUI_data_40_50])

#50_60
pedroPOO_data_50_60 = pd.read_excel("data/tagg/labeling/"+pedroPOO+"/1_search_50_60.xlsx")
pedroPOO_data_50_60.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

murciaGUI_data_50_60 = pd.read_excel("data/tagg/labeling/"+murciaGUI+"/1_search_50_60.xlsx")
murciaGUI_data_50_60.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

arteagaGUI_data_50_60 = pd.read_excel("data/tagg/labeling/"+arteagaGUI+"/1_search_50_60.xlsx")
arteagaGUI_data_50_60.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_50_60 = pd.concat([pedroPOO_data_50_60,murciaGUI_data_50_60,arteagaGUI_data_50_60])

#60_70
pedroPOO_data_60_70 = pd.read_excel("data/tagg/labeling/"+pedroPOO+"/1_search_60_70.xlsx")
pedroPOO_data_60_70.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

murciaGUI_data_60_70 = pd.read_excel("data/tagg/labeling/"+murciaGUI+"/1_search_60_70.xlsx")
murciaGUI_data_60_70.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

galindezStruct_data_60_70 = pd.read_excel("data/tagg/labeling/"+galindezStruct+"/1_search_60_70.xlsx")
galindezStruct_data_60_70.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_60_70 = pd.concat([pedroPOO_data_60_70,murciaGUI_data_60_70,galindezStruct_data_60_70])


#70_80
pedroPOO_data_70_80 = pd.read_excel("data/tagg/labeling/"+pedroPOO+"/1_search_70_80.xlsx")
pedroPOO_data_70_80.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

murciaGUI_data_70_80 = pd.read_excel("data/tagg/labeling/"+murciaGUI+"/1_search_70_80.xlsx")
murciaGUI_data_70_80.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

belloGUI_data_70_80 = pd.read_excel("data/tagg/labeling/"+belloGUI+"/1_search_70_80.xlsx")
belloGUI_data_70_80.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_70_80 = pd.concat([pedroPOO_data_70_80,murciaGUI_data_70_80,belloGUI_data_70_80])


#80_90
pedroPOO_data_80_90 = pd.read_excel("data/tagg/labeling/"+pedroPOO+"/1_search_80_90.xlsx")
pedroPOO_data_80_90.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

murciaGUI_data_80_90 = pd.read_excel("data/tagg/labeling/"+murciaGUI+"/1_search_80_90.xlsx")
murciaGUI_data_80_90.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

durangoGUI_data_80_90 = pd.read_excel("data/tagg/labeling/"+durangoGUI+"/1_search_80_90.xlsx")
durangoGUI_data_80_90.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_80_90 = pd.concat([pedroPOO_data_80_90,murciaGUI_data_80_90,durangoGUI_data_80_90])


#90_100
murciaGUI_data_90_100 = pd.read_excel("data/tagg/labeling/"+murciaGUI+"/1_search_90_100.xlsx")
murciaGUI_data_90_100.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

arteagaGUI_data_90_100 = pd.read_excel("data/tagg/labeling/"+arteagaGUI+"/1_search_90_100.xlsx")
arteagaGUI_data_90_100.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

rubioGUI_data_90_100 = pd.read_excel("data/tagg/labeling/"+rubioGUI+"/1_search_90_100.xlsx")
rubioGUI_data_90_100.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_90_100 = pd.concat([murciaGUI_data_90_100,arteagaGUI_data_90_100,rubioGUI_data_90_100])


#100_110
durangoGUI_data_100_110 = pd.read_excel("data/tagg/labeling/"+durangoGUI+"/1_search_100_110.xlsx")
durangoGUI_data_100_110.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

hernandezParraGUI_data_100_110 = pd.read_excel("data/tagg/labeling/"+hernandezParraGUI+"/1_search_100_110.xlsx")
hernandezParraGUI_data_100_110.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

rubioGUI_data_100_110 = pd.read_excel("data/tagg/labeling/"+rubioGUI+"/1_search_100_110.xlsx")
rubioGUI_data_100_110.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_100_110 = pd.concat([durangoGUI_data_100_110,hernandezParraGUI_data_100_110,rubioGUI_data_100_110])

#110_120
arteagaGUI_data_110_120 = pd.read_excel("data/tagg/labeling/"+arteagaGUI+"/1_search_110_120.xlsx")
arteagaGUI_data_110_120.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

hernandezParraGUI_data_110_120 = pd.read_excel("data/tagg/labeling/"+hernandezParraGUI+"/1_search_110_120.xlsx")
hernandezParraGUI_data_110_120.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

noreniaGUI_data_110_120 = pd.read_excel("data/tagg/labeling/"+noreniaGUI+"/1_search_110_120.xlsx")
noreniaGUI_data_110_120.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_110_120 = pd.concat([arteagaGUI_data_110_120,hernandezParraGUI_data_110_120,noreniaGUI_data_110_120])

#120_130
arteagaGUI_data_120_130 = pd.read_excel("data/tagg/labeling/"+arteagaGUI+"/1_search_120_130.xlsx")
arteagaGUI_data_120_130.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

durangoGUI_data_120_130 = pd.read_excel("data/tagg/labeling/"+durangoGUI+"/1_search_120_130.xlsx")
durangoGUI_data_120_130.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)

cardonaGUI_data_120_130 = pd.read_excel("data/tagg/labeling/"+cardonaGUI+"/1_search_120_130.xlsx")
cardonaGUI_data_120_130.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_120_130 = pd.concat([arteagaGUI_data_120_130,durangoGUI_data_120_130,cardonaGUI_data_120_130])


#130_140
belloGUI_data_130_140 = pd.read_excel("data/tagg/labeling/"+belloGUI+"/1_search_130_140.xlsx")
belloGUI_data_130_140.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)
belloGUI_data_130_140 = belloGUI_data_130_140[['id_tweet',"text","label"]]

noreniaGUI_data_130_140 = pd.read_excel("data/tagg/labeling/"+noreniaGUI+"/1_search_130_140.xlsx")
noreniaGUI_data_130_140.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)


data_130_140 = pd.concat([belloGUI_data_130_140,noreniaGUI_data_130_140])


"""
    **********************************************
        PASO FINAL: Concatenar todo
    **********************************************
"""
frames_three = [
        data_10_20, 
        data_20_30, 
        data_30_40, 
        data_40_50, 
        data_50_60, 
        data_60_70, 
        data_70_80,
        data_80_90,
        data_90_100,
        data_100_110,
        data_110_120,
        data_120_130
        ]
frames_two = [data_1_10, data_130_140]


dataset_three = pd.concat(frames_three)
dataset_two = pd.concat(frames_two)
#dataset = dataset.sample(n=20)
dataset_three.groupby('label').count()

dataset_three.info()


dataset_three['label'] = list(map(corregir_label, dataset_three['label']))
dataset_two['label'] = list(map(corregir_label, dataset_two['label']))

dummy = pd.get_dummies(dataset_three['label'])
dataset_three = pd.concat([dataset_three,dummy],axis=1)

dummy_two = pd.get_dummies(dataset_two['label'])
dataset_two = pd.concat([dataset_two,dummy_two],axis=1)

dataset_three['no'] = dataset_three.groupby(['id_tweet'])['no'].transform('sum')
dataset_three['si'] = dataset_three.groupby(['id_tweet'])['si'].transform('sum')
dataset_three['none'] = dataset_three.groupby(['id_tweet'])['none'].transform('sum')

dataset_three_score = dataset_three.drop_duplicates(subset=['id_tweet'])
del dataset_three_score['label']

dataset_two['no'] = dataset_two.groupby(['id_tweet'])['no'].transform('sum')
dataset_two['si'] = dataset_two.groupby(['id_tweet'])['si'].transform('sum')
dataset_two['none'] = dataset_two.groupby(['id_tweet'])['none'].transform('sum')

dataset_two_score = dataset_two.drop_duplicates(subset=['id_tweet'])
del dataset_two_score['label']


yes = dataset_three_score[dataset_three_score['si'] >= 2]
no = dataset_three_score[dataset_three_score['no'] > 2]


yes2 = dataset_two_score[dataset_two_score['si'] >= 2]
no2 = dataset_two_score[dataset_two_score['no'] >= 2]

dataset_positive = pd.concat([yes,yes2])
dataset_negative = pd.concat([no,no2])


dataset_positive.to_csv("data/tagg/labeling/positive.tsv",sep='\t')
dataset_negative.to_csv("data/tagg/labeling/negative.tsv",sep='\t')

positive = pd.read_csv("data/tagg/labeling/positive.tsv", delimiter = "\t",quoting = 3)
negative = pd.read_csv("data/tagg/labeling/negative.tsv", delimiter = "\t",quoting = 3)

"""
    Pedazo recordato porque hice la encuesta después de filtrado todo lo de arriba
"""

#140_150
noreniaGUI_data_140_150 = pd.read_excel("data/tagg/labeling/"+noreniaGUI+"/1_search_140_150.xlsx")
noreniaGUI_data_140_150.rename(columns={'Si':'label'},inplace = True)
noreniaGUI_data_140_150.info()
noreniaGUI_data_140_150.groupby('label').count()

nestor_data_140_150 = pd.read_excel("data/tagg/labeling/"+nestor+"/1_search_140_150.xlsx")
nestor_data_140_150.rename(columns={'¿Está relacionado a un accidente de tránsito? si/no/ninguna':'label'},inplace = True)
nestor_data_140_150.info()
nestor_data_140_150.groupby('label').count()

data_140_150 = pd.concat([noreniaGUI_data_140_150,nestor_data_140_150])

data_140_150['label'] = list(map(corregir_label, data_140_150['label']))
data_140_150.groupby('label').count()

dummy = pd.get_dummies(data_140_150['label'])
data_140_150 = pd.concat([data_140_150,dummy],axis=1)

data_140_150['no'] = data_140_150.groupby(['id_tweet'])['no'].transform('sum')
data_140_150['si'] = data_140_150.groupby(['id_tweet'])['si'].transform('sum')
data_140_150['none'] = data_140_150.groupby(['id_tweet'])['none'].transform('sum')

data_140_150_score = data_140_150.drop_duplicates(subset=['id_tweet'])
del data_140_150_score['label']

yes = data_140_150_score[data_140_150_score['si'] >= 2]
no = data_140_150_score[data_140_150_score['no'] >= 2]

yes2 = nestor_data_140_150[nestor_data_140_150['label'] == "si"]
yes2 = yes2[yes2['label'] == "si"]
yes2['no'] = 0
yes2['none'] = 0
yes2['si'] = 3
del yes2['label']

positive = pd.read_csv("data/tagg/labeling/positive.tsv", delimiter = "\t",quoting = 3)
del positive['Unnamed: 0']

positive = pd.concat([yes2,positive])
positive.to_csv("data/tagg/labeling/positive.tsv",sep='\t', index=False)
