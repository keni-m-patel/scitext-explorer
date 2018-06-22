# -*- coding: utf-8 -*-
"""
Created on Thu Jun 21 13:29:23 2018

@author: Brendan Gochett
"""

from collections import Counter

#Bag of Words: taking tokens and converting into list of words
def bow_from_tokens(documents):
    new_docs=list()
    for i in range(len(documents)-1):
        for t in documents:
            bow_simple = Counter(t)
            new_docs.append(bow_simple)
    return new_docs
