#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 20:53:26 2018

@author: patelkm
"""

import os
import utilities
import logging

class Corpus(object):
    def __init__(self, config_file):
        # here we should read a master data configuration file that specifies
        # data source type, location, and method of iterating over records        
        self.config = utilities.get_config(config_file)
        self.log_file = os.path.join(self.config['directory'], 'log', os.path.splitext(config_file)[0] + '.log')
        
        logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(levelname)s %(message)s',
                    filename=self.log_file,
                    filemode='w')

        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.config['files']]])
        
        if filetype == {'.txt'}:
            # the number of files will usually be large, use map so that we implement "lazy loading" 
            # and only read the text files from the stream as we need them!
            self.data_map = map(lambda x: open(os.path.join(self.config['directory'], x)).read(), self.config['files'])
            logging.info("data map created")                        
    def __iter__(self):
        # custom iterator function that defines how to iterate over 
        # records according to the configuration specified
        for doc in self.data_map:
            yield doc
    
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        return len(list(self.data_map))
