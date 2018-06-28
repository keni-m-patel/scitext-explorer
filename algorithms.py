import inspect
import utilities
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

class Algorithm(object):
    
    def __init__(self, data, config_file):
        self.data = data
        self.config = utilities.get_config(config_file)
        print('\n\n\nalg config:\n\n', self.config)
        
    def __iter__(self):
        for item in self.data:
            yield item

    def run(self):
        result_dict = {}
        
        if 'bag_of_words' in self.config:
            b = BagOfWords(self.data)
            b.run()
            result_dict['bag_of_words'] = b.output
            
        if 'LSA' in self.config:
            print('\n\nERROR: LSA not yet implemented\n\n')

        print(result_dict)
        return result_dict



# Base class for Vector Space Models (Bag of Words, LSA, LDA, Word2Vec, Doc2Vec)
class VectorSpaceModels(object):
    
    def __init__(self, 
                 corpus):
        self.corpus = corpus
        self.dtm = None
        self.dtm_dense = None
        self.vocabulary = None

        
class BagOfWords(VectorSpaceModels):
    
     def __init__(self, corpus):
        super().__init__(corpus)
        
     def run(self):  
        vectorizer = CountVectorizer(lowercase=True, stop_words='english')
        dtm = vectorizer.fit_transform(self.corpus)
        dtm_dense = dtm.todense()
        vocabulary = vectorizer.vocabulary_
        
        # inspecing the program stack to get the calling functions name so we don't have to hardcode it
        # when building our output
        self.output = {'dtm': dtm,'dtm_dense': dtm_dense,'vocabulary': vocabulary}
        
        if 'word_frequency' in self.config:
            wordfreq = WordFreq(self.data)
            wordfreq.run_word_freq()
        

        
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
        print(bow_max)

class LatentSemanticAnalysis(VectorSpaceModels):

    def __init__(self):
        super.__init__()
        
 
# Base class for Topic Models (Topic Modelingm Named Entity Recognition, etc.)
class TopicModels(object):
    pass
        
        
    