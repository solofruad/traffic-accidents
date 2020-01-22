#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TF IDF

Created on Thu Jul 25 20:39:00 2019

@author: hat
"""
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer
from classes.preprocessing import Preprocessing as Base


class Preprocessing(Base):
    def __init__(self, dataset):        
        Base.__init__(self,dataset)
        #self.cores = multiprocessing.cpu_count() # Count the number of cores in a computer            
    
    """/def fit_clean(self):
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
    """
    def feature_extraction(self,ngram_range, max_df,min_df,max_features):
        vectorizer = TfidfVectorizer(ngram_range=ngram_range, max_df=max_df, min_df=min_df, max_features=max_features) # 4-gram and limit to amount the features
        X = vectorizer.fit_transform(self.dataset.clean.values).toarray()
        self.word_features = vectorizer.get_feature_names() # Extract or get the list words features
        
        vecs_label = self.dataset['label'].values
        #vecs_id_tweet = self.dataset['id_tweet'].values
        #vecs_dataset = self.dataset['dataset'].values
        
        #vecs_id_tweet = vecs_id_tweet.reshape(vecs_id_tweet.shape[0],1)
        #vecs_dataset = vecs_dataset.reshape(vecs_dataset.shape[0],1)
        vecs_label = vecs_label.reshape(vecs_label.shape[0],1)
        #vecs = np.concatenate((vecs_id_tweet,vecs_label,X),axis=1)
        #vecs = np.concatenate((vecs_label,X),axis=1)
        vecs = np.concatenate((vecs_label,X),axis=1)
        
        return vecs, vectorizer
    
        
    
    def getDataset(self):
        return self.dataset
    
    def getWordFeatures(self):
        return self.word_features
