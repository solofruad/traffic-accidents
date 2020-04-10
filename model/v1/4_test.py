#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 15:44:03 2020

@author: hat
"""

from classes.tweet2accident.preprocessing import Preprocessing
import pickle

textos = [
    "|￣￣￣￣￣￣￣￣￣￣￣| Beso con beso devuelvo💃|＿＿＿＿＿＿＿＿＿＿＿|               \ (•◡•) /                 \      /                    ---                   |   |",
    "Epaaaa jijijuemadre, somos dos",
    "Acuario con acuario.",
    "@pilar_rod Con achiras @Avianca",
    "A 20 años de tragedia de 'Machuca', víctimas siguen esperando justicia https://t.co/ognaNZt8wh vía @eltiempo",
    "Dos canastas..",
    "hola mundo"
]



#clean = Preprocessing(type_clean=5,njobs=4)
#clean.transform(textos)

accident_clasification_model = pickle.load(open('accident_clasification_model.pkl', 'rb'))
#result = accident_clasification_model.score(X_test, y_test)
#print(result)

text_pred = accident_clasification_model.predict(textos)