#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 18:29:24 2018

@author: kenipatel
"""

import logging
from structures import Corpus
from preprocess import Preprocessor
from algorithms import BagOfWords

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename='scitext.log',
                    filemode='w')

corpus = Corpus('./config/data/text_files.yaml')
data = Preprocessor(corpus, './config/preprocessing.yaml')
b = BagOfWords(data).run()