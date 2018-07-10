#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jun 23 14:37:17 2018

@author: patelkm
"""
import yaml

def get_config(config_file):
    with open(config_file,'r') as stream:
        return yaml.load(stream)
    