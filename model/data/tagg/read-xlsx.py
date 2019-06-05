#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jun  3 12:07:25 2019

@author: hat
"""
import pandas as pd  # For data handling

data_1_10 = pd.read_excel("data/tagg/1_search_1_10.xlsx")
data_10_20 = pd.read_excel("data/tagg/1_search_10_20.xlsx")
data_20_30 = pd.read_excel("data/tagg/1_search_20_30.xlsx")
data_30_40 = pd.read_excel("data/tagg/1_search_30_40.xlsx")
data_40_50 = pd.read_excel("data/tagg/1_search_40_50.xlsx")
data_50_60 = pd.read_excel("data/tagg/1_search_50_60.xlsx")
data_60_70 = pd.read_excel("data/tagg/1_search_60_70.xlsx")
data_70_80 = pd.read_excel("data/tagg/1_search_70_80.xlsx")
data_80_90 = pd.read_excel("data/tagg/1_search_80_90.xlsx")
data_90_100 = pd.read_excel("data/tagg/1_search_90_100.xlsx")
data_100_110 = pd.read_excel("data/tagg/1_search_100_110.xlsx")
data_110_120 = pd.read_excel("data/tagg/1_search_110_120.xlsx")
data_120_130 = pd.read_excel("data/tagg/1_search_120_130.xlsx")
data_130_140 = pd.read_excel("data/tagg/1_search_130_140.xlsx")
data_140_150 = pd.read_excel("data/tagg/1_search_140_150.xlsx")


name = "rubioGUI"

student_data_20_30 = pd.read_excel("data/tagg/labeling/"+name+"/Este uno.xlsx")

student_data_1_10 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_1_10.xlsx")
student_data_10_20 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_10_20.xlsx")
student_data_20_30 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_20_30.xlsx")
student_data_30_40 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_30_40.xlsx")
student_data_40_50 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_40_50.xlsx")
student_data_50_60 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_50_60.xlsx")
student_data_60_70 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_60_70.xlsx")
student_data_70_80 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_70_80.xlsx")
student_data_80_90 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_80_90.xlsx")
student_data_90_100 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_90_100.xlsx")
student_data_100_110 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_100_110.xlsx")
student_data_110_120 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_110_120.xlsx")
student_data_120_130 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_120_130.xlsx")
student_data_130_140 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_130_140.xlsx")
student_data_140_150 = pd.read_excel("data/tagg/labeling/"+name+"/1_search_140_150.xlsx")

student_data_1_10.info()
student_data_10_20.info()
student_data_20_30.info()
student_data_30_40.info()
student_data_40_50.info()
student_data_50_60.info()
student_data_60_70.info()
student_data_70_80.info()
student_data_80_90.info()
student_data_90_100.info()
student_data_100_110.info()
student_data_110_120.info()
student_data_120_130.info()
student_data_130_140.info()
student_data_140_150.info()

alejandra_data_10_20_excel.groupby('¿Está relacionado a un accidente de tránsito? si/no/ninguna').count()


data_1_10['id_tweet'].equals(student_data_1_10['id_tweet'])
data_10_20['id_tweet'].equals(student_data_10_20['id_tweet'])
data_20_30['id_tweet'].equals(student_data_20_30['id_tweet'])
data_30_40['id_tweet'].equals(student_data_30_40['id_tweet'])
data_40_50['id_tweet'].equals(student_data_40_50['id_tweet'])
data_50_60['id_tweet'].equals(student_data_50_60['id_tweet'])
data_60_70['id_tweet'].equals(student_data_60_70['id_tweet'])
data_70_80['id_tweet'].equals(student_data_70_80['id_tweet'])
data_80_90['id_tweet'].equals(student_data_80_90['id_tweet'])
data_90_100['id_tweet'].equals(student_data_90_100['id_tweet'])
data_100_110['id_tweet'].equals(student_data_100_110['id_tweet'])
data_110_120['id_tweet'].equals(student_data_110_120['id_tweet'])
data_120_130['id_tweet'].equals(student_data_120_130['id_tweet'])
data_130_140['id_tweet'].equals(student_data_130_140['id_tweet'])
data_140_150['id_tweet'].equals(student_data_140_150['id_tweet'])