#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 18:29:24 2018

@author: kenipatel
"""

import logging
from structures import Corpus
from preprocess import Preprocessor
from algorithms import Algorithm
from itertools import chain, repeat

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename='scitext.log',
                    filemode='w')
'''
TODO:
# ADD MERGE class and functionality with master config and then allow link to all config classes
'''
'''
corpus_list = [Corpus(config_file) for config_file in utilities.get_config('./config/master.yaml')]
corpus_list = [corpus() for corpus in corpus_list]
corpi = Merge(corpus_list)
# run stuff
'''

corpus = Corpus('./config/data/text_files.yaml')

tokens = corpus()
tokenized_docs = []

for doc in tokens:
    tokenized_docs.append(doc)

#print(tokenized_docs)
#print('tokens')
    
file_names = corpus.get_file_names()

token_dict = dict(zip(file_names, chain(tokenized_docs, repeat(None))))


alg = Algorithm(tokens, './config/algorithms.yaml')
alg = alg.run()

#vis = visualization(file_object, './config/visualization.yaml')


#vis.run()

