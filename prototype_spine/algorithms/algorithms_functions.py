# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:29:23 2018

@author: Brendan Gochett
"""

def bow(documents):
    new_dict = {}
    new_list = list()
    for i in documents:
        for j in i:
            if j in new_dict:
                new_dict[j] += 1
            else:
                new_dict[j] = 1
        new_list.append(new_dict)
        new_dict = {}
    return new_list