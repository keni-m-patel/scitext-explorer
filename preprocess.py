
import utilities
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk import pos_tag
import os
import re




class Preprocessor(object):


    """This holds all the preprocessing which includes removes stop words, lowercases, removes punctuation, and removes symbols. It then has options to either lemmatizes or stem or neither.  """
    

    def __init__(self, corpus, config_file, files):

        self.corpus = corpus
        self.config = utilities.get_config(config_file)
        self.file_names = [os.path.basename(x) for x in files]
        self.regex = self.config['regex_stopwords']

        if not self.file_names:
            print('\n\nERROR: no files selected, must select at least one file to process, exiting program\n\n')
            return

        # print('\n\n\n\nRunning the following preprocessing actions:\n\n')
        # print(self.config)
        if self.config['default_stop_list']:
            self.stop = list(set(stopwords.words('english')))
        else:
            self.stop = []
        self.tokenized_docs = []
        self.named_entities_list = []
        
        
    def run(self):
        
        if not self.config['undergo_preprocess']:
            
            '''
            if self.config['named_entities']:
                ner = Named_Entity_Recognition(self.corpus)
                ner.run()
                self.corpus = ner.output
                '''

            return self.corpus

        if self.config['new_stop_set_list']:    
            self.stop = self.config['new_stop_set_list']
            
        if self.config['add_stop_list']:            
            self.stop.extend(self.config['add_stop_list'])
            
        if self.config['remove_stop_list']:            
            self.stop = list(set(self.stop) - set(self.config['remove_stop_list']))

        if self.regex:
                self.corpus = re.sub(self.regex, "", self.corpus)


        
        tokens = word_tokenize(self.corpus)
        
        if self.config['lemmatize']:  
            tokens = pos_tag(tokens)
            if self.config['lowercase']:
                tokens = [t[0].lower() for t in tokens]
            if self.config['alpha_only']:
                tokens = [t for t in tokens if t[0].isalpha()]   #and t[0] not in self.stop]
            tokens = [t for t in tokens if t[0] not in self.stop]
                

        else:
            if self.config['lowercase']:
                tokens = [t.lower() for t in tokens]    
            if self.config['alpha_only']:
                tokens = [t for t in tokens if t.isalpha()]  #and t not in self.stop]   
            
            tokens = [t for t in tokens if t not in self.stop]
         
             
        self.token_list = []
        
        
        
        if self.config['PorterStemmer']:
            stem_tool = PorterStemmer()
            
        if self.config['SnowballStemmer']:
            stem_tool = SnowballStemmer('english')

        if ((self.config['PorterStemmer'] or self.config['SnowballStemmer']) and not self.config['lemmatize']): 
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


'''
class Named_Entity_Recognition(object):
    
    """This takes in a document strings and obtains the Named Entities from each. """
    
    def __init__(self, corpus):
        self.corpus = corpus
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