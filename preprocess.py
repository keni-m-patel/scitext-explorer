# -*- coding: utf-8 -*-
import utilities

#import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer


#use mapping
#dont use of list of list, use dict perhaps


class Preprocessor(object):

    def __init__(self, corpus, config_file, file_names):

        self.corpus = corpus
        self.config = utilities.get_config(config_file)
        self.file_names = file_names

        print('\n\n\n\nRunning the following preprocessing actions:\n\n')
        print(self.config.keys())

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
        
        for item in self.corpus:            
            tokens = word_tokenize(item)
            tokens = [t.lower() for t in tokens]              
            tokens = [t for t in tokens if t.isalpha() and t not in self.stop]        
            #alpha_only = [t for t in lower_tokens if t.isalpha()]
            #no_stops = [w for w in alpha_only if w not in self.stop] 
            
            #if self.config['lemmatize']:  
                #no_stops = pos_tag(no_stops)
    
            self.tokenized_docs.append(tokens)        
            # print(self.tokenized_docs)        
        self.token_list = []
        

        if self.config['stem']:  
            print('hello')
            ps = PorterStemmer()
            stem_words=list()
            for tokens in self.tokenized_docs:
                for item in tokens:
                    #[map(lambda x:x+1 ,group) for group in self.tokenized_docs]
                    stem_words.append(ps.stem(item))
                self.token_list.append(stem_words)
                stem_words = list()
            self.output = dict(zip(self.file_names, self.token_list))
            return self.output

        if self.config['lemmatize']:
            print('success')
            #figure out pos_tagging
            wordnet_lemmatizer = WordNetLemmatizer()
            lem_words = list()
            #faster with list comprehnsion
            for tokens in self.tokenized_docs:
                for item in tokens:
                    #if item[1] == 'VB':
                    lemmatized = wordnet_lemmatizer.lemmatize(item) #, pos = item[1]
                    lem_words.append(lemmatized)
                self.token_list.append(lem_words)
                lem_words = list()
            self.output = dict(zip(self.file_names, self.token_list))
            return self.output
        
        
    

    
    