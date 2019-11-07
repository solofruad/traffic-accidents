# -*- coding: utf-8 -*-

import numpy as np
import spacy  # For preprocessing
import re
from nltk.stem import SnowballStemmer
import multiprocessing
from gensim.models.doc2vec import Doc2Vec
from gensim.models.phrases import Phrases, Phraser
from sklearn.feature_extraction.text import TfidfVectorizer
stemmer = SnowballStemmer('spanish')


class Preprocessing:
    def __init__(self, dataset):
        self.dataset = dataset
        self.cores = multiprocessing.cpu_count() # Count the number of cores in a computer
        
    def cleaning(self,doc):    
        txt = [token.lemma_ for token in doc if not token.is_stop]    
        if len(txt) > 2:
            return ' '.join(txt)
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

    def feature_extraction_doc2vec(self,size_dbow,size_dmm,size_vec, directory, file):        
        #phraser_tg = Phraser.load(directory+"model_dmm/trigram/trigram_"+file+".model")
        #phraser_tg = Phraser.load("models_v1/phraser_trigram-all-data.model")
        #dmm = Doc2Vec.load(directory+"model_dmm/"+file+".model")
        #print(directory+"model_dmm/"+file+".model")
        dbow = Doc2Vec.load(directory+"model_dbow/"+file+".model")        
        #dbow = Doc2Vec.load("models_v1/dbow/5-d2v-dbow-unigram-f200-w5.model")        
        
        #vecs_id_tweet = np.zeros((len(self.dataset.clean.values),1))
        vecs_dataset = np.zeros((len(self.dataset.clean.values),1))        
        vecs_label = np.zeros((len(self.dataset.clean.values),1))
        vecs_dbow = np.zeros((len(self.dataset.clean.values), size_dbow))
        #vecs_dmm = np.zeros((len(self.dataset.clean.values), size_dmm))
        vecs = np.zeros((len(self.dataset.clean.values), size_vec))        
        
        for index, row in self.dataset.iterrows():                
            vecs_label[index] = row['label']
            #vecs_id_tweet[index] = row['id_tweet']
            vecs_dataset[index] = row['dataset']
            vecs_dbow[index] = dbow.infer_vector(row['clean'].split())        
            #vecs_dmm[index] = dmm.infer_vector(phraser_tg[row['clean'].split()])
            #vecs[index] = np.concatenate((vecs_id_tweet[index],vecs_label[index],vecs_dbow[index],vecs_dmm[index]))            
            #vecs[index] = np.concatenate((vecs_dataset[index],vecs_label[index],vecs_dbow[index],vecs_dmm[index]))            
            vecs[index] = np.concatenate((vecs_dataset[index],vecs_label[index],vecs_dbow[index]))
            
        return vecs
    
    def feature_extraction_tfidf(self,ngram_range, max_df,min_df,max_features):    
        vectorizer = TfidfVectorizer(ngram_range=ngram_range, max_df=max_df, min_df=min_df, max_features=max_features) # 4-gram and limit to amount the features
        X = vectorizer.fit_transform(self.dataset.clean.values).toarray()
        self.word_features = vectorizer.get_feature_names() # Extract or get the list words features
        
        vecs_label = self.dataset['label'].values
        #vecs_id_tweet = self.dataset['id_tweet'].values
        vecs_dataset = self.dataset['dataset'].values
        
        #vecs_id_tweet = vecs_id_tweet.reshape(vecs_id_tweet.shape[0],1)
        vecs_dataset = vecs_dataset.reshape(vecs_dataset.shape[0],1)
        vecs_label = vecs_label.reshape(vecs_label.shape[0],1)
        #vecs = np.concatenate((vecs_id_tweet,vecs_label,X),axis=1)
        #vecs = np.concatenate((vecs_label,X),axis=1)
        vecs = np.concatenate((vecs_dataset,vecs_label,X),axis=1)
        
        return vecs, vectorizer
    
    
    def getCores(self):
        return self.cores
    
    def getDataset(self):
        return self.dataset

