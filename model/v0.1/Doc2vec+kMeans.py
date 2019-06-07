#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 15:08:22 2019

@author: hat
"""

import pandas as pd  # For data handling
import numpy as np
import spacy  # For preprocessing
import re
import multiprocessing

from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from scipy.spatial.distance import cdist
from sklearn import metrics

from gensim.models.doc2vec import Doc2Vec
from gensim.models.phrases import Phrases, Phraser


CORES = multiprocessing.cpu_count() # Count the number of cores in a computer
FNAME = "1_search.tsv"

def cleaning(doc):    
    txt = [token.lemma_ for token in doc if not token.is_stop]    
    if len(txt) > 4:
        return ' '.join(txt)


#######################################PARTE 1#####################################################

"""-------------------------------DATASETS-----------------------------------------------"""

filename = "data/"+FNAME
dataset = pd.read_csv(filename, delimiter = "\t", quoting = 3)
dataset = dataset[['id_tweet','created_at','user_name','text']]

"""-------------------------------LIMPIEZA-----------------------------------------------"""

#dataset = pd.read_csv("data/clean/"+FNAME, delimiter = "\t", quoting = 3)
#del dataset["Unnamed: 0"]

nlp = spacy.load("es_core_news_md",disabled=['ner','parser']) # disabling Named Entity Recognition for speed
nlp.vocab["rt"].is_stop = True #Add RT to Stopwords

brief_cleaning = (re.sub("(@[A-Za-z0-9]+)|((?<=[A-Za-z])(?=[A-Z][a-z]))|([^A-Za-zäÄëËïÏöÖüÜáéíóúáéíóúÁÉÍÓÚÂÊÎÔÛâêîôûàèìòùÀÈÌÒÙñÑ])|(\w+:\/\/\S+)",
                             ' ', str(row)).lower() for row in dataset['text'])

txt = [cleaning(doc) for doc in nlp.pipe(brief_cleaning, batch_size=5000, n_threads=CORES)]
dataset['clean'] = txt
dataset = dataset[~dataset['clean'].isnull()] #Elimina publicaciones que estan null al eliminarlo porque no generan valor en el proceso de limpieza
dataset = dataset.reset_index(drop=True) # if limited the amount tweets drop index so that it does not interfere later in te for_each 
dataset.to_csv("data/clean/"+FNAME,sep='\t')

"""-------------------------------DOC2VEC-----------------------------------------------"""

#vecs = pd.read_csv("vector/vec-"+FNAME, delimiter = "\t", quoting = 3)
#del vecs["Unnamed: 0"]
#vecs = vecs.values

phraser_tg = Phraser.load("model/phraser_trigram-all-data.model")

dmm = Doc2Vec.load("model/dmm/5-d2v-dmm-trig-f200-w5.model")
dbow = Doc2Vec.load("model/dbow/5-d2v-dbow-unigram-f200-w5.model")

vecs_id_tweet = np.zeros((len(dataset.clean.values),1))
vecs_dbow = np.zeros((len(dataset.clean.values), 200))
vecs_dmm = np.zeros((len(dataset.clean.values), 200))
vecs = np.zeros((len(dataset.clean.values), 401))
n = 0    
for row in dataset.values:
    vecs_id_tweet[n] = row[0]
    vecs_dbow[n] = dbow.infer_vector(row[4].split())        
    vecs_dmm[n] = dmm.infer_vector(phraser_tg[row[4].split()])
    vecs[n] = np.concatenate((vecs_id_tweet[n],vecs_dbow[n],vecs_dmm[n]))
    n=n+1
    if(n%10000 == 0):
        print(n)

columns = np.arange(401)

vectors = pd.DataFrame(vecs,columns=columns)
vectors.to_csv("vector/vec-"+FNAME,sep='\t')


#######################################PARTE 2#####################################################

"""-------------------------------AGRUPACIÓN-----------------------------------------------"""

"""
    AGRUPACIÓN CON KMEANS:
        n_cluster = Número de cluster
        n_init = Cantidad de veces que selecciona un centroide y se toma un promedio
        n_jobs = Número de procesos en paralelo (-1 significa que use todo los procesadores)
        random_state = semilla
        verbose = Ver proceso en consola
        max_iter = Número máxico de iteraciones para una ejecución
