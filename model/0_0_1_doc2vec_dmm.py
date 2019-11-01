#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 09:30:35 2019

@author: hat
"""

"""
   DOC2VEC distribuides memory DDM
"""

import re  # For preprocessing
import pandas as pd  # For data handling
from time import time  # To time our operations
from collections import defaultdict  # For word frequency

import spacy  # For preprocessing
#!pip3 install -U spacy
#!python3 -m spacy download es_core_news_md


import logging  # Setting up the loggings to monitor gensim
#logging.basicConfig(format="%(levelname)s - %(asctime)s: %(message)s", datefmt= '%H:%M:%S', level=logging.INFO)


logger = logging.getLogger("doc2vec")
hdlr = logging.FileHandler("log/logs.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

try:
    logger.info("#####Comenzando a entrenar modelo######")    
    logger.info("Leyendo archivo")    
    dataset = pd.read_csv("5-corpus-union-unique-clean.tsv",delimiter= "\t", quoting = 3)        
    logger.info("dataset cargado")    

    #Bigrams:
    from gensim.models.phrases import Phrases, Phraser

    unigram = [row.split() for row in dataset['text']]
    bigram = Phrases(unigram, min_count=5, progress_per=10000)
    trigram = Phrases(bigram[unigram], min_count=5, progress_per=10000)
    
    sentences = trigram[bigram[unigram]]

    #Gensim Doc2Vec Implementation

    import multiprocessing
    from gensim.models.doc2vec import Doc2Vec, TaggedDocument

    cores = multiprocessing.cpu_count() # Count the number of cores in a computer

    logger.info("Creando documentos para doc2vec")
    tagged_data = [TaggedDocument(words=_d, tags=[str(i)]) for i, _d in enumerate(sentences)]

    max_epochs = 100
    vec_size = 200
    alpha = 0.025
    min_alpha = 0.0001

    #DMM + Trigram
    logger.info("Creando objeto del modelo doc2vec")
    model = Doc2Vec(vector_size=vec_size,
                    window=5,
                    alpha=alpha, 
                    min_alpha=min_alpha,
                    min_count=5,
                    dm=1, #dm = 1 is "distribuides memory (no-order words)), if dm = 0 is "DBOW" (order words))
                    dm_mean=1,
                    epochs=40,
                    workers=cores,
                    seed=123) 
      

    logger.info("Comenzando a contruir vocab")
    t = time()
    model.build_vocab(tagged_data)    
    logger.info('Time to build vocab: {} mins'.format(round((time() - t) / 60, 2)))

    logger.info("Comenzando a entrenar")
    t = time()
    for epoch in range(max_epochs):        
        logger.info('iteration {0}'.format(epoch))
        model.train(tagged_data,
                    total_examples=model.corpus_count,
                    epochs=model.iter)
        # decrease the learning rate
        model.alpha -= 0.0002
        # fix the learning rate, no decay
        model.min_alpha = model.alpha

    logger.info('Time to train model doc2vec: {} mins'.format(round((time() - t) / 60, 2)))

    model.save("5-d2v-dmm-trig-f200-w5.model")    
    logger.info("Model Saved file: 5-d2v-dmm-trig-f200-w5.model")

except Exception as e:
    logger.error('Unhandled exception:')
    logger.error(e)



