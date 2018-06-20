# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize

#This imports file and converts to string.
bren = open('Emerson.txt', "rb").read()
bren = str(bren)

tokens = word_tokenize(bren)
tokens_lower = [t.lower() for t in tokens]


#Tokenize

def stem_tokens(tokens):  
    ps = PorterStemmer()  
    return [ps.stem(item) for item in tokens]
    

stem_tokens(tokens)