"""
kmeans = KMeans(n_clusters = 8, n_init = 100, n_jobs = -1, max_iter=300,random_state=1234,verbose=1) # n_init is the amount of times that select the centroid and take an average
X = kmeans.fit(vecs[:,1:])
labels=kmeans.labels_.tolist()

dataset['cluster'] = kmeans.labels_
dataset.to_csv("data/clean/v2"+FNAME,sep='\t')

#dataset = pd.read_csv("data/clean/v2"+FNAME, delimiter = "\t", quoting = 3)
#del dataset["Unnamed: 0"]
#inertia = kmeans.inertia_
#distortion = sum(np.min(cdist(vecs,kmeans.cluster_centers_,'euclidean'),axis=1)) / vecs.shape[0]
#metrics.silhouette_score(vecs, kmeans.labels_, metric="euclidean")


"""-------------------------------GRAFICANDO-----------------------------------------------"""

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

import seaborn as sns

# Plot cluster
clusters = dataset.groupby(['cluster', 'user_name']).size()
fig2, ax2 = plt.subplots(figsize = (30, 15))
sns.heatmap(clusters.unstack(level = 'user_name'), ax = ax2, cmap = 'Reds')

ax2.set_xlabel('user_name', fontdict = {'weight': 'bold', 'size': 24})
ax2.set_ylabel('cluster', fontdict = {'weight': 'bold', 'size': 24})
for label in ax2.get_xticklabels():
    label.set_size(16)
    label.set_weight("bold")
for label in ax2.get_yticklabels():
    label.set_size(16)
    label.set_weight("bold")
    
plt.show()

#######################################PARTE 3#####################################################

"""-------------------------------SUBAGRUPACIÓN-----------------------------------------------"""

cluster = dataset[dataset['cluster']==7]
cluster = cluster.reset_index(drop=True) # if limited the amount tweets drop index so that it does not interfere later in te for_each 

cluster_vecs = np.zeros((len(cluster.id_tweet.values),401))

n = 0
for row in cluster.values:
    cluster_vecs[n] = vecs[np.where(vecs[:,0] == row[0]),:]
    n=n+1

"""cluster.iloc[1000,0]
cluster_vecs[1000,0]
np.where(vecs[:,0] == 1073614713278353408)
vecs[23489,0]
#vecs[10843]
#cluster_vecs[1400]
cluster_vecs[1000] == vecs[23489]"""

cluster_kmeans = KMeans(n_clusters = 4, n_init = 100, n_jobs = -1, max_iter=300,random_state=1234,verbose=1) # n_init is the amount of times that select the centroid and take an average
cluster_X = cluster_kmeans.fit(cluster_vecs[:,1:])
cluster_labels=cluster_kmeans.labels_.tolist()

cluster['subcluster'] = cluster_kmeans.labels_
#dataset.to_csv("data/subclusters/cluster0_"+FNAME,sep='\t')


l = cluster_kmeans.labels_
pca = PCA(n_components=2).fit(cluster_vecs[:,1:])
datapoint = pca.transform(cluster_vecs[:,1:])

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

color = [label1[i] for i in cluster_labels]
plt.scatter(datapoint[:, 0], datapoint[:, 1], alpha=0.7, c=color)



centroids = cluster_kmeans.cluster_centers_
centroidpoint = pca.transform(centroids)
plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')
plt.show()

import seaborn as sns

# Plot cluster
clusters = cluster.groupby(['subcluster', 'user_name']).size()
fig2, ax2 = plt.subplots(figsize = (30, 15))
sns.heatmap(clusters.unstack(level = 'user_name'), ax = ax2, cmap = 'Reds')

ax2.set_xlabel('user_name', fontdict = {'weight': 'bold', 'size': 24})
ax2.set_ylabel('cluster', fontdict = {'weight': 'bold', 'size': 24})
for label in ax2.get_xticklabels():
    label.set_size(16)
    label.set_weight("bold")
for label in ax2.get_yticklabels():
    label.set_size(16)
    label.set_weight("bold")
    
plt.show()

"""
---------------------------------------------------------------------------------------------------
-----------------------*****WARD******-------------------------------------------------------------
--------------------------------------------------------------------------------------------------
"""

from sklearn.cluster import AgglomerativeClustering

cluster_ward = AgglomerativeClustering(linkage="ward", n_clusters=10)
cluster_X = cluster_ward.fit(cluster_vecs[:,1:])
cluster_labels=cluster_ward.labels_.tolist()

cluster['subcluster2'] = cluster_ward.labels_

l = cluster_ward.labels_
pca = PCA(n_components=2).fit(cluster_vecs[:,1:])
datapoint = pca.transform(cluster_vecs[:,1:])

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

color = [label1[i] for i in cluster_labels]
plt.scatter(datapoint[:, 0], datapoint[:, 1], alpha=0.7, c=color)



#centroids = cluster_ward.cluster_centers_
centroidpoint = pca.transform(centroids)
plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')
plt.show()

"""
---------------------------------------------------------------------------------------------------
-----------------------*****DBSCAN******-------------------------------------------------------------
--------------------------------------------------------------------------------------------------
"""

"""
    DBSCAN:
        eps = La distancia máxima entre dos muestras para que se consideren en el mismo vecindario.
        min_samples = La cantidad de muestras (o peso total) en un vecindario para que un punto se considere como un punto central. Esto incluye el punto en sí.
        metric = ‘cityblock’, ‘cosine’, ‘euclidean’, ‘l1’, ‘l2’, ‘manhattan'
        n_jobs = Número de hilos
"""

from sklearn.cluster import DBSCAN

cluster_dbscan = DBSCAN(eps=3, min_samples=5, metric="euclidean",n_jobs=-1)
cluster_X = cluster_dbscan.fit(cluster_vecs[:,1:])
cluster_labels=cluster_dbscan.labels_.tolist()

cluster['subcluster3'] = cluster_dbscan.labels_

l = cluster_dbscan.labels_
pca = PCA(n_components=2).fit(cluster_vecs[:,1:])
datapoint = pca.transform(cluster_vecs[:,1:])

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

color = [label1[i] for i in cluster_labels]
plt.scatter(datapoint[:, 0], datapoint[:, 1], alpha=0.7, c=color)



centroids = cluster_ward.cluster_centers_
centroidpoint = pca.transform(centroids)
plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')
plt.show()

