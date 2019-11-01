#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 22 18:38:58 2019

@author: hat
"""

"""
Clean dataset options:
    1. Stem.
    2. Lemma.
    3. only-stopwords without stem-lemma.
    4. All characteres, without @, urls, # and numbers.
    5. Stem without removes stopwords
    6. Lemma without removes stopwords
Two datasets input:
    1. 5050 bogota vs. no_bogota
    2. Complete, all tweets.
"""

import pandas as pd
import re
from time import time  # To time our operations
from nltk.stem import SnowballStemmer
import multiprocessing

import spacy  # For preprocessing
#!pip3 install -U spacy
#!python3 -m spacy download es_core_news_md

import logging  # Setting up the loggings to monitor

logger = logging.getLogger("clean_process")
hdlr = logging.FileHandler("log/logs_2.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

stemmer = SnowballStemmer('spanish')

def cleaning_stem_stopwords(doc):
    # Stemming and removes stopwords    
    #txt = [token.lemma_ for token in doc if not token.is_stop]    
    txt = [stemmer.stem(token.text) for token in doc if not token.is_stop]    
    if len(txt) > 2:
        return ' '.join(txt)
    
def cleaning_lemma_stopwords(doc):
    # Lemma and removes stopwords        
    txt = [(token.lemma_ if token.text != 'calle' else token.text) for token in doc if not token.is_stop]        
    if len(txt) > 2:
        return ' '.join(txt)

def cleaning_stopwords(doc):
    # Only removing stopwords        
    txt = [token.text for token in doc if not token.is_stop]    
    if len(txt) > 2:
        return ' '.join(txt)
    
def cleaning_special_chars(doc):
    #All characteres, without @, urls, # and numbers.        
    txt = [token.text for token in doc]    
    if len(txt) > 2:
        return ' '.join(txt)

def cleaning_stem(doc):
    #Stem without removes stopwords
    txt = [stemmer.stem(token.text) for token in doc]    
    if len(txt) > 2:
        return ' '.join(txt)
    
def cleaning_lemma(doc):
    #Lemma without removes stopwords
    txt = [(token.lemma_ if token.text != 'calle' else token.text) for token in doc]    
    if len(txt) > 2:
        return ' '.join(txt)
    
cores = multiprocessing.cpu_count()

proposals = ['dataset_propuesta2_complete.tsv']
dir_data = "data/v1/doc2vec/"
dir_ = 'data/v1/doc2vec/clean/'

for proposal in proposals:
    logger.info('# Starting...')
    logger.info('-- -- Reading file '+proposal)
    dataset = pd.read_csv(dir_data+proposal, delimiter = "\t", quoting = 3)
    del dataset['Unnamed: 0']
    #dataset = dataset.sample(n=10)
    
    #Stem
    logger.info("-- -- Loading nlp spacy in spanish")
    nlp = spacy.load("es_core_news_md",disabled=['ner','parser']) # disabling Named Entity Recognition for speed
    nlp.vocab["rt"].is_stop = True #Add RT to Stopwords
    
    logger.info(" ")
    logger.info('# Starting cleaning...')
    
    """
        |----------------------------------------------------------|
        |------------------1. Stem and stopwords-------------------|
        |----------------------------------------------------------|
    """
    """
    logger.info(" ")
    logger.info('## 1. Stem and stopwords')
    #Clean @, url, special characters,
    brief_cleaning = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in dataset['text'])
    
    t = time()    
    txt = [cleaning_stem_stopwords(doc) for doc in nlp.pipe(brief_cleaning, n_threads=cores)]
    #print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    logger.info('-- -- Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    
    df_clean_stem_stopwords = pd.DataFrame({'text': txt})
    df_clean_stem_stopwords = df_clean_stem_stopwords.dropna()
    filename = dir_+"1_clean_stem_stopwords_"+proposal+".tsv"
    df_clean_stem_stopwords.to_csv(filename,sep='\t')    
    logger.info('-- -- Se genero archivo tsv: '+filename)
    """
    """
        |----------------------------------------------------------|
        |------------------2. Lemma and stopwords------------------|
        |----------------------------------------------------------|
    """
    """
    logger.info(" ")
    logger.info('## 2. Lemma and stopwords')
    #Clean @, url, special characters,
    brief_cleaning = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in dataset['text'])
    
    t = time()    
    txt = [cleaning_lemma_stopwords(doc) for doc in nlp.pipe(brief_cleaning, n_threads=cores)]
    #print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    logger.info('-- -- Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    
    df_clean_lemma_stopwords = pd.DataFrame({'text': txt})
    df_clean_lemma_stopwords = df_clean_lemma_stopwords.dropna()
    filename = dir_+"2_clean_lemma_stopwords_"+proposal+".tsv"
    df_clean_lemma_stopwords.to_csv(filename,sep='\t')    
    logger.info('-- -- Se genero archivo tsv: '+filename)
    """
    """
        |----------------------------------------------------------|
        |------------------3. Only stopwords-----------------------|
        |----------------------------------------------------------|
    """
    """
    logger.info(" ")
    logger.info('## 3. Only stopwords')
    #Clean @, url, special characters,
    brief_cleaning = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in dataset['text'])
    
    t = time()    
    txt = [cleaning_stopwords(doc) for doc in nlp.pipe(brief_cleaning, n_threads=cores)]
    #print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    logger.info('-- -- Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    
    df_clean_stopwords = pd.DataFrame({'text': txt})
    df_clean_stopwords = df_clean_stopwords.dropna()
    filename = dir_+"3_clean_stopwords_"+proposal+".tsv"
    df_clean_stopwords.to_csv(filename,sep='\t')    
    logger.info('-- -- Se genero archivo tsv: '+filename)
    """
    """
        |----------------------------------------------------------|
        |--------------4. Only special characters------------------|
        |----------------------------------------------------------|
    """
    
    logger.info(" ")
    logger.info('## 4. Only special characters')
    #Clean @, url, special characters,
    brief_cleaning = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in dataset['text'])
    
    t = time()    
    txt = [cleaning_special_chars(doc) for doc in nlp.pipe(brief_cleaning, n_threads=cores)]
    #print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    logger.info('-- -- Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    
    df_clean_special_chars = pd.DataFrame({'text': txt})
    df_clean_special_chars = df_clean_special_chars.dropna()
    filename = dir_+"4_clean_special_chars_"+proposal+".tsv"
    df_clean_special_chars.to_csv(filename,sep='\t')    
    logger.info('-- -- Se genero archivo tsv: '+filename)
    
    """
        |----------------------------------------------------------|
        |-----------5. Stem without removes stopwords--------------|
        |----------------------------------------------------------|
    """
    """
    logger.info(" ")
    logger.info('## 5. Stem without removes stopwords')
    #Clean @, url, special characters,
    brief_cleaning = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in dataset['text'])
    
    t = time()    
    txt = [cleaning_stem(doc) for doc in nlp.pipe(brief_cleaning, n_threads=cores)]
    #print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    logger.info('-- -- Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    
    df_clean_stem = pd.DataFrame({'text': txt})
    df_clean_stem = df_clean_stem.dropna()
    filename = dir_+"5_clean_stem_"+proposal+".tsv"
    df_clean_stem.to_csv(filename,sep='\t')    
    logger.info('-- -- Se genero archivo tsv: '+filename)
    
    
    """
    """
        |----------------------------------------------------------|
        |----------6. Lemma without removes stopwords--------------|
        |----------------------------------------------------------|
    
    """
    """
    logger.info(" ")
    logger.info('## 6. Lemma without removes stopwords')
    #Clean @, url, special characters,
    brief_cleaning = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in dataset['text'])
    
    t = time()    
    txt = [cleaning_lemma(doc) for doc in nlp.pipe(brief_cleaning, n_threads=cores)]
    #print('Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    logger.info('-- -- Time to clean up everything: {} mins'.format(round((time() - t) / 60, 2)))
    
    df_clean_lemma = pd.DataFrame({'text': txt})
    df_clean_lemma = df_clean_lemma.dropna()
    filename = dir_+"6_clean_lemma_"+proposal+".tsv"
    df_clean_lemma.to_csv(filename,sep='\t')    
    logger.info('-- -- Se genero archivo tsv: '+filename)
    """
    logger.info('### Finish clean dataset '+proposal+' ####')
    logger.info('############################################################')
    logger.info(' ')
    
    
