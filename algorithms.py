
import inspect
import utilities

import warnings

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



import gensim

from gensim.corpora.dictionary import Dictionary



class Algorithm(object):
    """Reads the algorithm config file to see the selected algorithm(s)."""

    def __init__(self, data, config_file):
        self.corpus = data
        self.config = utilities.get_config(config_file)
        self.results = None
        print('\n\n\n\nRunning the following algorithms:\n\n')
        print(self.config)
        

    def run(self):
        """Runs algorithm assigned to the user-selected algorithm."""
        
        result_dict = {}
        
         
        #For each if self.config if set to true in the config, will set if statement to true
        #If the if statement is read as true an object for that algorithm type class is made, run, and added to the result dictionary
        #Wwarnings are triggered when a necessary component is not included when an algorithm is set to true in the config file
        
        if self.config['named_entities']:
            ner = Named_Entity_Recognition(self.corpus)
            ner.run()
            self.corpus = ner.output
            result_dict['named_entities'] = self.corpus
            
        
        if not self.config['latent_semantic_analysis'] and self.config['LSA_Concepts']:
            warnings.warn("NEED LATENT SEMANTIC ANALYSIS TO RUN LSA CONCEPTS")
            
        if not self.config['latent_semantic_analysis'] and self.config['kmeans']:
            warnings.warn("NEED LATENT SEMANTIC ANALYSIS TO RUN KMEANS")
     
        

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
             
                
        if not self.config['bag_of_words'] and self.config['word_frequency_table']:
            warnings.warn("NEED BAG OF WORDS TO RUN WORD FREQUENCY TABLE")
            

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
            
            
        if not self.config['bag_of_words'] and self.config['LDA']:
            warnings.warn("NEED BAG OF WORDS TO RUN Latent Dirchlet Allocation")
          
            
        
        if self.config['LDA'] and self.config['bag_of_words']:
            lda = LDA(self.corpus, self.config['LDA'])
            lda.run()
            result_dict['LDA'] = lda.output
       
            

        output_text = ""
        self.results = result_dict
        for alg,result in result_dict.items():
            output_text += "\n\nalgorithm: {}\n\nresult:\n\n {}\n\n".format(alg,result)


        print(output_text)
        return result_dict



# Base class for Vector Space Models (Bag of Words, LSA, LDA, Word2Vec, Doc2Vec)
class VectorSpaceModels(object):
    
    def __init__(self, corpi):
        self.corpi = corpi
        self.dtm = None
        self.vectorizer = None
        self.doc_ids = []

class BagOfWords(VectorSpaceModels):
  
     def __init__(self, corpi):
        super().__init__(corpi)
        self.bow = None
        print('\n\n\n\nRunning the following algorithm: \nBag of Words\n\n')
        
     def run(self):
        """Vectorizes words and fits words to a matrix."""

        self.vectorizer = CountVectorizer(lowercase = False, stop_words = 'english') #, preprocessor = None, tokenizer = None
        self.dtm = self.vectorizer.fit_transform(self.corpi)
 
        vocabulary = self.vectorizer.vocabulary_  # dict of unique word, index key-value pairs 

        sorted_by_value = sorted(vocabulary.items(), key=lambda kv: kv[1])

        sorted_vocab = [k for k,v in sorted_by_value]

        dtm_array = sum(self.dtm.toarray())  # [sum(x) for x in zip(list1, list2)]

        self.output = {word:freq for word,freq in zip(sorted_vocab, dtm_array)}


class WordFreq(VectorSpaceModels):
    """Initiates Word Frequency table: outputs how many times a word occurs."""
    
    """Used to output Bag of Words as a DataFrame."""
    
    def __init__(self, corpi, bow_output):
        super().__init__(corpi)
        print('\n\n\n\nRunning the following algorithm: \nWord Frequency\n\n')
        # print('bow output\n', bow_output)
        self.bow_output = bow_output
        self.output = None
        self.run()
    
    def run(self):
        """Takes Bag of Words and outputs into table."""
        
        bow_series = pd.Series(self.bow_output)
        bow_data = bow_series.to_frame().reset_index()
        bow_data.columns = ['Word', 'Word Count']
        self.output = bow_data.sort_values(by='Word Count', ascending=False)

class LatentSemanticAnalysis(VectorSpaceModels):
    """Initiates LSA: computing document similarity. """

    def __init__(self, corpi):
        super().__init__(corpi)
        print('\n\n\n\nRunning the following algorithm: \nLatent Semantic Analysis\n\n')


    def run(self):
        """Data goes through dimensionality reduction with cosine similarity and returns lsa."""

        self.vectorizer = TfidfVectorizer(stop_words = None, lowercase=False)
        print('\n\n\n\nTFIDF vectorizer', self.vectorizer)
        self.dtm = self.vectorizer.fit_transform(self.corpi)
        self.lsa = TruncatedSVD(n_components=200)  # , algorithm = 'arpack')
        self.dtm_lsa = self.lsa.fit_transform(self.dtm)
        self.dist = 1 - cosine_similarity(self.dtm_lsa)
        
        for corpus in self.corpi.corpus_list:
            self.doc_ids.extend(corpus.doc_ids)
            
        # dataframe = pd.DataFrame(lsa.components_, index=["component_1","component_2"], columns=self.vectorizer.get_feature_names())
        self.output = {'dtm': self.dtm,
                       'dtm_lsa': self.dtm_lsa,
                       'doc_ids': self.doc_ids}
        
