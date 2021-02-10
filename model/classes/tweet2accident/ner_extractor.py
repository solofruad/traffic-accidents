#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 27 15:08:56 2021

@author: hat
"""

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

import pandas as pd
import spacy
import multiprocessing


class NerExtractor(BaseEstimator, TransformerMixin):
    
    def __init__(self, spacy_model, njobs):
        self.spacy_model = spacy_model
        self.njobs = multiprocessing.cpu_count() if njobs ==-1  else njobs
        

    def get_entities(self, ents):
        entities = []
        entity = ''
        tokens = []
        for e in range(len(ents)):
            token = ents[e][0]
            ner = ents[e][1]
            ner_iob = ner.split("-")[0]
            ner_text = ner.split("-")[1] 
        
            if (ner_iob == 'B' and len(tokens) > 0):        
                t = ' '.join(tokens)
                entities.append((t,entity))
                tokens = []
        
            entity = ner_text        
            tokens.append(token)
            if e == len(ents)-1:
                t = ' '.join(tokens)
                entities.append((t,entity))
        
        
        return entities
    
    def extractor_fn(self, doc):
        ents = [(e.text, e.label_) for e in doc.ents]
        return self.get_entities(ents)
    
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        nlp = spacy.load(self.spacy_model)    
        ner = [ self.extractor_fn(doc) for doc in nlp.pipe(X, batch_size=50, n_threads=self.njobs)]                
        return ner



















