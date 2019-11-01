#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 20:39:00 2019

@author: hat
"""
import numpy as np
import re
import spacy  # For preprocessing
import multiprocessing

from sklearn.feature_extraction.text import TfidfVectorizer


class Preprocessing:
    def __init__(self, dataset):
        self.dataset = dataset     
        self.word_features = []
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
        return self.dataset


    def feature_extraction(self,ngram_range, max_df,min_df,max_features):
        vectorizer = TfidfVectorizer(ngram_range=ngram_range, max_df=max_df, min_df=min_df, max_features=max_features) # 4-gram and limit to amount the features
        X = vectorizer.fit_transform(self.dataset.clean.values).toarray()
        self.word_features = vectorizer.get_feature_names() # Extract or get the list words features
        
        vecs_label = self.dataset['label'].values
        #vecs_id_tweet = self.dataset['id_tweet'].values
        vecs_dataset = self.dataset['dataset'].values
        
        #vecs_id_tweet = vecs_id_tweet.reshape(vecs_id_tweet.shape[0],1)
        vecs_dataset = vecs_dataset.reshape(vecs_dataset.shape[0],1)
        vecs_label = vecs_label.reshape(vecs_label.shape[0],1)
        #vecs = np.concatenate((vecs_id_tweet,vecs_label,X),axis=1)
        #vecs = np.concatenate((vecs_label,X),axis=1)
        vecs = np.concatenate((vecs_dataset,vecs_label,X),axis=1)
        
        return vecs, vectorizer
    
        
    
    def getDataset(self):
        return self.dataset
    
    def getWordFeatures(self):
        return self.word_features