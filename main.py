#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 18:29:24 2018

@author: kenipatel
"""

import logging
from structures import Corpus, DotPDF, DotTXT, DotCSV
from preprocess import Preprocessor
from algorithms import Algorithm, BagOfWords

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename='scitext.log',
                    filemode='w')
'''
TODO:
# for future of UI: 
# Config class: init with path to folder, use those defaults
# have method that lets you save as a folder of yaml files
# Algs class have objs in list and then depending on what config/alg.yaml says, will run it.
# if select something (ie for PP) that doesn't work for ALG or VIZ, spit out warning
'''

corpus = Corpus('./config/data/text_files.yaml', 'doc')





file_object = corpus.getObj()
#print(file_object)
#print(file_object.grouping)
#print(file_object.config)


data = Preprocessor(file_object, './config/preprocessing.yaml')
data.run()
tokens = data.output
alg = Algorithm(file_object, './config/algorithms.yaml')

alg.run()
