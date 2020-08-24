#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Aug  23 18:23:41 2020

@author: solofruad

This script is based on Norvig (2009) in Natural Language Corpus Data. Beautiful Data, O’Reilly Media, Chapter 14, 219 - 242. ISBN 9780596157111
"""

import re, string, random, glob, operator, heapq, functools
from collections import defaultdict
from math import log10

def memo(f):
        "Memoize function f."
        table = {}
        def fmemo(*args):
            if args not in table:
                table[args] = f(*args)
            return table[args]
        fmemo.memo = table
        return fmemo

class WordSegmentation:
    def memo(f):
        "Memoize function f."
        table = {}
        def fmemo(*args):
            if args not in table:
                table[args] = f(*args)
            return table[args]
        fmemo.memo = table
        return fmemo
    
    @memo
    def segment(text):
        "Return a list of words that is the best segmentation of text."
        if not text: return []
        candidates = ([first]+segment(rem) for first,rem in splits(text))    
        return max(candidates, key=Pwords)

    def splits(text, L=20):
        "Return a list of all possible (first, rem) pairs, len(first)<=L."
        return [(text[:i+1], text[i+1:]) 
                for i in range(min(len(text), L))]

    def Pwords(words): 
        "The Naive Bayes probability of a sequence of words."
        return product(Pw(w) for w in words)
    
    #### Support functions (p. 224)

    def product(nums):
        "Return the product of a sequence of numbers."
        return functools.reduce(operator.mul, nums, 1)
    
    def datafile(name, sep='\t'):
        "Read key,value pairs from file."
        for line in open(name):
            yield line.split(sep)

    def avoid_long_words(key, N):
        "Estimate the probability of an unknown word."
        return 10./(N * 10**len(key))

class Pdist(dict):
    "A probability distribution estimated from counts in datafile."
    def __init__(self, data=[], N=None, missingfn=None):
        for key,count in data:
            self[key] = self.get(key, 0) + int(count)
        self.N = float(N or sum(self.itervalues()))
        self.missingfn = missingfn or (lambda k, N: 1./N)
    def __call__(self, key): 
        if key in self: return self[key]/self.N  
        else: return self.missingfn(key, self.N)


