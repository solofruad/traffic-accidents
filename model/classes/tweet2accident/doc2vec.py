#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 12 17:49:28 2020

@author: hat
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 18:31:18 2020

@author: hat
"""
import numpy as np
from gensim.models.doc2vec import Doc2Vec
from gensim.models.phrases import Phraser

from sklearn.base import BaseEstimator
from sklearn.base import TransformerMixin

class Embedding(BaseEstimator, TransformerMixin):
    
    def __init__(self, type_transform, directory, file):
        self.type_transform = type_transform
        self.directory = directory
        self.file = file        
        
    def feature_extraction_dbow(self, X, y, directory, file):        
        dbow = Doc2Vec.load(directory+"model_dbow/"+file+".model")
        
        vecs = np.zeros((len(X), 200))
              
        for i in range(len(X)):            
            vecs[i] = dbow.infer_vector(X[i].split())                                
            
        return vecs
    
    def feature_extraction_dmm(self, X, y, directory, file):        
        
        phraser_tg = Phraser.load(directory+"model_dmm/trigram/trigram_"+file+".model")
        dmm = Doc2Vec.load(directory+"model_dmm/"+file+".model")        
                       
        vecs = np.zeros((len(X), 200))        
        
        for i in range(len(X)):
            vecs[i] = dmm.infer_vector(phraser_tg[X[i].split()])                                    
            
        return vecs        
    
    def feature_extraction(self, X, y, directory, file):           
        phraser_tg = Phraser.load(directory+"model_dmm/trigram/trigram_"+file+".model")
        dmm = Doc2Vec.load(directory+"model_dmm/"+file+".model")
        dbow = Doc2Vec.load(directory+"model_dbow/"+file+".model")        
                
        vecs_dbow = np.zeros((len(self.dataset.clean.values), 200))
        vecs_dmm = np.zeros((len(self.dataset.clean.values), 200))
        vecs = np.zeros((len(self.dataset.clean.values), 402))        
        
        for i in range(len(X)):          
            vecs_dbow[index] = dbow.infer_vector(row['clean'].split())        
            vecs_dmm[index] = dmm.infer_vector(phraser_tg[row['clean'].split()])            
            vecs[index] = np.concatenate((vecs_dbow[index],vecs_dmm[index]))
            
        return vecs
                  
    def fit(self, X, y=None):
        return self
    
    def transform(self, X, y=None):
            
        if self.type_transform == 'dbow':
            fn = self.feature_extraction_dbow
        elif self.type_transform == 'dmm':
            fn = self.feature_extraction_dmm
        elif self.type_transform == 'concat':
            fn = self.feature_extraction        
        else:
            print("Error: ("+str(self.type_transform)+") No es una opción válida")
            exit()
                            
        return fn(X, y, self.directory, self.file)
    
    
