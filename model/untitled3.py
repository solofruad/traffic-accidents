#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 13 16:31:47 2019

@author: hat
"""

import numpy as np
import pandas as pd
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

train = pd.read_csv("data/v1/7030/train70.tsv", delimiter = "\t", quoting = 3)
test = pd.read_csv("data/v1/7030/test30.tsv", delimiter = "\t", quoting = 3)


