#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 20:39:00 2019

@author: hat
"""
import numpy as np
import spacy  # For preprocessing
import re
import multiprocessing
from gensim.models.doc2vec import Doc2Vec
from gensim.models.phrases import Phrases, Phraser



class Preprocessing:
    def __init__(self, dataset):
        self.dataset = dataset
        self.cores = multiprocessing.cpu_count() # Count the number of cores in a computer
        
    def cleaning(self,doc):    
        txt = [token.lemma_ for token in doc if not token.is_stop]    
        if len(txt) > 2:
            return ' '.join(txt)
    
    def fit_clean(self):
        nlp = spacy.load("es_core_news_md",disabled=['ner','parser']) # disabling Named Entity Recognition for speed
        nlp.vocab["rt"].is_stop = True #Add RT to Stopwords

        brief_cleaning = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in self.dataset['text'])
        
        txt = [self.cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=50, n_threads=self.cores)]
        self.dataset['clean'] = txt
        self.dataset = self.dataset[~self.dataset['clean'].isnull()] #Elimina publicaciones que estan null al eliminarlo porque no generan valor en el proceso de limpieza
        self.dataset = self.dataset.reset_index(drop=True) # if limited the amount tweets drop index so that it does not interfere later in te for_each         

    def feature_extraction(self,size_dbow,size_dmm,size_vec):
        phraser_tg = Phraser.load("models/phraser_trigram-all-data.model")
        dmm = Doc2Vec.load("models/dmm/5-d2v-dmm-trig-f200-w5.model")
        dbow = Doc2Vec.load("models/dbow/5-d2v-dbow-unigram-f200-w5.model")
        
        vecs_id_tweet = np.zeros((len(self.dataset.clean.values),1))
        vecs_label = np.zeros((len(self.dataset.clean.values),1))
        vecs_dbow = np.zeros((len(self.dataset.clean.values), size_dbow))
        vecs_dmm = np.zeros((len(self.dataset.clean.values), size_dmm))
        vecs = np.zeros((len(self.dataset.clean.values), size_vec))
        
        for index, row in self.dataset.iterrows():    
            vecs_label[index] = row['label']
            vecs_id_tweet[index] = row['id_tweet']
            vecs_dbow[index] = dbow.infer_vector(row['clean'].split())        
            vecs_dmm[index] = dmm.infer_vector(phraser_tg[row['clean'].split()])
            vecs[index] = np.concatenate((vecs_id_tweet[index],vecs_label[index],vecs_dbow[index],vecs_dmm[index]))            
            
        return vecs
    
    
    def getCores(self):
        return self.cores
    
    def getDataset(self):
        return self.dataset