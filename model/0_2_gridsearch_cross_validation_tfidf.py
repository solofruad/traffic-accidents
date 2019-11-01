#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 16 12:22:11 2019

@author: hat
"""
import pandas as pd  # For data handling

from classes.tfidf.preprocessing import Preprocessing as tfidf
from classes.tfidf.preprocessing_lemma import Preprocessing as tfidf_lemma
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
#from sklearn.svm import LinearSVC
from sklearn.svm import SVC
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics import classification_report

from pprint import pprint
from time import time
import logging  # Setting up the loggings to monitor gensim

logger = logging.getLogger("gridsearch")
hdlr = logging.FileHandler("log/gridsearch_tfidf.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


#aux = X[X['clean'].isnull()]
try:    
    
    logger.info("#####Comenzando a entrenar modelo######")    
    logger.info(__doc__)
    
    train = pd.read_csv("data/v1/7030/train70.tsv", delimiter = "\t", quoting = 3)
    clean = tfidf_lemma(train)
    train = clean.fit_clean()
    
    
    test = pd.read_csv("data/v1/7030/test30.tsv", delimiter = "\t", quoting = 3)
    clean = tfidf_lemma(test)
    test = clean.fit_clean()
    
    logger.info("dataset cargado y limpio")    
    
    X, y = train.clean, train.label
    X_test, y_test = test.clean, test.label
    
    '''pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(ngram_range=(1,2), max_df=0.45, min_df=0.001, max_features=None)),
        ('clf', SVC(random_state=123)),   
    ])'''
    pipeline = Pipeline([
      ('tfidf', TfidfVectorizer(min_df=0.001, max_features=None)),
      #('tfidf', TfidfVectorizer()),
      ('clf', SVC(random_state=123, kernel='rbf')),   
      #('clf', SVC(random_state=123)),   
    ])
    
    
    parameters = {
            'tfidf__ngram_range': ((1,1),(1,2)),
            'tfidf__max_df': (0.3, 0.4, 0.5),
            #'tfidf__min_df': (0.001, 0.01),
            #'tfidf__max_features': (None, 220),    
            'clf__C': (4, 5),
            'clf__gamma': (0.7, 0.8),
            #'clf__C': (1, 1.5, 2, 3, 4, 5, 6),
            #'clf__gamma': (0.3, 0.5, 0.7, 0.8, 1, 2),
            #'clf__kernel': ('rbf', 'linear')
    }
    
    """parameters = {
          'tfidf__ngram_range': ((1,1),(1,2),(1,3),(1,4)),
          'tfidf__max_df': (0.25,0.3, 0.35, 0.4, 0.45, 0.5, 0.6),
          'tfidf__min_df': (0.001,0.01,0.2),
          'tfidf__max_features': (None, 600, 800, 1000, 1200, 1500, 1800, 2000,3000),    
          #'clf__C': (0.9,1,1.2,1.4,1.6,1.8,2,3,4,5),
          #'clf__gamma': (0,6,0.7,0.8,0.9,1,2,3),
          #'clf__kernel': ('linear', 'rbf','poly','sigmoid')
    }"""
    
    
    scores = ['accuracy', 'f1']
    #logger.info("Comenzando tuning")
    for score in scores:
        logger.info("# Tuning hyper-parameters for %s" % score)
        logger.info(" ")
    
        logger.info("Performing grid search...")
        logger.info("pipeline:", [name for name, _ in pipeline.steps])
        logger.info("parameters:")
        pprint(parameters)
        t0 = time()
        grid_search = GridSearchCV(pipeline, parameters, cv=5, scoring=score, n_jobs=-1,verbose=1)
        grid_search.fit(X, y)
        logger.info("done in %0.3fs" % (time() - t0))
        logger.info(" ")
        
        logger.info("Best parameters set found on development set:")
        logger.info(" ")
        logger.info(grid_search.best_params_)
        logger.info(" ")
        ##Old start
        logger.info("--")
        logger.info("Best score: %0.3f" % grid_search.best_score_)    
        logger.info("Best parameters set:")
        best_parameters = grid_search.best_estimator_.get_params()    
        for param_name in sorted(parameters.keys()):
            logger.info("\t%s: %r" % (param_name, best_parameters[param_name]))
        logger.info("--")
        logger.info(" ")
        ##Old end
        
        logger.info("Grid scores on development set:")
        logger.info(" ")
        means = grid_search.cv_results_['mean_test_score']
        stds = grid_search.cv_results_['std_test_score']
        for mean, std, params in sorted(zip(means, stds, grid_search.cv_results_['params']),key = lambda t: t[0],reverse=True):
            logger.info("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))
        logger.info(" ")
    
        logger.info("Detailed classification report:")
        logger.info(" ")
        logger.info("The model is trained on the full development set.")
        logger.info("The scores are computed on the full evaluation set.")
        logger.info(" ")
        y_true, y_pred = y_test, grid_search.predict(X_test)
        logger.info(classification_report(y_true, y_pred))
        logger.info(" ")
    
except Exception as e:
    logger.error('Unhandled exception:')
    logger.error(e)
    
    
