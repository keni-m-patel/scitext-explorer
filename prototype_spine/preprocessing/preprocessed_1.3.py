
# coding: utf-8

# In[ ]:


import pandas as pd
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
from wordcloud import WordCloud
from os import path


# In[ ]:


#Import different documents from a file
#Must give path
#Works for text files and PDFs
#Turns files into a list of strings

def text_import(path):
    files = glob.glob(path + '*')
    documents=list()
    for textfile in files[:]:
        if '.txt' in textfile:
            textfile_open = open(textfile,'r')
            textfileReader = textfile_open.read()
            textfile_1 = ''
            textfile_1 = textfileReader
            documents.append(textfile_1)
        elif '.pdf' in textfile:
            pdfFileObj = open(textfile, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            textfile_1 = ''
            for page in range(0,pdfReader.numPages):
                textfile_1 += pdfReader.getPage(page).extractText()
            documents.append(textfile_1)
        else:
            print('File Error: Cannot read file type for ' + textfile + '\n') 
    return documents


#Removes stop words and punctuation and makes letter lowercase
#Then does tokenization
#Keeps form of list of strings, but breaks it into words

def complete_tokenize(documents):
    tokenized_documents=list()
    stop = set(stopwords.words('english'))
    Add_Stop = int(input('To Add a Stop Word Enter 1: '))
    while Add_Stop == 1:
        look_at_stop = int(input("Press 1 to look at set of stop words. Press 2 if not."))
        if look_at_stop == 1:
            print(stop)
        stop_word_added = input('Enter a stop word to add: ')
        if stop_word_added not in stop:
            stop.add(stop_word_added)
        else:
            print("That word is alredy in the set of stop words!")
        Add_Stop = int(input('To Add Another Stop Word Enter 1: '))
    Remove_Stop = int(input('To Remove a Stop Word Enter 1: '))
    while Remove_Stop == 1:
        look_at_stop_1 = int(input("Press 1 to look at set of stop words. Press 2 if not."))
        if look_at_stop_1 == 1:
            print(stop)
        stop_word_removed = input('Enter a stop word to remove: ')
        if stop_word_removed in stop:
            stop.remove(stop_word_removed)
        else:
            print("That word is not in the set of stop words!")
        Remove_Stop = int(input('To Remove Another Stop Word Enter 1: '))
    for text in documents:   
        # TO DO: word_tokenize chapter_one
        tokens = word_tokenize(text)   
        # Convert the tokens into lowercase
        lower_tokens = [t.lower() for t in tokens]
        # Retain alphabetic words: alpha_only
        alpha_only = [t for t in lower_tokens if t.isalpha()]
        ## Retrieve list of NLTK Stopwords for English
    
        # Remove all stop words: no_stops
        no_stops = [w for w in alpha_only if w not in stop]       
        tokenized_documents.append(no_stops)
    return tokenized_documents


#Stems tokens
#List of strings

def stem_tokens(documents):  
    ps = PorterStemmer()
    stem_docs=list()
    for tokens in documents:
        for item in tokens:
            stem_item = ps.stem(item)
        stem_docs.append(stem_item)
        return stem_docs


#Lemmatizes tokens
#List of strings

def lemma(documents):
    lem_docs=list()
    wordnet_lemmatizer = WordNetLemmatizer()
    for no_stops in documents:
        for t in no_stops:
            lemmatized = wordnet_lemmatizer.lemmatize(t)
            #bow = Counter(lemmatized)
            lem_docs.append(lemmatized)
    return lem_docs

