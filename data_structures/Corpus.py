#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 20:53:26 2018

@author: patelkm
"""

def Corpus(object):
    def __init__(self, config):
        # here we should read a master data configuration file that specifies
        # data source type, location, and method of iterating over records
        self.config = config
        
    def __iter__(self):
        # this is a custom iterator function that defines how to iterate over 
        # records according to the configuration specified
        pass
    
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        pass