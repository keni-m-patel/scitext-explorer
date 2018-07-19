
import utilities
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk import pos_tag
import os
import re
import warnings




class Preprocessor(object):


    """This holds all the preprocessing which includes removes stop words, lowercases, removes punctuation, and removes symbols. It then has options to either lemmatizes or stem or neither.  """
    

    def __init__(self, data, config_file, files):
        
        #data represents a single doc (or page, tweet, ect.)
        self.data = data
        
        #connects to preprocess config file
        self.config = utilities.get_config(config_file)
        
        
        #self.file_names  = [os.path.basename(x) for x in files]
        
        self.regex = self.config['regex_stopwords']

        #if there is nothing found in the file program gives a warning
        if not self.file_names:
            warnings.warn('\n\nERROR: no files selected, must select at least one file to process, exiting program\n\n')
            

        # print('\n\n\n\nRunning the following preprocessing actions:\n\n')
        # print(self.config)
        
        #if chooses default stop list, gives english stopword set from nltk
        if self.config['default_stop_list']:
            self.stop = list(set(stopwords.words('english')))
            
        #if default stopword list is not chosen, allows user to create their own from scratch
        else:
            self.stop = []
            
        
        
    def run(self):
        
        
        '''
        #if named entities chosen, named entities is returned as the data output
        if self.config['named_entities']:
            
            #if  choose named entities but did not set undergo preprocess to false gives a warning because will not run NER properly
            if self.config['undergo_preprocess']:
                warnings.warn("NEED TO TURN OFF PREPROCESS TO RUN NAMED ENTITY RECOGNITION")
            
            #NER runs
            else:
                ner = Named_Entity_Recognition(self.data)
                ner.run()
                self.data = ner.output
        '''
                
                
        #if choose not to undergo preprocess automatically returns data unchanged
        #if NER selected, returns named entities for the data
        if not self.config['undergo_preprocess']:
            return self.data

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
        
        #goes through necessary preprocessing if going to lemmatize
        if self.config['lemmatize']:  
            
            #part of speech tags words
            tokens = pos_tag(tokens)
            
            #lowercases words if set to true
            if self.config['lowercase']:
                tokens = [t[0].lower() for t in tokens]
                
            #gets rid of punctuation if set to true
            if self.config['alpha_only']:
                tokens = [t for t in tokens if t[0].isalpha()]   #and t[0] not in self.stop]
            
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
        
        
        #stems words with porterstemmer from nltk
        if self.config['PorterStemmer']:
            stem_tool = PorterStemmer()
            
        #stems words with snowballstemmer from nltk
        if self.config['SnowballStemmer']:
            stem_tool = SnowballStemmer('english')

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

        #returns the list of preprocessed words as a string in order to work with algorithms
        return ' '.join(self.output)


'''
class Named_Entity_Recognition(object):
    
    """This takes in a document strings and obtains the Named Entities from each. """
    
    def __init__(self, data):
        self.data = data
        print('\n\n\n\nRunning the following algorithm: \nNamed_Entity_Recognition\n\n')
        
        self.output = []
        self.test = []
        
    def run(self):
        for item in self.data:
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

'''