#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 15:05:00 2020

@author: hat
"""
import pandas as pd
from classes.tweet2accident.preprocessing import Preprocessing
import pickle

filename = '2_server_token_search.tsv'
dir_ = 'data/database/'

df = pd.read_csv(dir_+'output_ml/clf_'+filename, delimiter = "\t", quoting = 3 )
del df['Unnamed: 0']

df = df[['text','label_m1','label_m3','label_m4']]


train = pd.read_csv("data/v1/7030/train70.tsv", delimiter = "\t", quoting = 3)
test = pd.read_csv("data/v1/7030/test30.tsv", delimiter = "\t", quoting = 3)

X, y = train.text, train.label
X_test, y_test = test.text, test.label

dirmodel = 'notebook/1 Tweets Clasification/5 Filtering/'
model1 = pickle.load(open(dirmodel+'model_m1_dbow_svm.pkl', 'rb')) 
model3 = pickle.load(open(dirmodel+'model_m3_tfidf_svm_1.pkl', 'rb')) 
model4 = pickle.load(open(dirmodel+'model_m4_tfidf_svm_2.pkl', 'rb'))

y_pred1 = model1.predict(X_test)
y_pred3 = model3.predict(X_test)
y_pred4 = model4.predict(X_test)


import spacy  # For preprocessing
import re
def clean_fn(doc):
    #All characteres, without @, urls, # and numbers.        
    #stop = ['', 'rt']
    #txt = [token.text.strip() for token in doc if token.text.lower() != 'rt']    
    #print(txt)
    #if len(txt) > 4:        
    #    return ' '.join(txt)
    #else:
    #    return ''
    return doc.text
        
nlp = spacy.load("es_core_news_md",disabled=['ner','parser']) # disabling Named Entity Recognition for speed
nlp.vocab["rt"].is_stop = True #Add RT to Stopwords

X = train.iloc[75:81]['text']

"""
Clean tweets of:
    links: (\w+:\/\/\S+)
    username mentions: (@[A-Za-z0-9]+)
    emoticons, others specials characters, numbers: 
        ([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])
    Split Hashtags (HelloWorlds): ((?<=[A-Za-z])(?=[A-Z][a-z]))
"""

#Eliminar links
#Rempleazar @user for [UNK]
#Reemplazar RT for [UNK]

brief_cleaning = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row).strip()) for row in X)

txt = [clean_fn(doc) for doc in nlp.pipe(brief_cleaning, n_threads=-1)]

aux = train.iloc[80].text
#aux = train.iloc[0].text
#aux = "RT @Bocarejo_JP12: El 14 rt 👮🏻‍♀️  de &gt; &lt; ##dicieeeembre #reducciones ((reeemplazo)) #CaracolEsMás aart EsteÁr gooool gool??? [ (murieron) \"\"\"\"\" ? 2 ; peatones. \"\"atropellados\" \"\" por - conductores de transporte público y un ciclista por un conductor d…  https://t.co/CrF859mPPw rt"

def preText(text):
    #print("\nOriginal: "+text)
    pre = re.sub("(@[A-Za-z0-9_]+)", '[MASK]', text) #Reemplazar @username por [UNK]
    pre = re.sub("&[A-Za-z]+;", ' ', pre) #Eliminar códigos ASCII
    pre = re.sub("(\w+:\/\/\S+)",' ',pre) #Eliminar links http y https
    pre = re.sub("([^A-Za-z0-9äÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ,;.:\-\[\]¿?¡!#\"\"()])",' ',pre) #Eliminar caracteres especiales como emoticones, exceptuando los signos de puntuación y tildes.
    pre = re.sub(r'([;.:\-\[\]¿?¡!#\"()]){3,}',r'\1\1',pre) #Si repite un caracters especial más de 3 veces ej. """"
    pre = re.sub(r'([a-zA-Z])\1{2,}',r'\1\1',pre) #Si repite una letra más de dos veces las reduce a dos repeticiones goool => gool
    pre = re.sub(r'( rt )|( RT )|( Rt )|( rT )',r' ',pre) #Hashtags
    pre = re.sub(r'(^rt )|(^RT )|(^Rt )|(^rT )',r' ',pre) #Hashtags
    pre = re.sub(r'( rt$)|( RT$)|( Rt$)|( rT$)',r' ',pre) #Hashtags
    pre = re.sub(r'((?<=[A-Za-z])(?=[A-Z][a-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ]))',r' ',pre) #Hashtags
    pre = re.sub(r'(\s){2,}',r' ',pre) #Eliminar espacios seguidos    
    #pre = re.sub(r'(?!\w\s)rt(?!\w)',r' ',pre) #Hashtags
    
    #print("\nProcesado: "+pre)
    return pre

preText("rt hola... rt art articulo rto rt")
preText("RT ArTiculo #EsteEsUnEjemplo #EsMás RT")


brief_cleaning = (preText(str(row)) for row in X)
txt = [clean_fn(doc) for doc in nlp.pipe(brief_cleaning, n_threads=-1)]


#El RT lo reemplazo en la función clean_fn

#Falta:
# - Eliminar twwet [80] con muchos """"""""""
# - Eliminar emoticons
# - Eliminar caracteres especiales sin eliminar signos de puntuación
# - Eliminar # y Hashtags y separar las palabras juntas EsteEsUnEjemplo
# - No eliminar números



















