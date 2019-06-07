#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar 13 21:41:07 2019

@author: hat
"""
import pandas as pd  # For data handling

subcluster1 = cluster[cluster['subcluster']==1]
subcluster2 = cluster[cluster['subcluster2']==2]
subcluster2 = subcluster2[subcluster2['user_name']!="Citytv"]
subcluster4 = cluster[cluster['subcluster2']==4]
subcluster7 = cluster[cluster['subcluster2']==7]
subcluster9 = cluster[cluster['subcluster2']==9]

subcluster_a = pd.concat([subcluster1,subcluster2,subcluster4, subcluster7, subcluster9])

subcluster_vecs = np.zeros((len(subcluster.id_tweet.values),401))

n = 0
for row in subcluster.values:
    subcluster_vecs[n] = vecs[np.where(vecs[:,0] == row[0]),:]
    n=n+1


from sklearn.cluster import AgglomerativeClustering

subcluster_ward = AgglomerativeClustering(linkage="ward", n_clusters=6)
subcluster_X = subcluster_ward.fit(subcluster_vecs[:,1:])
subcluster_labels=subcluster_ward.labels_.tolist()

subcluster['subsubcluster'] = subcluster_ward.labels_

l = subcluster_ward.labels_
pca = PCA(n_components=2).fit(subcluster_vecs[:,1:])
datapoint = pca.transform(subcluster_vecs[:,1:])

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

color = [label1[i] for i in subcluster_labels]
plt.scatter(datapoint[:, 0], datapoint[:, 1], alpha=0.7, c=color)



centroids = subcluster_ward.cluster_centers_
centroidpoint = pca.transform(centroids)
plt.scatter(centroidpoint[:, 0], centroidpoint[:, 1], marker='^', s=150, c='#000000')
plt.show()


subcluster = subcluster_a[['id_tweet','created_at','user_name','text','clean','subsubcluster']]

subcluster0 = subcluster[subcluster['subsubcluster']==0]
subcluster0 = subcluster0[subcluster0['user_name']!="Citytv"]


subcluster1 = subcluster[subcluster['subsubcluster']==1]
subcluster1 = subcluster1[subcluster1['user_name']!="Citytv"]

subcluster3 = subcluster[subcluster['subsubcluster']==3]
subcluster3 = subcluster3[subcluster3['user_name']!="Citytv"]

subcluster6 = subcluster[subcluster['subsubcluster']==6]
subcluster6 = subcluster6[subcluster6['user_name']!="Citytv"]


subcluster_a = pd.concat([subcluster0,subcluster1,subcluster3, subcluster6])
subcluster = subcluster_a

subcluster2 = subcluster[subcluster['subsubcluster']==2]
subcluster3 = subcluster[subcluster['subsubcluster']==3]
subcluster_b = pd.concat([subcluster2,subcluster3])

subcluster_b.to_csv("data/subclusters/cluter2_timeline_user_A.tsv",sep='\t')


subcluster = subcluster[subcluster['subsubcluster']==0]


subclusterP = cluster[cluster['cluster']>-1]
subclusterN = subcluster[subcluster['subsubcluster']==-1]

subclusterN = cluster[cluster['subcluster']==-1]
subcluster_c = pd.concat([subclusterP,subcluster_b])

subclusterP.to_csv("data/subclusters/search_positive.tsv",sep='\t')
subclusterN.to_csv("data/subclusters/search_negative.tsv",sep='\t')

subcluster = subcluster[subcluster['subsubcluster']==0]


subclusterP = dataset[dataset['cluster']==1]
subclusterP = subclusterP[subclusterP['user_name']!="rutassitp"]
subclusterPa = subclusterP

subclusterN1 = dataset[dataset['cluster']==0]
subclusterN2 = dataset[dataset['cluster']==2]
subclusterN4 = dataset[dataset['cluster']==4]
subclusterN4 = subclusterN4[subclusterN4['user_name']!="WazeTrafficBOG"]
subclusterN5 = cluster[cluster['subcluster']==2]

subclusterN = pd.concat([subclusterN1,subclusterN2,subclusterN4,subclusterN5])