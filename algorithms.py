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
import warnings
import numpy


class Algorithm(object):
    
    def __init__(self, data, config_file):
        self.data = data
        pass # because the next line doesn't actually work yet, need to build a preprocessing.yaml file
        self.config = utilities.get_config(config_file)
        print('\n\n\nalg config:\n\n', self.config)
        
    def __iter__(self):
        for item in self.data:
            yield item

    def run(self):
        result_dict = {}
        # NEED TO THINK ABOUT HOW TO DO FOR MULTIPLE DOCS/SPLIT BY SENTENCES  
        vectorizer = CountVectorizer(lowercase=True, stop_words='english')
        dtm = vectorizer.fit_transform(self.data)  # HACKY: use in all things to avoid iterating multiple times

        if self.config['latent_semantic_analysis']:
            # print('\n\nERROR: LSA not yet implemented\n\n')
            l = LatentSemanticAnalysis(self.data, vectorizer, dtm)
            l.run()
            result_dict['latent_semantic_analysis'] = l.output

        if self.config['bag_of_words']:
            b = BagOfWords(self.data, vectorizer, dtm)
            b.run()
            result_dict['bag_of_words'] = b.output

        print(result_dict)
        return result_dict



# Base class for Vector Space Models (Bag of Words, LSA, LDA, Word2Vec, Doc2Vec)
class VectorSpaceModels(object):
    
    def __init__(self, corpus, vectorizer, dtm):
        self.corpus = corpus
        self.vectorizer = vectorizer
        self.dtm = dtm
        self.dtm_dense = None
        self.vocabulary = None

        
class BagOfWords(VectorSpaceModels):
    
     def __init__(self, corpus, vectorizer, dtm):
        super().__init__(corpus, vectorizer, dtm)
        
     def run(self):   
        # vectorizer = CountVectorizer(lowercase=True, stop_words='english')
        # dtm = vectorizer.fit_transform(self.corpus)
        dtm_dense = self.dtm.todense()
        vocabulary = self.vectorizer.vocabulary_
        self.output = {'dtm': self.dtm,
                        'dtm_dense': dtm_dense,
                        'vocabulary': vocabulary}
        
        # inspecing the program stack to get the calling functions name so we don't have to hardcode it
        # when building our output
 

class LatentSemanticAnalysis(VectorSpaceModels):
    '''
    currently non-functional, need to ake this take in multiple docs for comparison.
    '''

    def __init__(self, corpus, vectorizer, dtm):
        super().__init__(corpus, vectorizer, dtm)

    def run(self):
        lsa_list = []

        # Fit LSA. Use algorithm = “randomized” for large datasets
        lsa = TruncatedSVD(200)  # , algorithm = 'arpack')
        dtm_lsa = lsa.fit_transform(self.dtm)
        dtm_lsa = Normalizer(copy=False).fit_transform(dtm_lsa)
        print('\ndtm_lsa:', dtm_lsa)

        pd.DataFrame(lsa.components_,index = ["component_1","component_2"],columns = self.vectorizer.get_feature_names())

        self.output = {'dtm': self.dtm,
                        'dtm_lsa': dtm_lsa,}

        
 
# Base class for Topic Models (Topic Modelingm Named Entity Recognition, etc.)
class TopicModels(object):
    pass
        
        
    