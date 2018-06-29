import inspect
import utilities
from sklearn.feature_extraction.text import CountVectorizer
import pandas as pd

class Algorithm(object):
    
    def __init__(self, corpus, config):
        self.corpus = corpus
        self.config = utilities.get_config(config)
        print('\n\n\nalg config:\n\n', self.config)
        
    def __iter__(self):
        for item in self.corpus:
            yield item

    def run(self):
        result_dict = {}
        
        if 'bag_of_words' in self.config:
            b = BagOfWords(self.corpus, self.config)
            b.run()
            result_dict['bag_of_words'] = b.output
            
            if 'word_frequency' in self.config:
                w = WordFreq(self.corpus, self.config, b.output)
                w.run()
                result_dict['word_frequency'] = w.output
                

        print(result_dict)
        return result_dict



# Base class for Vector Space Models (Bag of Words, LSA, LDA, Word2Vec, Doc2Vec)
class VectorSpaceModels(object):
    
    def __init__(self, 
                 corpus, config):
        self.config = config
        self.corpus = corpus
        self.dtm = None
        self.dtm_dense = None
        self.vocabulary = None
       
        
class BagOfWords(VectorSpaceModels):
    
     def __init__(self, corpus, config):
        super().__init__(corpus, config)
        
     def run(self):  
        vectorizer = CountVectorizer(lowercase=True, stop_words='english')
        dtm = vectorizer.fit_transform(self.corpus)
        dtm_dense = dtm.todense()
        vocabulary = vectorizer.vocabulary_
        
        # inspecing the program stack to get the calling functions name so we don't have to hardcode it
        # when building our output
        self.output = {'dtm': dtm,'dtm_dense': dtm_dense,'vocabulary': vocabulary}
    
        
        

        
class WordFreq(BagOfWords):
    
    def __init__(self, corpus, config, output):
        super().__init__(corpus, config)
        self.output = output
        #self.run()
    
    def run(self):
        bow_series = pd.Series(self.output['vocabulary'])
        bow_data = bow_series.to_frame().reset_index()
        bow_data.columns = ['Word', 'Word Count']
        bow_max = bow_data.sort_values(by='Word Count', ascending=False)
        bow_max = bow_max.set_index('Word')
        self.output = bow_max


class LatentSemanticAnalysis(VectorSpaceModels):

    def __init__(self):
        super.__init__()
        
 
# Base class for Topic Models (Topic Modelingm Named Entity Recognition, etc.)
class TopicModels(object):
    pass
        
        
    