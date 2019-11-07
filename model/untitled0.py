#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov  3 22:04:46 2019

@author: hat
"""

from gensim.models.doc2vec import Doc2Vec
from gensim.models.phrases import Phrases, Phraser

directory = "data/v1/doc2vec/"
file = "2_clean_lemma_stopwords_dataset_propuesta1_5050"

dbow = Doc2Vec.load(directory+"model_dmm/"+file+".model")