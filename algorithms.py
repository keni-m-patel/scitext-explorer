import inspect
import utilities
from sklearn.feature_extraction.text import CountVectorizer

from sklearn.decomposition import TruncatedSVD

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.preprocessing import Normalizer
#from sklearn import metrics
#from sklearn.cluster import KMeans, MiniBatchKMeans
import pandas as pd
#from pandas import DataFrame
#import warnings
#import numpy



class Algorithm(object):

    def __init__(self, data, config_file):
        self.data = data
        pass # because the next line doesn't actually work yet, need to build a preprocessing.yaml file
        self.config = utilities.get_config(config_file)
        print('\n\n\n\nRunning the following algorithms:\n\n')
        print(self.config)
        
    def __iter__(self):
        for item in self.corpus:
            yield item

    def run(self):
        result_dict = {}
        
        # NEED TO THINK ABOUT HOW TO DO FOR MULTIPLE DOCS/SPLIT BY SENTENCES  

        if self.config['latent_semantic_analysis']:

            # print('\n\nERROR: LSA not yet implemented\n\n')

            l = LatentSemanticAnalysis(self.corpus, self.config)

            l.run()

            result_dict['latent_semantic_analysis'] = l.output
        
        if 'bag_of_words' in self.config:
            b = BagOfWords(self.corpus)
            b.run()
            result_dict['bag_of_words'] = b.output
            
            if 'word_frequency_table' in self.config:
                w = WordFreq(self.corpus, b.output)
                w.run()
                result_dict['word_frequency'] = w.output
                

        
        if self.config['tf_idf']:
            t = Tf_Idf(self.corpus, self.config)
            t.run()
            result_dict['tf_idf'] = t.output



        print(result_dict)
        return result_dict



# Base class for Vector Space Models (Bag of Words, LSA, LDA, Word2Vec, Doc2Vec)
class VectorSpaceModels(object):
    
    def __init__(self, corpus):
        self.config = config
        self.corpus = corpus
        self.dtm = None
        self.dtm_dense = None
        self.vocabulary = None
       
        
class BagOfWords(VectorSpaceModels):
  
     def __init__(self, corpus):
        super().__init__(corpus)
        print('\n\n\n\nRunning the following algorithm: \nBag of Words\n\n')
        
     def run(self):   
        self.vectorizer = CountVectorizer(lowercase=True, stop_words='english')
        self.dtm = self.vectorizer.fit_transform(self.data)
        dtm_dense = self.dtm.todense()
        vocabulary = self.vectorizer.vocabulary_
        self.output = {'dtm': dtm,'dtm_dense': dtm_dense,'vocabulary': vocabulary}
    

        
class WordFreq(VectorSpaceModels):
    
    def __init__(self, corpus, bow_output):
        super().__init__(corpus)
        print('\n\n\n\nRunning the following algorithm: \nWord Frequency\n\n')
        self.bow_output = bow_output
        self.output = None
        self.run()
    
    def run(self):
        bow_series = pd.Series(self.bow_output['vocabulary'])
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
        print('\n\n\n\nRunning the following algorithm: \nLatent Semantic Analysis\n\n')

    def run(self):

        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')

        self.dtm = self.vectorizer.fit_transform(self.corpus)

        lsa = TruncatedSVD(200)  # , algorithm = 'arpack')

        dtm_lsa = lsa.fit_transform(self.dtm)

        dtm_lsa = Normalizer(copy=False).fit_transform(dtm_lsa)

        # dataframe = pd.DataFrame(lsa.components_, index=["component_1","component_2"], columns=self.vectorizer.get_feature_names())



        self.output = {'dtm': self.dtm,'dtm_lsa': dtm_lsa}  # ,'dataframe': dataframe}

        
class Tf_Idf(VectorSpaceModels):
    
    def __init__(self, corpus):
        super().__init__(corpus)
        self.output = None
        print('\n\n\n\nRunning the following algorithm: \nTFIDF \n\n')
        
    def run(self):
        vectorizer = TfidfVectorizer(stop_words='english', lowercase=True, encoding='utf-8')
        
        #Tranforms corpus into vectorized words
        self.dtm = vectorizer.fit_transform(self.corpus)
        
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
        