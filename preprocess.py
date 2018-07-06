# -*- coding: utf-8 -*-
import utilities

#import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer, SnowballStemmer
from nltk import pos_tag


#use mapping
#dont use of list of list, use dict perhaps


class Preprocessor(object):

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
            
                
        '''
        for item in self.corpus:
            tokens = word_tokenize(item)
            if self.config['lemmatize']:  
                tokens = pos_tag(tokens)
                tokens = [t[0].lower() for t in tokens]              
                tokens = [t for t in tokens if t[0].isalpha() and t[0] not in self.stop]
            else:
                tokens = [t.lower() for t in tokens]              
                tokens = [t for t in tokens if t.isalpha() and t not in self.stop]   
        
            self.tokenized_docs.append(tokens)        
        '''
        self.token_list = []
        
        
        
        if self.config['PorterStemmer']:
            stem_tool = PorterStemmer()
            
        if self.config['SnowballStemmer']:
            stem_tool = SnowballStemmer('english')
            
        if self.config['PorterStemmer'] or self.config['SnowballStemmer']:
            stem_words=[]
            
            stem_words.append([stem_tool.stem(item) for item in tokens])
                
 #               for item in tokens:
                    #[map(lambda x:x+1 ,group) for group in self.tokenized_docs]
#                    stem_words.append(stem_tool.stem(item))
                    
                #self.token_list.append(stem_words)
                #stem_words = []
            self.output = stem_words #dict(zip(self.file_names, self.token_list))
            return self.output

        if self.config['lemmatize']:
            #figure out pos_tagging
            # we can specify part of speech (pos) value like below:
            # noun = n, verb = v, adjective = a, adverb = r
            wordnet_lemmatizer = WordNetLemmatizer()
            lem_words = []
            #faster with list comprehnsion
            #for tokens in self.tokenized_docs:
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
                #self.token_list.append(lem_words)
                #lem_words = []
            self.output = lem_words#dict(zip(self.file_names, self.token_list))
            return self.output
        
        

