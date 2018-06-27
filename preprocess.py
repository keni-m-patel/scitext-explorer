#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 24 21:52:23 2018

@author: kenipatel
"""

import utilities

class Preprocessor(object):
    
    def __init__(self, data, config_file):
        self.data = data
        pass # because the next line doesn't actually work yet, need to build a preprocessing.yaml file
        self.config = utilities.get_config(config_file)
        
    def __iter__(self):
        for item in self.data:
            yield item

    def run(self):
        return self.data