#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 28 15:31:01 2021

@author: hat
"""
import pandas as pd
import sys
sys.path.insert(0, '../../')

from classes.tweet2accident.ner_preprocessing import NerPreprocessing
from classes.tweet2accident.ner_extractor import NerExtractor

file = 'ner_dataset.tsv'
dir_ = "../../data/v1/NER/"

dataset = pd.read_csv(dir_+file, delimiter = "\t", quoting = 3)


spacy_model = "../../data/v1/NER/spacy_model_complete/"
corpus_segmentation = dir_+'spanish_count_1w_small_v2_twitter.txt'

### Limpieza y normalización para NER
ner_preprocessing = NerPreprocessing(spacy_model=spacy_model, corpus_segmentation=corpus_segmentation,njobs=4)
txt = ner_preprocessing.transform(dataset['text'])
dataset['clean'] = txt

### Predicción etiquetar NER
ner_extractor = NerExtractor(spacy_model=spacy_model, njobs=4)
txt = ner_extractor.transform(dataset['clean'])
dataset['entities'] = txt                    

