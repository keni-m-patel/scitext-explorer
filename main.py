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

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename='scitext.log',
                    filemode='w')
'''
TODO:
# if select something (ie for PP) that doesn't work for ALG or VIZ, spit out warning
'''

corpus = Corpus('./config/data/text_files.yaml',)
file_object = corpus()

data = Preprocessor(file_object, './config/preprocessing.yaml', file_names)
data.run()
tokens = data.output
# use preprocessed data
alg = Algorithm(file_object, './config/algorithms.yaml')

alg.run()
