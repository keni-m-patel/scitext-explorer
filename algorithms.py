import inspect
import utilities

from sklearn.manifold import mds, TSNE

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.decomposition import TruncatedSVD

from sklearn.feature_extraction.text import TfidfVectorizer

from sklearn.feature_extraction.text import CountVectorizer

from sklearn.preprocessing import Normalizer


from sklearn.cluster import KMeans, MiniBatchKMeans

from collections import defaultdict, Counter

from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
#from sklearn import metrics

import pandas as pd
#from pandas import DataFrame
#import warnings
#import numpy

#Viz Stuff
import matplotlib.pyplot as plt


class Algorithm(object):

    def __init__(self, data, config_file):
        self.corpus = data
        pass # because the next line doesn't actually work yet, need to build a preprocessing.yaml file
        self.config = utilities.get_config(config_file)
        print('\n\n\n\nRunning the following algorithms:\n\n')
        print(self.config)
        
    def __iter__(self):
        for item in self.corpus:
            yield item

    def run(self):
        result_dict = {}

        if self.config['latent_semantic_analysis']:
            l = LatentSemanticAnalysis(self.corpus)
            l.run()
            result_dict['latent_semantic_analysis'] = l.output

            if self.config['LSA_Concepts']:
                c = LSA_Concepts(self.corpus, l.dtm_lsa, l.lsa, l.vectorizer)
                c.run()
                result_dict['LSA_Concepts'] = c.output
            
            if self.config['kmeans']:
                k = kmeans(self.corpus, l.dist)
                k.run()
                result_dict['kmeans'] = k.output
               
            if self.config['tsne']:
                t = tsne(self.corpus, l.dist)
                t.run()
                result_dict['tsne'] = t.output

        if 'bag_of_words' in self.config:
            b = BagOfWords(self.corpus)
            b.run()
            result_dict['bag_of_words'] = b.output
            
            if 'word_frequency_table' in self.config:
                w = WordFreq(self.corpus, b.output)
                w.run()
                result_dict['word_frequency'] = w.output
                
        if self.config['tf_idf']:
            t = Tf_Idf(self.corpus)
            t.run()
            result_dict['tf_idf'] = t.output

        output_text = ""
        for alg,result in result_dict.items():
            output_text += "\n\nalgorithm: {}\n\nresult:\n\n {}\n\n".format(alg,result)

        print(output_text)
        return output_text



# Base class for Vector Space Models (Bag of Words, LSA, LDA, Word2Vec, Doc2Vec)
class VectorSpaceModels(object):
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.dtm = None
        self.vectorizer = None
    

        
class BagOfWords(VectorSpaceModels):
  
     def __init__(self, corpus):
        super().__init__(corpus)
        self.bow = None
        print('\n\n\n\nRunning the following algorithm: \nBag of Words\n\n')
        
     def run(self): 

        self.vectorizer = CountVectorizer(lowercase=True, stop_words='english')
        self.dtm = self.vectorizer.fit_transform(self.corpus)
        dtm_dense = self.dtm.todense()
        vocabulary = self.vectorizer.vocabulary_  # dict of unique word, index key-value pairs 

        # print('\nvocab to index\n', vocabulary)
        # print(self.vectorizer.get_feature_names())

        list1 = self.dtm.toarray()[0]
        list2 = self.dtm.toarray()[1]
        # print(list1,'\n', list2)
        dtm_array = [sum(x) for x in zip(list1, list2)]

        self.bow = {word:freq for word,freq in zip(vocabulary.keys(), dtm_array)}
        # print('bow\n', self.bow)

        self.output = self.bow
        # print('\n\nCHECK THIS\n\n')
        # {'dtm': self.dtm,'dtm_dense': dtm_dense,'vocabulary': vocabulary, 'vectorizer': self.vectorizer}
    

        
class WordFreq(VectorSpaceModels):
    
    def __init__(self, corpus, bow_output):
        super().__init__(corpus)
        print('\n\n\n\nRunning the following algorithm: \nWord Frequency\n\n')
        print('bow output\n', bow_output)
        self.bow_output = bow_output
        self.output = None
        self.run()
    
    def run(self):
        bow_series = pd.Series(self.bow_output)
        bow_data = bow_series.to_frame().reset_index()
        bow_data.columns = ['Word', 'Word Count']
        bow_max = bow_data.sort_values(by='Word Count', ascending=False)
        bow_max = bow_max.set_index('Word')
        self.output = bow_max


