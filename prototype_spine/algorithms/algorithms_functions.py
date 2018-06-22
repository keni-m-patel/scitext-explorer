# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:29:23 2018

@author: Brendan Gochett
"""

#Bag of Words: taking tokens and converting into list of words

def bow(documents):

    new_dict = {}
    for i in documents:
        if i in new_dict:
            new_dict[i] += 1
        else:
            new_dict[i] = 1
    return new_dict

