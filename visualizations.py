# -*- coding: utf-8 -*-
"""
Created on Mon Jul  2 10:37:05 2018

@author: 597667
"""
import inspect
import utilities
# from sklearn.feature_extraction.text import CountVectorizer

import sklearn
# Import all of the scikit learn stuff

from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.preprocessing import Normalizer
from sklearn import metrics
from sklearn.cluster import KMeans, MiniBatchKMeans
import pandas as pd
from pandas import DataFrame
import warnings
import numpy

class Visualizations(object):
    
    def __init__(self, data, config_file):
        self.data = data
        pass # because the next line doesn't actually work yet, need to build a preprocessing.yaml file
        self.config = utilities.get_config(config_file)
        print('\n\n\nalg config:\n\n', self.config)
        self.result = None
        
    def __iter__(self):
        for item in self.data:
            yield item

    def run(self):
        result_dict = {}
        # NEED TO THINK ABOUT HOW TO DO FOR MULTIPLE DOCS/SPLIT BY SENTENCES  
        if self.config['histogram']:
            # print('\n\nERROR: LSA not yet implemented\n\n')
            h = histogram(self.data)
            h.run()
            result_dict['histogram'] = h.output

        if self.config['wordcloud']:
            w = wordmap(self.data)
            w.run()
            result_dict['wordcloud'] = w.output
        
        if self.config['clustermap']:
            c = c(self.data)
            c.run()
            result_dict['clustermap'] = c.output

        if self.config['scatterplot']:
            s = scatterplot(self.data)
            s.run()
            result_dict['scatterplot'] = s.output

        print(result_dict)
        self.result = result_dict
        return self.result_dict



class VectorSpaceModels(object):
    
    def __init__(self, corpus):
        self.data = corpus
        self.CosineSimilarity = None
        self.dtm_lsa = None
        self.svd = None
        self.kmeans = None

###  Word Cloud is an example of how visualizations should look like
class worldcloud(VectorSpaceModels):
    
    def __init__(self, corpus):
        super().__init__(corpus)
        self.run()
    
    def run_word_freq(self):
        bow_series = pd.Series(self.output['vocabulary'])
        bow_data = bow_series.to_frame().reset_index()
        bow_data.columns = ['Word', 'Word Count']
        bow_max = bow_data.sort_values(by='Word Count', ascending=False)
        bow_max = bow_max.set_index('Word')
        self.output = bow_max
