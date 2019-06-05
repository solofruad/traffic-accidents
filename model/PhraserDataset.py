#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 16:39:25 2019

@author: hat
"""

from gensim.models.phrases import Phrases, Phraser

import pandas as pd  # For data handling

all_data = pd.read_csv("data/corpus-union-unique-clean.tsv", delimiter = "\t", quoting = 3)
all_data = all_data[['text']]

unigram = [row.split() for row in all_data['text']]
bigram = Phrases(unigram, min_count=30, progress_per=10000)
trigram = Phrases(bigram[unigram], min_count=30, progress_per=10000)
phraser_tg = Phraser(trigram)

phraser_tg.save("model/phraser_trigram-all-data.model")
