#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 18:29:24 2018

@author: kenipatel
"""

import logging
from structures import Corpus
from algorithms import Algorithm
from visualization import Visualization
from itertools import chain, repeat

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename='scitext.log',
                    filemode='w')
'''
TODO:
# if select something (ie for PP) that doesn't work for ALG or VIZ, spit out warning
'''


corpus = Corpus('./config/data/text_files.yaml', 'doc')

tokens = corpus()
tokenized_docs = []

for doc in tokens:
    tokenized_docs.append(doc)

#print(tokenized_docs)
#print('tokens')
    
file_names = corpus.get_file_names()

token_dict = dict(zip(file_names, chain(tokenized_docs, repeat(None))))

print('tokens!!!!!!!!!!')
print(token_dict)


    

# have to change this to give a string instead of DOT Text fsvsdvgbd nonsense

#print(file_object)
#print(file_object.grouping)
#print(file_object.config)



print(tokens)

alg = Algorithm(tokens, './config/algorithms.yaml')
alg_ran = alg.run()

print("test1")
print(alg.run())
vis = Visualization( './config/visualization.yaml',alg)


vis.run()

