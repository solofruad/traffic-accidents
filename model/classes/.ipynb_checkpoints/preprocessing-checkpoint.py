#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 21 11:51:41 2019

@author: hat
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 20:39:00 2019

@author: hat
"""
import spacy  # For preprocessing
import re
from nltk.stem import SnowballStemmer
import multiprocessing

stemmer = SnowballStemmer('spanish')


class Preprocessing:
    def __init__(self, dataset):
        self.dataset = dataset
        self.cores = multiprocessing.cpu_count() # Count the number of cores in a computer
        
    """ 1 """        
    def cleaning_stem_stopwords(self, doc):
        # Stemming and removes stopwords    
        #txt = [token.lemma_ for token in doc if not token.is_stop]    
        txt = [stemmer.stem(token.text) for token in doc if not token.is_stop]    
        if len(txt) > 2:
            return ' '.join(txt)
    """ 2 """    
    def cleaning_lemma_stopwords(self, doc):
        # Lemma and removes stopwords        
        txt = [(token.lemma_ if token.text != 'calle' else token.text) for token in doc if not token.is_stop]        
        if len(txt) > 2:
            return ' '.join(txt)
    """ 3 """
    def cleaning_stopwords(self, doc):
        # Only removing stopwords        
        txt = [token.text for token in doc if not token.is_stop]    
        if len(txt) > 2:
            return ' '.join(txt)
    """ 4 """
    def cleaning_special_chars(self, doc):
        #All characteres, without @, urls, # and numbers.        
        txt = [token.text for token in doc]    
        if len(txt) > 2:
            return ' '.join(txt)
    """ 5 """
    def cleaning_stem(self, doc):
        #Stem without removes stopwords
        txt = [stemmer.stem(token.text) for token in doc]    
        if len(txt) > 2:
            return ' '.join(txt)
    """ 6 """
    def cleaning_lemma(self, doc):
        #Lemma without removes stopwords
        txt = [(token.lemma_ if token.text != 'calle' else token.text) for token in doc]    
        if len(txt) > 2:
            return ' '.join(txt)

    
    def fit_clean(self, proposal):
        nlp = spacy.load("es_core_news_md",disabled=['ner','parser']) # disabling Named Entity Recognition for speed
        nlp.vocab["rt"].is_stop = True #Add RT to Stopwords

        brief_cleaning = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in self.dataset['text'])
        
        if proposal == 1:
            clean_fn = self.cleaning_stem_stopwords
        elif proposal == 2:
            clean_fn = self.cleaning_lemma_stopwords
        elif proposal == 3:
            clean_fn = self.cleaning_stopwords
        elif proposal == 4:
            clean_fn = self.cleaning_special_chars
        elif proposal == 5:
            clean_fn = self.cleaning_stem
        elif proposal == 6:
            clean_fn = self.cleaning_lemma
        else:
            print("Error: ("+str(proposal)+") No es una opción válida")
            exit()
            
        
        txt = [clean_fn(doc) for doc in nlp.pipe(brief_cleaning, batch_size=50, n_threads=self.cores)]    
        self.dataset['clean'] = txt
        self.dataset = self.dataset[~self.dataset['clean'].isnull()] #Elimina publicaciones que estan null al eliminarlo porque no generan valor en el proceso de limpieza
        self.dataset = self.dataset.reset_index(drop=True) # if limited the amount tweets drop index so that it does not interfere later in te for_each         

    
    def getCores(self):
        return self.cores
    
    def getDataset(self):
        return self.dataset