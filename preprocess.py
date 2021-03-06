import utilities
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk import pos_tag
import re
import warnings

class Preprocessor(object):


    """This holds all the preprocessing which includes removes stop words, lowercases, removes punctuation, and removes symbols. It then has options to either lemmatizes or stem or neither.  """
    

    def __init__(self, data, config_file):
        #data represents a single doc (or page, tweet, ect.)
        self.data = data
        
        #connects to preprocess config file
        self.config = utilities.get_config(config_file)
        
        self.regex = self.config['regex_stopwords']
        
    def run(self):
        #if choose not to undergo preprocess automatically returns data unchanged
        #if NER selected, returns named entities for the data
        if not self.config['undergo_preprocess']:
            return self.data
        
        #if chooses default stop list, gives english stopword set from nltk
        if self.config['default_stop_list']:
            self.stop = list(set(stopwords.words('english')))
            
        #if default stopword list is not chosen, allows user to create their own from scratch
        else:
            self.stop = []
            
        #adds brand new user implemented stopset
        if self.config['new_stop_set_list']:    
            self.stop = self.config['new_stop_set_list']
        
        #adds stop words
        if self.config['add_stop_list']:            
            self.stop.extend(self.config['add_stop_list'])
        
        #remove stop words
        if self.config['remove_stop_list']:            
            self.stop = list(set(self.stop) - set(self.config['remove_stop_list']))

        #allows user to enter their own regex expression to remove words from the data
        if self.regex:
                self.data = re.sub(self.regex, "", self.data)


        #tokenizes words
        tokens = word_tokenize(self.data)
        
        
        if ((self.config['PorterStemmer'] or self.config['SnowballStemmer']) and self.config['lemmatize']): 
            warnings.warn("CHOSE BOTH LEMMATIZING AND STEMMING. ONLY LEMMATIZING WILL BE DONE!")
            
            
        #goes through necessary preprocessing if going to lemmatize
        if self.config['lemmatize']:  
            
            #part of speech tags words
            tokens = pos_tag(tokens)
            #lowercases words if set to true
            if self.config['lowercase']:
                tokens = [(t[0].lower(), t[1]) for t in tokens]
                
            #gets rid of punctuation if set to true
            if self.config['alpha_only']:
                tokens = [t for t in tokens if t[0].isalpha()]
                
            #gets rid of stop words
            tokens = [t for t in tokens if t[0] not in self.stop]
            
            
        #goes through necessary preprocessing steps for stemming
        else:
            
            #lowercases words if set to true
            if self.config['lowercase']:
                tokens = [t.lower() for t in tokens]   
                
            #gets rid of punctuation if set to true
            if self.config['alpha_only']:
                tokens = [t for t in tokens if t.isalpha()]  #and t not in self.stop]   
            
            #gets rid of stop words
            tokens = [t for t in tokens if t not in self.stop]
         
             
        self.token_list = []
        
        
        if self.config['PorterStemmer'] and self.config['SnowballStemmer']:
             warnings.warn("CHOSE BOTH PorterStemmer AND SnowballStemmer. ONLY PorterStemmer WILL BE DONE!")
            
            
        #stems words with snowballstemmer from nltk
        if self.config['SnowballStemmer']:
            stem_tool = SnowballStemmer('english')
            
        #stems words with porterstemmer from nltk
        if self.config['PorterStemmer']:
            stem_tool = PorterStemmer()

        #appends stemmed words to a list
        if ((self.config['PorterStemmer'] or self.config['SnowballStemmer']) and not self.config['lemmatize']): 
            stem_words = []
            for item in tokens:
                stem_words.append(stem_tool.stem(item))
            self.output = stem_words

        #lemmatizes words with wordnetlemmatizer from nltk
        if self.config['lemmatize']:
            wordnet_lemmatizer = WordNetLemmatizer()
            lem_words = []
            
            #correctly sets each part of speech
            for item in tokens:

                if item[1].startswith('VB'):
                    position = 'v'
                elif item[1] == 'JJ':
                    position = 'a'
                elif item[1] == 'RB':
                    position = 'r'
                else:
                    position = 'n'
                lemmatized = wordnet_lemmatizer.lemmatize(item[0], pos = position)
                lem_words.append(lemmatized)

            self.output = lem_words

        #returns the list of preprocessed words as a string in order to work with algorithms
        
        return ' '.join(self.output)
