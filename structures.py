#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 20:53:26 2018

@author: patelkm
"""

import os
import utilities
import logging
import decorators

logger = logging.getLogger(__name__)

@decorators.log(logger)
class Corpus(object):
    
    def __init__(self, config_file):
        self.config = utilities.get_config(config_file) # read the config file and set the log_file name
        self.__read_data(self.config) # get data    
        self.__log() # log things
                                    
    def __iter__(self):
        # custom iterator function that defines how to iterate over 
        # records according to the configuration specified
        # INTERFACE DEFINITION: this iterator should always yield a string
        for doc in self.data_map:
            yield doc
    
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        return len(list(self.config['files']))
        
    def __read_data(self, config):
        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.config['files']]])
        
        if filetype == {'.txt'}:
            # map to implement "lazy loading"; only read files as we need
            self.data_map = map(lambda x: open(os.path.join(self.config['directory'], x)).read(), self.config['files'])

    def __log(self):
        logger.info('Data Map created for: ' + ', '.join(self.config['files']))
        