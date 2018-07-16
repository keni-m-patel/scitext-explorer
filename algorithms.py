
import inspect
import utilities

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import Normalizer
from sklearn.cluster import KMeans
from collections import Counter
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd

from nltk import ne_chunk, pos_tag
from nltk.tree import Tree
from nltk.tokenize import word_tokenize




class Algorithm(object):
    

    def __init__(self, data, config_file):
        self.corpus = data
        self.config = utilities.get_config(config_file)
        self.results = None
        print('\n\n\n\nRunning the following algorithms:\n\n')
        print(self.config)
        

    def run(self):
        result_dict = {}
        
        
         #HAVE TO SWITCH TO NOT RUN WITH ANY PREPROCESSING
        if self.config['named_entities']:
            ner = Named_Entity_Recognition(self.corpus)
            ner.run()
            self.corpus = ner.output
            result_dict['named_entities'] = self.corpus
            

        if self.config['latent_semantic_analysis']:
            l = LatentSemanticAnalysis(self.corpus)
            l.run()
            result_dict['latent_semantic_analysis'] = l.output

            if self.config['LSA_Concepts']:
                c = LSA_Concepts(self.corpus, l.dtm_lsa, l.lsa, l.vectorizer)
                c.run()
                result_dict['LSA_Concepts'] = c.output
            
            if self.config['kmeans']:
                k = kmeans(self.corpus, l.dtm_lsa)
                k.run()
                result_dict['kmeans'] = k.output
             

        if self.config['bag_of_words']:
            b = BagOfWords(self.corpus)
            b.run()
            result_dict['bag_of_words'] = b.output
            
            if self.config['word_frequency_table']:
                self.w = WordFreq(self.corpus, b.output)
                self.w.run()
                result_dict['word_frequency'] = self.w.output
                
                
        if self.config['tf_idf']:
            t = Tf_Idf(self.corpus)
            t.run()
            result_dict['tf_idf'] = t.output
            

        output_text = ""
        self.results = result_dict
        for alg,result in result_dict.items():
            output_text += "\n\nalgorithm: {}\n\nresult:\n\n {}\n\n".format(alg,result)


        print(output_text)
        return result_dict



# Base class for Vector Space Models (Bag of Words, LSA, LDA, Word2Vec, Doc2Vec)
class VectorSpaceModels(object):
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.dtm = None
        self.vectorizer = None
    

        
class BagOfWords(VectorSpaceModels):
    
     """Gives words and their word count"""
  
     def __init__(self, corpus):
        super().__init__(corpus)
        self.bow = None
        print('\n\n\n\nRunning the following algorithm: \nBag of Words\n\n')
        
     def run(self): 

        self.vectorizer = CountVectorizer(lowercase = False, stop_words = None) #, preprocessor = None, tokenizer = None
        self.dtm = self.vectorizer.fit_transform(self.corpus)
        dtm_dense = self.dtm.todense()

        vocabulary = self.vectorizer.vocabulary_  # dict of unique word, index key-value pairs 

        sorted_by_value = sorted(vocabulary.items(), key=lambda kv: kv[1])

        sorted_vocab = [k for k,v in sorted_by_value]

        dtm_array = sum(self.dtm.toarray())  # [sum(x) for x in zip(list1, list2)]

        self.bow = {word:freq for word,freq in zip(sorted_vocab, dtm_array)}
        self.output = self.bow


class WordFreq(VectorSpaceModels):
    
    """Used to output Bag of Words as a DataFrame"""
    
    def __init__(self, corpus, bow_output):
        super().__init__(corpus)
        print('\n\n\n\nRunning the following algorithm: \nWord Frequency\n\n')
        # print('bow output\n', bow_output)
        self.bow_output = bow_output
        self.output = None
        self.run()
    
    def run(self):
        bow_series = pd.Series(self.bow_output)
        bow_data = bow_series.to_frame().reset_index()
        bow_data.columns = ['Word', 'Word Count']
        bow_max = bow_data.sort_values(by='Word Count', ascending=False)
        #bow_max = bow_max.set_index('Word')
        self.output = bow_max
        return self.output


class LatentSemanticAnalysis(VectorSpaceModels):

    def __init__(self, corpus):
        super().__init__(corpus)
        print('\n\n\n\nRunning the following algorithm: \nLatent Semantic Analysis\n\n')


    def run(self):

        self.vectorizer = TfidfVectorizer(lowercase=True, stop_words='english')
        print('\n\n\n\nTFIDF vectorizer', self.vectorizer)
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
            for term in self.output:
                print(term[0])
            print (" ")
   
         
class kmeans(LatentSemanticAnalysis):  
    def __init__(self, corpus, dtm_lsa):
        super().__init__(corpus) 
        self.dtm_lsa = dtm_lsa
        
    def run(self):
        km_dict = dict()
        max_clusters = 5
        for index in range(2,max_clusters + 1):
            km = KMeans(n_clusters = index,  init = 'k-means++', max_iter = 1000, random_state = 1423)
            km.fit(self.dtm_lsa)
            clusters = km.labels_.tolist()
            km_dict[index] = Counter(clusters)
            self.output = (index, Counter(clusters))


class Tf_Idf(VectorSpaceModels):
    
    def __init__(self, corpus):
        super().__init__(corpus)
        self.output = None
        print('\n\n\n\nRunning the following algorithm: \nTFIDF \n\n')
        
    def run(self):
        #figure out how to link up with preprocess
        self.vectorizer = TfidfVectorizer(stop_words=None, lowercase=False, encoding='utf-8')
        
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
    
    """Parent Class for Named Entity Recognition"""

    
    def __init__(self, corpus):
        self.corpus = corpus

class Named_Entity_Recognition(TopicModels):
    
    """This takes in a document strings and obtains the Named Entities from each. """
    
    def __init__(self, corpus):
        super().__init__(corpus)
        print('\n\n\n\nRunning the following algorithm: \nNamed_Entity_Recognition\n\n')
        
        self.output = []
        self.test = []
        
    def run(self):
        for item in self.corpus:
                chunked_docs = []
                chunked = ne_chunk(pos_tag(word_tokenize(item)))
                chunked_docs.append(chunked)
                continuous_chunk = []
                current_chunk = []
                for chunk in chunked_docs:
                    
                    for i in chunk:
                        self.test.append(i)
                        if type(i) == Tree:
                            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
                        elif current_chunk:
                                
                                named_entity = " ".join(current_chunk)
                                
                                if named_entity not in continuous_chunk:
                                        continuous_chunk.append(named_entity)
                                        current_chunk = []
                        else:
                                continue
                        
                            
                    continuous_chunk = ' '.join(continuous_chunk)
                    self.output.append(continuous_chunk)
       
        #Replace 'the_word' with * 'the_word' * -> "highlight" it
        #filedata.replace(the_word,  "*" + the_word + '*')

     
 
 

        

