
import utilities
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk import pos_tag



class Preprocessor(object):
    """This holds all the preprocessing which includes removes stop words, lowercases, removes punctuation, and removes symbols. It then has options to either lemmatizes or stem or neither.  """
    
    def __init__(self, corpus, config_file):
        
        self.corpus = corpus
        self.config = utilities.get_config(config_file)
        
        #self.file_names = self.corpus.get_file_names()
        

        print('\n\n\n\nRunning the following preprocessing actions:\n\n')
        print(self.config)

        self.stop = list(set(stopwords.words('english')))
        self.tokenized_docs = []
        self.named_entities_list = []
        
        
    def run(self):

        if self.config['new_stop_set_list']:    
            self.stop = self.config['new_stop_set_list']
            
        if self.config['add_stop_list']:            
            self.stop.extend(self.config['add_stop_list'])
            
        if self.config['remove_stop_list']:            
            self.stop = list(set(self.stop) - set(self.config['remove_stop_list']))
        
        tokens = word_tokenize(self.corpus)
        if self.config['lemmatize']:  
            tokens = pos_tag(tokens)
            tokens = [t[0].lower() for t in tokens]              
            tokens = [t for t in tokens if t[0].isalpha() and t[0] not in self.stop]
        else:
            tokens = [t.lower() for t in tokens]              
            tokens = [t for t in tokens if t.isalpha() and t not in self.stop]   
         
             
        self.token_list = []
        
        
        
        if self.config['PorterStemmer']:
            stem_tool = PorterStemmer()
            
        if self.config['SnowballStemmer']:
            stem_tool = SnowballStemmer('english')
        

        if not self.config['lemmatize']: 
            stem_words = []
            for item in tokens:
                stem_words.append(stem_tool.stem(item))
            self.output = stem_words

        if self.config['lemmatize']:
            wordnet_lemmatizer = WordNetLemmatizer()
            lem_words = []
            for item in tokens:
                if len(item) < 2:
                    position = 'n'
                elif item[1].startswith('VB'):
                    position = 'v'
                elif item[1] == 'JJ':
                    position = 'a'
                elif item[1] == 'RB':
                    position = 'r'
                else:
                    position = 'n'
                lemmatized = wordnet_lemmatizer.lemmatize(item, pos = position)
                lem_words.append(lemmatized)
            self.output = lem_words
            
        return ' '.join(self.output)
        
        

