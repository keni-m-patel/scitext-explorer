#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 21:52:23 2018

@author: kenipatel
"""
import pandas as pd
from pandas import DataFrame
import numpy as np

import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer

import glob
import PyPDF2

import re
from collections import Counter

import matplotlib.pyplot as plt
#from wordcloud import WordCloud
from os import path

class Preprocessor(object):

    

    def __init__(self, data):

        self.data = data

        #self.config = utilities.get_config(config_file)
        
        self.stop = list(set(stopwords.words('english')))
        
        self.tokenized_docs = list()
        
        self.stem_docs = list()
        
        self.lem_docs = list()
        
        
    def new_stop_set(self, new_set):
        
        self.stop = new_set
        

    def add_stop(self, new_stop):
        
        self.stop.extend(new_stop)
    
    
    def remove_stop(self, old_stop):
        
        self.stop = set(self.stop) - set(old_stop)
        
        self.stop = list(self.stop)
        
        #for remove_word in old_stop:
            
            #self.stop.remove(remove_word)
            
    def get_stop(self):
        
        print(self.stop)
        
        
    #def add_single_stop(self, new_word):
        
        #self.new_word = new_word
        
        #self.stop.add(new_word)
        
        
    #def remove_single_stop(self, old_word):
        
        #self.old_word = old_word
        
        #self.stop.remove(old_word)

 
    def tokenize(self):
        
        self.tokenized_docs = list()
        
        for item in self.data:

            tokens = word_tokenize(item)
            
            lower_tokens = [t.lower() for t in tokens]        
    
            alpha_only = [t for t in lower_tokens if t.isalpha()]
    
            no_stops = [w for w in alpha_only if w not in self.stop]       
    
            self.tokenized_docs.append(no_stops)
        

    
    
    #Stems tokens
    #List of strings
    
    def stem(self):  
        ps = PorterStemmer()
        stem_words=list()
        for tokens in self.tokenized_docs:
            for item in tokens:
                stem_words.append(ps.stem(item))
            self.stem_docs.append(stem_words)
            stem_words = list()
        return self.stem_docs

 
    
    
    #Lemmatizes tokens
    #List of strings
    
    def lemma(self):
        lem_words=list()
        wordnet_lemmatizer = WordNetLemmatizer()
        for tokens in self.tokenized_docs:
            for item in tokens:
                lemmatized = wordnet_lemmatizer.lemmatize(item)
                lem_words.append(lemmatized)
            self.lem_docs.append(lem_words)
            lem_words = list()