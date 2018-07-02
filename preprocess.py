# -*- coding: utf-8 -*-
import utilities

#import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.stem import PorterStemmer
from nltk import ne_chunk, pos_tag
from nltk.tree import Tree







class Preprocessor(object):

    

    def __init__(self, corpus, config_file):

        self.corpus = corpus

        self.config = utilities.get_config(config_file)
        print('\n\n\n\nRunning the following preprocessing actions:\n\n')
        print(self.config)
        
        self.stop = list(set(stopwords.words('english')))
        
        self.tokenized_docs = []
        
        self.named_entities_list = []
        
        
    def run(self):
        
        if self.config['new_stop_set']:
            
            self.stop = self.config['new_stop_set_list']
            
        if self.config['add_stop']:
            
            self.stop.extend(self.config['add_stop_list'])
            
        if self.config['remove_stop']:
            
            self.stop = list(set(self.stop) - set(self.config['remove_stop_list']))
        
        for item in self.corpus:
            
            tokens = word_tokenize(item)
                
            lower_tokens = [t.lower() for t in tokens]        

            alpha_only = [t for t in lower_tokens if t.isalpha()]

            no_stops = [w for w in alpha_only if w not in self.stop] 
            
            #if not self.config['stem']:
                
                #no_stops = pos_tag(no_stops)
    
            self.tokenized_docs.append(no_stops)
        
            print(self.tokenized_docs)
        
        self.output = []
        
            
        if self.config['stem']:
            
            ps = PorterStemmer()
            stem_words=list()
            for tokens in self.tokenized_docs:
                for item in tokens:
                    stem_words.append(ps.stem(item))
                self.output.append(stem_words)
                stem_words = list()
            return self.output


        else:
            #figure out pos_tagging
            wordnet_lemmatizer = WordNetLemmatizer()
            lem_words = list()
            for tokens in self.tokenized_docs:
                for item in tokens:
                    #if item[1] == 'VB':
                    lemmatized = wordnet_lemmatizer.lemmatize(item) #, pos = item[1]
                    lem_words.append(lemmatized)
                self.output.append(lem_words)
                lem_words = list()
            return self.output
        
        
        
        if self.config['named_entities']:
            for item in self.corpus:
                chunked_docs = []
                chunked = ne_chunk(pos_tag(word_tokenize(item)))
                chunked_docs.append(chunked)
                continuous_chunk = []
                current_chunk = []
                for chunk in chunked_docs:
                    for i in chunked:
                        if type(i) == Tree:
                            current_chunk.append(" ".join([token for token, pos in i.leaves()]))
                        elif current_chunk:
                            named_entity = " ".join(current_chunk)
                            if named_entity not in continuous_chunk: 
                                continuous_chunk.append(named_entity)
                                current_chunk = []
                        else:
                            continue
                        self.named_entities_list.append(continuous_chunk)
                print(self.named_entities_list)
            return self.named_entities_list

    
    