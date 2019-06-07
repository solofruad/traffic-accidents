#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 19:37:32 2019

@author: hat
"""

import pandas as pd  # For data handling
import numpy as np

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn import metrics

from gensim.models.doc2vec import Doc2Vec
from gensim.models.phrases import Phrases, Phraser

import multiprocessing
CORES = multiprocessing.cpu_count() # Count the number of cores in a computer

positive_part1 = pd.read_csv("data/subclusters/positive_part1.tsv", delimiter = "\t", quoting = 3)
positive_part1 = positive_part1[['id_tweet','created_at','user_name','text','clean']]

negative_part1 = pd.read_csv("data/subclusters/negative_part1.tsv", delimiter = "\t", quoting = 3)
negative_part1 = negative_part1[['id_tweet','created_at','user_name','text','clean']]

positive_by_username = positive_part1['user_name'].value_counts() # Show distribution of tweets by user
negative_by_username = negative_part1['user_name'].value_counts() # Show distribution of tweets by user

#positive_part2 = positive_part1.drop_duplicates(['clean'],keep='first')

phraser_tg = Phraser.load("model/phraser_trigram-all-data.model")

dmm = Doc2Vec.load("model/dmm/5-d2v-dmm-trig-f200-w5.model")
dbow = Doc2Vec.load("model/dbow/5-d2v-dbow-unigram-f200-w5.model")

vecs_id_tweet = np.zeros((len(positive_part1.clean.values),1))
vecs_dbow = np.zeros((len(positive_part1.clean.values), 200))
vecs_dmm = np.zeros((len(positive_part1.clean.values), 200))
vecs = np.zeros((len(positive_part1.clean.values), 401))
n = 0    
for row in positive_part1.values:
    vecs_id_tweet[n] = row[0]
    vecs_dbow[n] = dbow.infer_vector(row[4].split())        
    vecs_dmm[n] = dmm.infer_vector(phraser_tg[row[4].split()])
    vecs[n] = np.concatenate((vecs_id_tweet[n],vecs_dbow[n],vecs_dmm[n]))
    n=n+1
    if(n%10000 == 0):
        print(n)
        
kmeans = KMeans(n_clusters = 15, n_init = 100, n_jobs = -1, max_iter=300,random_state=1234,verbose=1) # n_init is the amount of times that select the centroid and take an average
X = kmeans.fit(vecs[:,1:])
labels=kmeans.labels_.tolist()

positive_part1['cluster'] = kmeans.labels_

l = kmeans.labels_
pca = PCA(n_components=2).fit(vecs[:,1:])
datapoint = pca.transform(vecs[:,1:])

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

color = [label1[i] for i in labels]
plt.scatter(datapoint[:, 0], datapoint[:, 1], alpha=0.7, c=color)



centroids = kmeans.cluster_centers_
centroidpoint = pca.transform(centroids)
plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')
plt.show()



positive_bogotatransito = positive_part1[positive_part1["user_name"] == "BogotaTransito"]
positive_without = positive_part1[positive_part1["user_name"] != "BogotaTransito"]

positive_by_cluster = positive_bogotatransito['cluster'].value_counts() # Show distribution of tweets by user



positive_bogotatransito_part1 = positive_bogotatransito[positive_bogotatransito["sub"]==1]
positive_bogotatransito_part2 = positive_bogotatransito[positive_bogotatransito["sub"]==0]

positive_bogotatransito_part2_a = positive_bogotatransito_part2_a.drop_duplicates(['clean'],keep='first')
positive_bogotatransito_part2_b = positive_bogotatransito_part2_a.sample(n=522) # Use only to limit the number of tweet samples or the population, to avoid computational overload, parameter n = populate

positive_part2 = pd.concat([positive_without, positive_bogotatransito_part1])

positive_bogotatransito_part2_c = positive_bogotatransito_part2_a[positive_bogotatransito_part2_a["sub"]==1]
positive_bogotatransito_part2_d = positive_bogotatransito_part2_a[positive_bogotatransito_part2_a["sub"]==0]
positive_bogotatransito_part2_e = positive_bogotatransito_part2_d.sample(n=428) # Use only to limit the number of tweet samples or the population, to avoid computational overload, parameter n = populate

positive_part2 = pd.concat([positive_part2, positive_bogotatransito_part2_e])
positive_part2 = positive_part2[['id_tweet','created_at','user_name','text','clean']]
positive_part2.to_csv("data/subclusters/positive_part2.tsv",sep='\t')




negative_part1b = negative_part1[negative_part1["user_name"]== "BogotaTransito"]
negative_part1b["sub"] = 0

negative_part2 = negative_part1.sample(n=800) # Use only to limit the number of tweet samples or the population, to avoid computational overload, parameter n = populate
negative_part2["sub"] = 0
negative_part2_by_username = negative_part2['user_name'].value_counts() # Show distribution of tweets by user


negative_part3 = negative_part2[negative_part2["sub"]==0]

negative_part4 = pd.read_csv("data/4_stream_bogota.tsv", delimiter = "\t", quoting = 3)
negative_part4 = negative_part4[['id_tweet','created_at','user_name','text']]


negative_part5 = negative_part4.sample(n=1500)
negative_part5["sub"] = 0

negative_part5 = negative_part5[['id_tweet','created_at','user_name','text']]
negative_part3 = negative_part3[['id_tweet','created_at','user_name','text']]
negative_part6 = pd.concat([negative_part3, negative_part5])
negative_part6.to_csv("data/subclusters/ok_negative_part2.tsv",sep='\t')
negative_part6a = pd.read_csv("data/subclusters/ok_negative_part2.tsv", delimiter = "\t", quoting = 3)

positive_part6a = pd.read_csv("data/subclusters/ok_positive_part2.tsv", delimiter = "\t", quoting = 3)