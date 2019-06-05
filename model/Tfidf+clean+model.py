#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 07:30:17 2019

@author: hat
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 07:08:23 2019

@author: hat
"""

import pandas as pd  # For data handling
import numpy as np

from sklearn.feature_extraction.text import TfidfVectorizer

#######################################PARTE 1#####################################################

"""-------------------------------DATASETS-----------------------------------------------"""

dataset = pd.read_csv("data/dataset_accident_tweet.tsv", delimiter = "\t", quoting = 3)
dataset = dataset[['id_tweet','created_at','user_name','text','clean','label']]
dataset = dataset.sort_values(by=['created_at'])

"""-------------------------------CLEAN-----------------------------------------------"""

import re
import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer

tweets = dataset["text"]
h = 0 # Only show the progress
corpus = [] # Array with clenased tweets 
stoplist = stopwords.words('spanish') # Create list the stopwords
stoplist.extend(['rt']) # Add to list the stopwords for clean token RT


# Loop for clean tweets
for i in range(0,len(dataset)):       
    review = tweets[i]    
    
    # Clean tweets of links, username mentions, emoticons, others specials characters, numbers, split Hashtags
    review = re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",' ', review)

    # Changes tweets to lowercase
    review = review.lower()
    
    # First eliminate the stopwords, then apply the SnowballStemmer
    review = review.split()    
    stem = SnowballStemmer('spanish')
    review = [stem.stem(word) for word in review if not word in set(stoplist)]
    review = ' '.join(review) #Concatenate all in one text
    
    # Add each tweet to array
    corpus.append(review)    

dataset["clean_tf"] = corpus
"""-------------------------------TF-IDF-----------------------------------------------"""

vectorizer = TfidfVectorizer(ngram_range=(1,3), max_df=0.3, min_df=0.1, max_features=15000) # 4-gram and limit to amount the features
X = vectorizer.fit_transform(dataset.clean_tf.values).toarray()

word_features = vectorizer.get_feature_names() # Extract or get the list words features

"""-------------------------------TRAIN & TEST-----------------------------------------------"""

y = dataset.label.values
# Splitting the dataset into the Training set and Test set
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0)

"""----------------------------------MODEL---------------------------------------------------"""

"""----------------------------------NAIVE BAYES---------------------------------------------------"""

# Fitting Naive Bayes to the Training set
from sklearn.naive_bayes import GaussianNB
classifier = GaussianNB()
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)

from sklearn.metrics import recall_score
recall_score(y_test, y_pred)

from sklearn.metrics import precision_score
precision_score(y_test, y_pred)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred)


"""----------------------------------LINEAR SVM---------------------------------------------------"""

from sklearn.svm import LinearSVC
classifier = LinearSVC(random_state=0, tol=1e-5)
classifier.fit(X_train, y_train)

# Predicting the Test set results
y_pred = classifier.predict(X_test)

# Making the Confusion Matrix
from sklearn.metrics import confusion_matrix
cm = confusion_matrix(y_test, y_pred)

from sklearn.metrics import accuracy_score
accuracy_score(y_test, y_pred)

from sklearn.metrics import recall_score
recall_score(y_test, y_pred)

from sklearn.metrics import precision_score
precision_score(y_test, y_pred)

from sklearn.metrics import f1_score
f1_score(y_test, y_pred)




"""----------------------------------Graficando---------------------------------------------------"""

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