class LSA_Concepts(VectorSpaceModels):
    """Analyzes the conceptual ideas within the data."""
    
    def __init__(self, corpi, dtm_lsa, lsa, vectorizer):
        super().__init__(corpi)
        
        self.dtm_lsa = dtm_lsa
        self.lsa = lsa
        self.vectorizer = vectorizer
        
    def run(self):
        """Vectorizes data and returns the top concepts in each documents."""
        
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
    """Initiates k-means: clustering data according to means."""
    

    def __init__(self, corpi, dtm_lsa):
        super().__init__(corpi) 
        self.dtm_lsa = dtm_lsa
        
    def run(self):
        """Function of k-means that fits data into matrix and clusters the data."""
        
        km_dict = dict()
        max_clusters = 5
        for index in range(2,max_clusters + 1):
            km = KMeans(n_clusters = index,  init = 'k-means++', max_iter = 1000, random_state = 1423)
            km.fit(self.dtm_lsa)
            clusters = km.labels_.tolist()
            km_dict[index] = Counter(clusters)
            self.output = (index, Counter(clusters))



class Tf_Idf(VectorSpaceModels):
    """Initiates Tf-Idf algorithm: compares word frequency in a collection of documents."""
    
    def __init__(self, corpi):
        super().__init__(corpi)
        self.output = None
        print('\n\n\n\nRunning the following algorithm: \nTFIDF \n\n')
        
    def run(self):
        """Vectorizes the words."""
        
        #figure out how to link up with preprocess
        self.vectorizer = TfidfVectorizer(stop_words=None, lowercase=False, encoding='utf-8')
        
        #Tranforms corpus into vectorized words
        self.dtm = self.vectorizer.fit_transform(self.corpi)
        
        #Prints idf'd words
        #print(self.dtm.get_feature_names())
        
        #Prints doc-term matrix
        #print(self.dtm)
        
        """Returns Data Table of doc-term matrix."""
        Tf_Idf_Table = pd.DataFrame(self.dtm.toarray())
        self.output = Tf_Idf_Table

    
class LDA(VectorSpaceModels):
    """Initiates Latent Dirichlet Allocation algorithm: shows how much a bag of words represents different topics"""
    
    def __init__(self, corpus, num_topics):
        super().__init__(corpus)
        self.output = []
        self.num = num_topics
        print('\n\n\n\nRunning the following algorithm: \nLatent Dirichlet Allocation \n\n')
        
    def run(self):
        
        tokens = []
        for text in self.corpus:
            tokens.append(word_tokenize(text))
        
        # Create a corpus from a list of texts
        common_dictionary = Dictionary(tokens)
        
        common_corpus = [common_dictionary.doc2bow(text) for text in tokens]
        
        # Train the model on the corpus.
        lda = gensim.models.ldamodel.LdaModel(tokens, num_topics=self.num)
        self.output = lda.show_topics(num_topics = self.num, num_words = 8)
 
        for i in range(0, lda.num_topics):
    
        
            for word, prob in lda.show_topic(i, topn=20):
                print(word, prob)
        #other_corpus = common_dictionary.doc2bow(self.bow) # for text in other_texts] #needs txt as dict
        
        #vector = lda[common_corpus]
        
        
        
        #for v in vector:
          #self.output.append(v)

        
# Base class for Topic Models (Topic Modelingm Named Entity Recognition, etc.)
class TopicModels(object):
    
    """Parent Class for Named Entity Recognition"""

    
    def __init__(self, corpi):
        self.corpus = corpi

class Named_Entity_Recognition(TopicModels):
    """Initiates NER: identifies categories such as names, organizations, locations, etc."""
    
    """This takes in a document strings and obtains the Named Entities from each. """
    
    def __init__(self, corpi):
        super().__init__(corpi)
        print('\n\n\n\nRunning the following algorithm: \nNamed_Entity_Recognition\n\n')
        
        self.output = []
        
    def run(self):
        """Chunks docs and adds named entities to a list."""
        
        for item in self.corpus:
                chunked_docs = []
                chunked = ne_chunk(pos_tag(word_tokenize(item)))
                chunked_docs.append(chunked)
                continuous_chunk = []
                current_chunk = []
                for chunk in chunked_docs:
                    
                    for i in chunk:
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

