
##############################################
###    DOCUMENTATION FOR DEVELOPMENT       ###
##############################################


INSTRUCTIONS:
1) enter your file names under the correct section (representing directories/folders)
2) for each .py file, write description of file and list function names
3) under each function, list function description (what does it do), input type (i.e. string, dict, etc), and output type.
4) add any imports you need to the imports section



### IMPORTS ###  (just copy paste any new imports you need as lines of code)
import yaml
from preprocessing import text_import as timp, complete_tokenize as ctkn
from algorithms import BOW
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

### TOKENIZING STOPWORDS ###
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

### WORD STEMMING ###
import nltk 
from nltk.stem.lancaster import LancasterStemmer
Input: List of lists
Output: Stemmed List of lists

### BAG OF WORDS: NO IMPORTS###
Input: List of lists
Output: List of dictionaries

### DIRECTORY STRUCTURE ###
FILE: main.py

    - description: main file that runs the program.
    
    FUNCTIONS:
        1) main(): function that takes in config file and imports other python files to preprocess, run algs, visualize, etc.
            - input:
            - output: visualization(likely in .png form or similar), receipt (.txt)
   
   
FOLDER: CONFIGURATION

    FILE:


FOLDER:

    FILE:
    
    FILE:
    

FOLDER:

    FILE:
    
    FILE:


FOLDER:

    FILE:
    
    FILE:
    
    
FOLDER:

    FILE:
    
    FILE:
      
    