class LatentSemanticAnalysis(VectorSpaceModels):

    def __init__(self, corpus):
        super().__init__(corpus)
        print('\n\n\n\nRunning the following algorithm: \nLatent Semantic Analysis\n\n')

    def run(self):

        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        self.dtm = self.vectorizer.fit_transform(self.corpus)
        self.lsa = TruncatedSVD(n_components=200)  # , algorithm = 'arpack')
        self.dtm_lsa = self.lsa.fit_transform(self.dtm)
        self.dist = 1 - cosine_similarity(self.dtm_lsa)
        
        # dataframe = pd.DataFrame(lsa.components_, index=["component_1","component_2"], columns=self.vectorizer.get_feature_names())
        self.output = {'dtm': self.dtm,
                        'dtm_lsa': self.dtm_lsa}
# ,'dataframe': dataframe}}
        
class LSA_Concepts(VectorSpaceModels):
    def __init__(self, corpus, dtm_lsa, lsa, vectorizer):
        super().__init__(corpus)
        
        self.dtm_lsa = dtm_lsa
        self.lsa = lsa
        self.vectorizer = vectorizer
        
    def run(self):
        terms = Normalizer(copy=False).fit_transform(self.dtm_lsa)
        terms = self.vectorizer.get_feature_names()
        for i, comp in enumerate(self.lsa.components_): 
            termsInComp = zip (terms,comp)
            self.output =  sorted(termsInComp, key=lambda x: x[1], reverse=True) [:10]
            print("Concept %d:" % i )
            for term in  self.output:
                print(term[0])
            print (" ")
            
class kmeans(LatentSemanticAnalysis):  
    def __init__(self, corpus, dist):
        super().__init__(corpus) 
        self.dist = dist
        
    def run(self):
        models = dict()
        km_dict = dict()
        max_clusters = 2

        for index in range(2,max_clusters + 1):
            km = KMeans(n_clusters = index,  init = 'k-means++', max_iter = 1000, random_state = 1423)
            km.fit(self.dist)
            clusters = km.labels_.tolist()
            km_dict[index] = Counter(clusters)
            self.output = (index, Counter(clusters))
'''
        models[index] = {'KMeans Model': km,
                             'KMeans Centroids': km.cluster_centers_.argsort()[:, ::-1],
                             'Document-Clustering': Counter(clusters),
                             'Frame': pd.DataFrame({'Cluster': clusters})}
                                                    #'Document Name': docnames})}
        background = 'gray'
        higlight = '#2171b5'
        accent = 'dimgray'
        font_size = 10.0
        index = 0
        for key,val in models.items():

            if index%5 == 0:
                fig = plt.figure(figsize=(12,2))

            ax = fig.add_subplot(151 + index%5)

            x = [k for k,v in sorted(val['Document-Clustering'].items())]
            y = [v for k,v in sorted(val['Document-Clustering'].items())]

            plt.bar(x,y,width = 0.8, color = background)

            plt.title(str(key) + ' Document\nClusters', fontweight = 'normal', color = accent)

            plt.grid(False)
            ax.tick_params(direction='out', length = 4, width = 1, colors = background,
                           labelsize = font_size, labelcolor = background)

            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_visible(False)
            ax.spines['top'].set_visible(False)
            ax.spines['bottom'].set_visible(False)

            plt.savefig('Corpus2 Clusters ' + str(index) + '.png', transparent = True, bbox_inches = 'tight', dpi = 600)

            index += 1
'''
class tsne(LatentSemanticAnalysis):
    def __init__(self, corpus, dist):
        super().__init__(corpus)      
        
        self.dist = dist         

    def run(self):
        random_state = 1423
        tsne_matrix = TSNE(n_components=2, perplexity=30.0, early_exaggeration=12.0, learning_rate=200.0, 
                           n_iter=1000, n_iter_without_progress=300, min_grad_norm=1e-07, metric='euclidean', 
                           init='random', verbose=0, random_state = random_state, method='barnes_hut', angle=0.5)
        
        position = tsne_matrix.fit_transform(self.dist)
        
        x, y = position[:, 0], position[:, 1]
        self.output = (x,y)


class Tf_Idf(VectorSpaceModels):
    
    def __init__(self, corpus):
        super().__init__(corpus)
        self.output = None
        print('\n\n\n\nRunning the following algorithm: \nTFIDF \n\n')
        
    def run(self):
        self.vectorizer = TfidfVectorizer(stop_words='english', lowercase=True, encoding='utf-8')
        
        #Tranforms corpus into vectorized words
        self.dtm = self.vectorizer.fit_transform(self.corpus)
        
        #Prints idf'd words
        # print(self.vectorizer.get_feature_names())
        
        #Prints doc-term matrix
        # print(self.dtm)
        
        #Prints and returns Data Table of doc-term matrix
        Tf_Idf_Table = pd.DataFrame(self.dtm.toarray())
        self.output = Tf_Idf_Table
        

# Base class for Topic Models (Topic Modelingm Named Entity Recognition, etc.)
class TopicModels(object):
    pass
