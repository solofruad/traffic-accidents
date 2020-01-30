#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 28 09:30:35 2019

@author: hat
"""

"""
   DOC2VEC distribuides memory DDM
"""

#import re  # For preprocessing
import pandas as pd  # For data handling
from time import time  # To time our operations
#from collections import defaultdict  # For word frequency

#import spacy  # For preprocessing
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
    logger.info("#####Comenzando a entrenar modelo DMM######")    
    logger.info("Leyendo archivo")    
    __dir = "data/v1/doc2vec/clean/"
    __file = "6_clean_lemma_dataset_propuesta1_5050"
    dataset = pd.read_csv(__dir + __file + ".tsv", delimiter= "\t", quoting = 3)
    del dataset["Unnamed: 0"]
    logger.info("dataset cargado")    

    #Bigrams:
    from gensim.models.phrases import Phrases, Phraser

    unigram = [row.split() for row in dataset['text']]
    bigram = Phrases(unigram, min_count=5, progress_per=10000)
    trigram = Phrases(bigram[unigram], min_count=5, progress_per=10000)
    trigram.save("data/v1/doc2vec/model_dmm/trigram/tigram_"+__file+".model")
    sentences = trigram[bigram[unigram]]

    #Gensim Doc2Vec Implementation

    import multiprocessing
    from gensim.models.doc2vec import Doc2Vec, TaggedDocument

    cores = multiprocessing.cpu_count() # Count the number of cores in a computer

    logger.info("Creando documentos para doc2vec")
    tagged_data = [TaggedDocument(words=_d, tags=[str(i)]) for i, _d in enumerate(sentences)]

    max_epochs = 30
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
                    epochs=24,
                    workers=cores,
                    seed=123) 
      

    logger.info("Comenzando a construir vocab")
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

    __dir_save = "data/v1/doc2vec/model_dmm/"
    model.save(__dir_save+__file+".model")    
    logger.info("Model Saved file: "+__file+".model")    
    logger.info("###Finalizando entrenamiento de modelo DMM###")
    logger.info(" ")

except Exception as e:
    logger.error('Unhandled exception:')
    logger.error(e)


