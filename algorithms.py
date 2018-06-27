import inspect
import utilities
from sklearn.feature_extraction.text import CountVectorizer


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
        self.output = {inspect.stack()[0][3]: {'dtm': dtm,
                               'dtm_dense': dtm_dense,
                               'vocabulary': vocabulary}}
 

class LatentSemanticAnalysis(VectorSpaceModels):

    def __init__(self):
        super.__init__()
        
 
# Base class for Topic Models (Topic Modelingm Named Entity Recognition, etc.)
class TopicModels(object):
    pass
        
        
    