#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

import spacy  # For preprocessing
import re
import multiprocessing
from classes.wordsegmentation import WordSegmentation


class NerPreprocessing(BaseEstimator, TransformerMixin):
    
    def __init__(self, spacy_model, corpus_segmentation, njobs):
        self.spacy_model = spacy_model
        self.njobs = multiprocessing.cpu_count() if njobs ==-1  else njobs        
        self.seg = WordSegmentation(corpus_segmentation)

        
    def word_segmentation(self, pattern, text):
        search = re.search(pattern,text)
        while search:    
            s = search.start()
            e = search.end()                
            text = text[:s] + ' ' + ' '.join(self.seg.segment(text[s+1:e])) +' '+ text[e:]        
            search = re.search(pattern,text)        
        return text
        
    def clean_fn(self, text):        
        # Username segmentation
        pattern = "(@[A-Za-z0-9äÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ_]+)"
        text = self.word_segmentation(pattern,text)
        # Hashtag segmentation
        pattern = "(#[A-Za-z0-9äÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ_]+)"
        text = self.word_segmentation(pattern,text)
        return text
        
    def preText(self, text):        
        pre = re.sub("&[A-Za-z]+;", ' ', text) #Eliminar códigos ASCII
        pre = re.sub("(\w+:\/\/\S+)",' ',pre) #Eliminar links http y https
        pre = re.sub("([^A-Za-z0-9äÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ,;.:*\-\[\]¿?¡!\"\"()_'/])",' ',pre) #Eliminar caracteres especiales como emoticones, exceptuando los signos de puntuación y tildes.
        pre = re.sub(r'([;.:\-\[\]¿?¡!#\"()]){3,}',r'\1\1',pre) #Si repite un caracters especial más de 3 veces ej. """"
        pre = re.sub(r'([a-zA-Z])\1{2,}',r'\1\1',pre) #Si repite una letra más de dos veces las reduce a dos repeticiones goool => gool        
        pre = re.sub(r'(\s){2,}',r' ',pre) #Eliminar espacios seguidos              
        return pre.strip()
    
             
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
        nlp = spacy.load(self.spacy_model,disabled=['ner','parser']) # disabling Named Entity Recognition for speed
        

        brief_cleaning = (self.clean_fn(str(row)) for row in X)        
                            
        txt = [self.preText(doc.text) for doc in nlp.pipe(brief_cleaning, batch_size=50, n_threads=self.njobs)]
        #del nlp
        
        return txt
    
    


