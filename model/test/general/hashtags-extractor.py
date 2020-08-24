#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 28 20:44:35 2020

@author: hat
"""

import pandas as pd
import re
import random

def extractor(filename):

    df = pd.read_csv(filename, delimiter='\t', quoting = 3)
    
    text = df[['text']]
    
    words = []
    for i in range(len(text)):
        txt = text.iloc[i][0]
    
        for j in re.findall('([@#][A-Za-z0-9_]+)',txt):
            words.append(re.sub('[@#]','',j).lower())
    
    words = sorted(list(set(words)))
    
    return words


f = 'ner_dataset.tsv'
words = extractor(f)

f = '../../data/database/1_server_bogota.tsv'
words_bogota = extractor(f)
random.shuffle(words_bogota)

sub = words_bogota[:400]


final = list(set(words+sub))

df = pd.DataFrame(final)
df.to_csv('word_segmentation.csv')
