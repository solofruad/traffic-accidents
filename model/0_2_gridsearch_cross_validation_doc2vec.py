#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Oct  7 22:42:27 2019

@author: hat
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd  # For data handling


from classes.doc2vec.preprocessing import Preprocessing as doc2vec

"""-------------------------------DATASETS-----------------------------------------------"""

train = pd.read_csv("data/v1/7030/train70.tsv", delimiter = "\t", quoting = 3)
train['dataset'] = 99 # train = 1
test = pd.read_csv("data/v1/7030/test30.tsv", delimiter = "\t", quoting = 3)
test['dataset'] = 100 # test = 0
dataset = pd.concat([train,test])
dataset = dataset.reset_index(drop=True)

"""-------------------------------PREPROCESSING-----------------------------------------------"""

clean = doc2vec(dataset)

directory = "data/v1/doc2vec/"
file = "4_clean_special_chars_dataset_propuesta1_5050"
clean.fit_clean(4)

#embendding = clean.feature_extraction(200,200,402, directory, file)
embendding = clean.feature_extraction(200,200,202, directory, file)

"""-------------------------------TRAIN & TEST-----------------------------------------------"""
vecs_train = embendding[embendding[:,0] == 99.0,:]
vecs_test = embendding[embendding[:,0] == 100.0,:]

X_train = vecs_train[:,2:]
y_train = vecs_train[:,1]
X_test = vecs_test[:,2:]
y_test = vecs_test[:,1]

"""----------------------------------GRID SEARCH---------------------------------------------------"""
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn.svm import SVC
from sklearn.metrics import classification_report
from pprint import pprint
from time import time

import logging  # Setting up the loggings to monitor gensim

logger = logging.getLogger("gridsearch")
hdlr = logging.FileHandler("log/gridsearch_doc2vec.log")
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)

try:
    logger.info("#####Comenzando a entrenar modelo######")    
    logger.info(__doc__)
    pipeline = Pipeline([      
      ('clf', SVC(random_state=123) )
    ])
    parameters = {          
            'clf__kernel': ('linear', 'poly', 'rbf'),              
            'clf__C': (0.01, 0.05, 0.1, 1, 2, 3, 4, 5, 6, 7, 8),
            'clf__gamma': (0.01, 0.05, 0.1, 0.2, 0.3, 0.4, 0.7, 1, 2, 3,10)            
    }
    """
    parameters = {          
            'clf__kernel': ('poly', 'rbf'),              
            'clf__C': (5, 6),
            'clf__gamma': (0.1, 0.2, 0.3, 0.4)            
    }
    """
    scores = ['accuracy', 'f1']    
    for score in scores:
        logger.info("# Tuning hyper-parameters for %s" % score)
        logger.info(" ")
    
        logger.info("Performing grid search...")
        print("pipeline:", [name for name, _ in pipeline.steps])
        logger.info("parameters:")
        pprint(parameters)
        t0 = time()
        grid_search = GridSearchCV(pipeline, parameters, cv=5, scoring=score, n_jobs=-1,verbose=1)
        grid_search.fit(X_train, y_train)
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


"""----------------------------------NAIVE BAYES---------------------------------------------------"""

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB

classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

cm_nb = confusion_matrix(y_test, y_pred)

metrics_nb = []
metrics = {}
metrics['accuracy'] = accuracy_score(y_test, y_pred)
metrics['recall'] = recall_score(y_test, y_pred)
metrics['precision'] = precision_score(y_test, y_pred)
metrics['f1'] = f1_score(y_test, y_pred)
metrics_nb.append(metrics)
metrics_nb = pd.DataFrame(metrics_nb)

"""----------------------------------LINEAR SVM---------------------------------------------------"""

#from sklearn.svm import LinearSVC
#classifier = LinearSVC(random_state=0, tol=1e-4)

from sklearn.svm import SVC
classifier = SVC(random_state=123, kernel='rbf', gamma=0.05, C=5)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

cm_svm = confusion_matrix(y_test, y_pred)

metrics_svm = []
metrics = {}
metrics['accuracy'] = accuracy_score(y_test, y_pred)
metrics['recall'] = recall_score(y_test, y_pred)
metrics['precision'] = precision_score(y_test, y_pred)
metrics['f1'] = f1_score(y_test, y_pred)
metrics_svm.append(metrics)
metrics_svm = pd.DataFrame(metrics_svm)

"""----------------------------------Graficando---------------------------------------------------"""
"""
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

pca = PCA(n_components=2).fit(X)
datapoint = pca.transform(X)

plt.figure

label1 = ["#32C12C", #0. GREEN
          "#009888", #1. TEAL
          "#3E49BB", #2. INDIGO
          "#526EFF",#3. AZUL
          "#7F4FC9", #4. purple
          "#FFEF00", #5. YELOW
          "#FF9A00", #6. ORANGE
          "#7C5547", #7. BROWN
          "#5F7D8E", #8. BLUE GREY
          "#FF5500", #9. DEEP ORANGE
          "#87C735", #10. LIGHT GREEN
          "#CDE000", #11. LIME
          "#00A5F9", #12. LIGHT BLUE
          "#00BCD9",  #13. CYAN
          "#682CBF"] #14. DEEP PURPLE          

color = [label1[int(i)] for i in y]
plt.scatter(datapoint[:, 0], datapoint[:, 1], alpha=0.7, c=color)

plt.show()
"""