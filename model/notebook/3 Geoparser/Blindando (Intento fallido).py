#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 19 14:55:03 2021

@author: hat
"""

import pandas as pd

import sys
sys.path.insert(0, '../../')

from classes.tweet2accident.preprocessing import Preprocessing
from classes.tweet2accident.doc2vec import Embedding


from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt

dir_ = "../../data/database/output_ml/M1/NER_extractor/"
file = 'accident_tweets_lat_lon_geocord_bogota_unique.tsv'

dataset = pd.read_csv(dir_+file, delimiter = "\t", quoting = 3)
#dataset = dataset[:100]
X = dataset.text


###### Preprocessing
directory = "../../data/v1/doc2vec/"
file = "6_clean_lemma_dataset_propuesta1_5050"
type_clean = 6 #Tiene que ser el mismo que 'file' (prefijo)

clean = Preprocessing(type_clean=type_clean, njobs=4)
aux = clean.fit_transform(X)

##### Embedding
embedding = Embedding(type_transform='dbow',directory=directory, file=file)
aux2 = embedding.fit_transform(X)


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
kmeans.fit(aux2)
labels=kmeans.labels_.tolist()

dataset['cluster'] = kmeans.labels_

"""-------------------------------GRAFICANDO-----------------------------------------------"""

l = kmeans.labels_
pca = PCA(n_components=2).fit(aux2)
datapoint = pca.transform(aux2)

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

cluster_dbscan = DBSCAN(eps=0.172, min_samples=7, metric="euclidean",n_jobs=-1)
cluster_dbscan.fit(aux2)
cluster_labels=cluster_dbscan.labels_.tolist()

dataset['cluster'] = cluster_dbscan.labels_

l = cluster_dbscan.labels_
pca = PCA(n_components=2).fit(aux2)
datapoint = pca.transform(aux2)

plt.figure
plt.scatter(datapoint[:, 0], datapoint[:, 1], alpha=0.7, cmap='magma')


"""label1 = ["#32C12C", #0. GREEN
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
"""
plt.scatter(datapoint[:, 0], datapoint[:, 1], alpha=0.7, cmap='magma')


