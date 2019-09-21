#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 20:39:00 2019

@author: hat
"""
import numpy as np
import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer


class Preprocessing:
    def __init__(self, dataset):
        self.dataset = dataset     
        self.word_features = []
        
    def fit_clean(self):
        stoplist = stopwords.words('spanish') # Create list the stopwords
        stoplist.extend(['rt']) # Add to list the stopwords for clean token RT
        corpus = [] # Array with clenased tweets 
            
        # Loop for clean tweets        
        for index, row in self.dataset.iterrows():                
            # Clean tweets of links, username mentions, emoticons, others specials characters, numbers, split Hashtags
            review = re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",' ', row["text"])
        
            # Changes tweets to lowercase
            review = review.lower()
            
            # First eliminate the stopwords, then apply the SnowballStemmer
            review = review.split()    
            stem = SnowballStemmer('spanish')
            review = [stem.stem(word) for word in review if not word in set(stoplist)]
            review = ' '.join(review) #Concatenate all in one text
            
            # Add each tweet to array
            corpus.append(review)                
        
        self.dataset["clean"] = corpus

    def feature_extraction(self,ngram_range, max_df,min_df,max_features):
        vectorizer = TfidfVectorizer(ngram_range=ngram_range, max_df=max_df, min_df=min_df, max_features=max_features) # 4-gram and limit to amount the features
        X = vectorizer.fit_transform(self.dataset.clean.values).toarray()
        self.word_features = vectorizer.get_feature_names() # Extract or get the list words features
        
        vecs_label = self.dataset['label'].values
        vecs_id_tweet = self.dataset['id_tweet'].values

        vecs_id_tweet = vecs_id_tweet.reshape(vecs_id_tweet.shape[0],1)
        vecs_label = vecs_label.reshape(vecs_label.shape[0],1)
        vecs = np.concatenate((vecs_id_tweet,vecs_label,X),axis=1)
        
        return vecs
    
        
    
    def getDataset(self):
        return self.dataset
    
    def getWordFeatures(self):
        return self.word_features