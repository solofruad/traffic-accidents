#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 19:05:56 2019

@author: hat
"""

import pandas as pd  # For data handling

pc1_timeline = pd.read_csv("data/subclusters/cluster1_timeline_user_positive.tsv", delimiter = "\t", quoting = 3)
pc1_timeline = pc1_timeline[['id_tweet','created_at','user_name','text','clean']]

pc2_timeline = pd.read_csv("data/subclusters/cluster2_timeline_user_positive.tsv", delimiter = "\t", quoting = 3)
pc2_timeline = pc2_timeline[['id_tweet','created_at','user_name','text','clean']]

pc3_timeline = pd.read_csv("data/subclusters/cluster3_timeline_user_positive.tsv", delimiter = "\t", quoting = 3)
pc3_timeline = pc3_timeline[['id_tweet','created_at','user_name','text','clean']]

pc4_timeline = pd.read_csv("data/subclusters/cluster4_timeline_user_positive.tsv", delimiter = "\t", quoting = 3)
pc4_timeline = pc4_timeline[['id_tweet','created_at','user_name','text','clean']]

pc5_timeline = pd.read_csv("data/subclusters/cluster5_timeline_user_positive.tsv", delimiter = "\t", quoting = 3)
pc5_timeline = pc5_timeline[['id_tweet','created_at','user_name','text','clean']]

pc6_timeline = pd.read_csv("data/subclusters/cluster6_timeline_user_positive.tsv", delimiter = "\t", quoting = 3)
pc6_timeline = pc6_timeline[['id_tweet','created_at','user_name','text','clean']]


pc7_timeline = pd.read_csv("data/subclusters/cluster7_timeline_user_positive.tsv", delimiter = "\t", quoting = 3)
pc7_timeline = pc7_timeline[['id_tweet','created_at','user_name','text','clean']]

p_search = pd.read_csv("data/subclusters/search_positive.tsv", delimiter = "\t", quoting = 3)
p_search = p_search[['id_tweet','created_at','user_name','text','clean']]


positive_a = pd.concat([p_search,pc3_timeline, pc5_timeline])


positive_b = pd.concat([positive_a,pc2_timeline])

positive = pd.concat([positive_b, pc1_timeline, pc4_timeline, pc6_timeline, pc7_timeline])
positive = positive.drop_duplicates(['id_tweet'],keep='first')
positive.to_csv("data/subclusters/positive_part1.tsv",sep='\t')


"""
-----------------
-
-----------------
"""

nc0_timeline = pd.read_csv("data/subclusters/cluster0_timeline_user_negative.tsv", delimiter = "\t", quoting = 3)
nc0_timeline = nc0_timeline[['id_tweet','created_at','user_name','text','clean']]

nc2_timeline = pd.read_csv("data/subclusters/cluster2_timeline_user_negative.tsv", delimiter = "\t", quoting = 3)
nc2_timeline = nc2_timeline[['id_tweet','created_at','user_name','text','clean']]

nc3_timeline = pd.read_csv("data/subclusters/cluster3_timeline_user_negative.tsv", delimiter = "\t", quoting = 3)
nc3_timeline = nc3_timeline[['id_tweet','created_at','user_name','text','clean']]

nc4_timeline = pd.read_csv("data/subclusters/cluster4_timeline_user_negative.tsv", delimiter = "\t", quoting = 3)
nc4_timeline = nc4_timeline[['id_tweet','created_at','user_name','text','clean']]

nc5_timeline = pd.read_csv("data/subclusters/cluster5_timeline_user_negative.tsv", delimiter = "\t", quoting = 3)
nc5_timeline = nc5_timeline[['id_tweet','created_at','user_name','text','clean']]

nc6_timeline = pd.read_csv("data/subclusters/cluster6_timeline_user_negative.tsv", delimiter = "\t", quoting = 3)
nc6_timeline = nc6_timeline[['id_tweet','created_at','user_name','text','clean']]

n_search = pd.read_csv("data/subclusters/search_negative.tsv", delimiter = "\t", quoting = 3)
n_search = n_search[['id_tweet','created_at','user_name','text','clean']]


negative = pd.concat([nc0_timeline, nc2_timeline, nc3_timeline, nc4_timeline, nc5_timeline, nc6_timeline, n_search])
negative = negative.drop_duplicates(['id_tweet'],keep='first')
negative.to_csv("data/subclusters/negative_part1.tsv",sep='\t')