'''
todo:
1) add TFIDF instead of CountVectorizer to algs for LSA ::::: done
2) make generators repeatable so that I can run count vectrorizer for BOW and TFIDF for LSA  # I THINK IT WORKS NOW

'''


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


class Algorithm(object):
    
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
        if self.config['latent_semantic_analysis']:
            # print('\n\nERROR: LSA not yet implemented\n\n')
            l = LatentSemanticAnalysis(self.data)
            l.run()
            result_dict['latent_semantic_analysis'] = l.output

        if self.config['bag_of_words']:
            b = BagOfWords(self.data)
            b.run()
            result_dict['bag_of_words'] = b.output
        
        if self.config['tf_idf']:
            t = Tf_Idf(self.data)
            t.run()
            result_dict['tf_idf'] = t.output

        if self.config['word_frequency_table']:
            w = WordFreq(self.data)
            w.run()
            result_dict['word_frequency_table'] = w.output
        
        if self.config['LSA_Concepts']:
            c = LSA_Concepts(self.data)
            c.run()
            result_dict['LSA_Concepts'] = c.output        

        print(result_dict)
        return result_dict
    
# Base class for Vector Space Models (Bag of Words, LSA, LDA, Word2Vec, Doc2Vec)
class VectorSpaceModels(object):
    
    def __init__(self, corpus):
        self.data = corpus
        self.vectorizer = None
        self.dtm = None
        self.dtm_dense = None
        self.vocabulary = None
        self.dtm_lsa = None

        
class BagOfWords(VectorSpaceModels):
    
     def __init__(self, corpus):
        super().__init__(corpus)
        
     def run(self):   
        self.vectorizer = CountVectorizer(lowercase=True, stop_words='english')
        self.dtm = self.vectorizer.fit_transform(self.data)
        dtm_dense = self.dtm.todense()
        vocabulary = self.vectorizer.vocabulary_
        self.output = {'dtm': self.dtm,
                        'dtm_dense': dtm_dense,
                        'vocabulary': vocabulary}
        
        # inspecing the program stack to get the calling functions name so we don't have to hardcode it
        # when building our output
        
###  Word Frequency table inputting BagOFWords outputting freq table
class WordFreq(BagOfWords):
    
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


class LatentSemanticAnalysis(VectorSpaceModels):
    '''
    currently non-functional, need to ake this take in multiple docs for comparison.
    '''

    def __init__(self, corpus):
        super().__init__(corpus)

    def run(self):
        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self.dtm = self.vectorizer.fit_transform(self.data)
        lsa = TruncatedSVD(n_components=200)  # , algorithm = 'arpack')
        self.dtm_lsa = lsa.fit_transform(self.dtm)
# dataframe = pd.DataFrame(lsa.components_, index=["component_1","component_2"], columns=self.vectorizer.get_feature_names())

        self.output = {'dtm': self.dtm,
                        'dtm_lsa': self.dtm_lsa}
# ,'dataframe': dataframe}}
class LSA_Concepts(LatentSemanticAnalysis):
    def __init__(self, dtm_lsa):
        super().__init__(dtm_lsa)
 
    def run(self):
        terms = Normalizer(copy=False).fit_transform(self.dtm_lsa)
        terms = self.vectorizer.get_feature_names()
        for i, comp in enumerate(self.lsa.components_): 
            termsInComp = zip (terms,comp)
            sortedTerms =  sorted(termsInComp, key=lambda x: x[1], reverse=True) [:10]
            print("Concept %d:" % i )
            for term in sortedTerms:
                print(term[0])
            print (" ")
        self.output = print (" ")
        
class Tf_Idf(VectorSpaceModels):
    
    def __init__(self, corpus):
        super().__init__(corpus)
        
    def run(self):
        vectorizer = TfidfVectorizer(stop_words='english', lowercase=True, encoding='utf-8')
        
        #Tranforms corpus into vectorized words
        self.dtm = vectorizer.fit_transform(self.data)
        
        #Prints idf'd words
        print(vectorizer.get_feature_names())
        
        #Prints doc-term matrix
        print(self.dtm)
        
        #Prints and returns Data Table of doc-term matrix
        Tf_Idf_Table = pd.DataFrame(self.dtm.toarray())
        self.output = print(Tf_Idf_Table)
        
        
#
# Base class for Topic Models (Topic Modelingm Named Entity Recognition, etc.)
class TopicModels(object):
    pass
        
        
    