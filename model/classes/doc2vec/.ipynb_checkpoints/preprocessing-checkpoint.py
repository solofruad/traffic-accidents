#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DOC2VEC

Created on Thu Jul 25 20:39:00 2019

@author: hat
"""
import numpy as np
from gensim.models.doc2vec import Doc2Vec
from gensim.models.phrases import Phraser
from classes.preprocessing import Preprocessing as Base

class Preprocessing(Base): 
    def __init__(self, dataset):        
        Base.__init__(self,dataset)
        
    def feature_extraction_dbow(self, directory, file):        
        dbow = Doc2Vec.load(directory+"model_dbow/"+file+".model")        
        
        vecs_dataset = np.zeros((len(self.dataset.clean.values),1))        
        vecs_label = np.zeros((len(self.dataset.clean.values),1))
        vecs_dbow = np.zeros((len(self.dataset.clean.values), 200))
        
        vecs = np.zeros((len(self.dataset.clean.values), 202))        
        
        for index, row in self.dataset.iterrows():                
            vecs_label[index] = row['label']        
            vecs_dataset[index] = row['dataset']
            vecs_dbow[index] = dbow.infer_vector(row['clean'].split())                    
            vecs[index] = np.concatenate((vecs_dataset[index],vecs_label[index],vecs_dbow[index]))
            
        return vecs
    
    def feature_extraction_dmm(self, directory, file):        
        phraser_tg = Phraser.load(directory+"model_dmm/trigram/trigram_"+file+".model")
        dmm = Doc2Vec.load(directory+"model_dmm/"+file+".model")        
        
        vecs_dataset = np.zeros((len(self.dataset.clean.values),1))        
        vecs_label = np.zeros((len(self.dataset.clean.values),1))        
        vecs_dmm = np.zeros((len(self.dataset.clean.values), 200))
        vecs = np.zeros((len(self.dataset.clean.values), 202))        
        
        for index, row in self.dataset.iterrows():                
            vecs_label[index] = row['label']        
            vecs_dataset[index] = row['dataset']            
            vecs_dmm[index] = dmm.infer_vector(phraser_tg[row['clean'].split()])                        
            vecs[index] = np.concatenate((vecs_dataset[index],vecs_label[index],vecs_dmm[index]))
            
        return vecs
    
    def feature_extraction(self, directory, file):        
        phraser_tg = Phraser.load(directory+"model_dmm/trigram/trigram_"+file+".model")
        dmm = Doc2Vec.load(directory+"model_dmm/"+file+".model")
        dbow = Doc2Vec.load(directory+"model_dbow/"+file+".model")        
        
        vecs_dataset = np.zeros((len(self.dataset.clean.values),1))        
        vecs_label = np.zeros((len(self.dataset.clean.values),1))
        vecs_dbow = np.zeros((len(self.dataset.clean.values), 200))
        vecs_dmm = np.zeros((len(self.dataset.clean.values), 200))
        vecs = np.zeros((len(self.dataset.clean.values), 402))        
        
        for index, row in self.dataset.iterrows():                
            vecs_label[index] = row['label']        
            vecs_dataset[index] = row['dataset']
            vecs_dbow[index] = dbow.infer_vector(row['clean'].split())        
            vecs_dmm[index] = dmm.infer_vector(phraser_tg[row['clean'].split()])            
            vecs[index] = np.concatenate((vecs_dataset[index],vecs_label[index],vecs_dbow[index],vecs_dmm[index]))
            
        return vecs
    
    
    def getCores(self):
        return self.cores
    
    def getDataset(self):
        return self.dataset
