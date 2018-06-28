# -*- coding: utf-8 -*-
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

        self.config = utilities.get_config(config_file)
        
        self.stop = list(set(stopwords.words('english')))
        
        self.tokenized_docs = []
        
        
    def tokenize(self):
        
        self.tokenized_docs = list()
        
        for item in self.data:

            tokens = word_tokenize(item)
            
            lower_tokens = [t.lower() for t in tokens]        
    
            alpha_only = [t for t in lower_tokens if t.isalpha()]
    
            no_stops = [w for w in alpha_only if w not in self.stop]       
    
            self.tokenized_docs.append(no_stops)
            
        
        if self.config['new_stop_set']:
            
            self.stop = self.config['new_stop_set_list']
            
        if self.config['add_stop']:
            
            self.stop.extend(self.config['add_stop_list'])
            
        if self.config['remove_stop']:
            
            self.stop = list(set(self.stop) - set(self.config['remove_stop_list']))
        
        
        
        self.data = []
        
            
        if self.config['stem']:
            
            ps = PorterStemmer()
            stem_words=list()
            for tokens in self.tokenized_docs:
                for item in tokens:
                    stem_words.append(ps.stem(item))
                self.data.append(stem_words)
                stem_words = list()
            return self.data


        else:
        
            wordnet_lemmatizer = WordNetLemmatizer()
            lem_words = list()
            for tokens in self.tokenized_docs:
                for item in tokens:
                    lemmatized = wordnet_lemmatizer.lemmatize(item)
                    lem_words.append(lemmatized)
                self.data.append(lem_words)
                lem_words = list()
            return self.data
    
    