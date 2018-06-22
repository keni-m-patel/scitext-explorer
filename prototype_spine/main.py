"""
Created on Wed Jun 20 12:30:52 2018

@author: sonj@mit.edu
"""

### NOTES ###
'''
this is the main file for the prototype system.
main.py will read through the config file, pick out the parameters, 
and then execute the correct files from algs, visualization, and preprocessing (all directories)
using those parameters.
'''

### CODE ###

# (modified from Keni's read_config_file.py)


### CONSTANTS ###
DEBUG = 1  # if true, print debugging statements
DATA_PATH = 'data/'

### IMPORTS ###
# config
import yaml

# preprocessing
from preprocessing import pre_process_functions
from pre_process_functions import complete_tokenize, stem_tokens, lemma as lemmatize_tokens

# algs
from algorithms import BOW
from BOW import bow_from_tokens

# viz
# from visualization import viz_functions as viz
# from viz import make_word_cloud as mwc





def read_config_file():
    
    # open master config file for (currently) 1 key dict on which config file to use
    with open('config.yaml', 'r') as filestream:
        config = yaml.load(filestream)

    user_config = config[user]

    if DEBUG:
        print('master config file type: {}\n'.format(type(config)) + '\n')
        print('master config dict (k,v) pairs: ', str([(k,config[k]) for k in config.keys()]) )

    # now open the config file specified by the master config dict
    with open(user_config, 'r') as filestream:
        user_config = yaml.load(filestream)

    if DEBUG:
        print('user config file type: {}\n'.format(type(user_config)) + '\n')
        print('user config dict (k,v) pairs: ', str([(k,user_config[k]) for k in user_config.keys()]) )

    # extract each section's parameters as list or dict
    user_data_path = user_config['data']
    preprocessing = user_config['preprocessing']
    algorithms = user_config['algorithms']
    visualization =  user_config['visualization']

    return user_data_path, preprocessing, algorithms, visualization


def preprocess_data(user_data_path, preprocessing, algorithms, visualization)
    path = DATA_PATH + user_data_path
    # text import, get list of string, each is a document 
    files_as_strings = text_import(path)
    output = files_as_strings
    
    # we can make this better-organized later...
    # later this will have multiple if statements , or some other way of organizing
    # do this for each possibility
    if preprocessing['complete_tokenize']:
        output = complete_tokenize(output)
        
    if preprocessing['stem']:
        output = stem_tokens(output)
    elif preprocessing['lemmatize']:
        output = lemmatize_tokens(output)

    return output # this will be a list of lists of tokens, each list represents a document's tokens


def apply_algorithms(data):
    output = data
    # do algs
    if algorithms['BOW']:
        output = bow_from_tokens(output)
        print(output)
    # apply other algs/have more options here
    else:
        print('NO ALG SELECTED')
        print('input: ', data)
        print('algs selected: ', algorithms)

    return output


def run_visualizations(data):
    output = data

    # this needs to be put into
    # do viz
    if visualization['WordCloud']:
        # mwc()
        # import and apply WC alg
        # immport WC_viz function
        # output = WC_viz(processed_data)

    # apply other visualizations maybe??

    return output




if __name__ == '__main__':
    d,p,a,v = read_config_file()
    # do preprocessing
    processed_data = preprocess_data(d,p,a,v)
    algs_done_data = apply_algorithms(processed_data)
    return run_visualizations(algs_done_data)

    # do algs
    # do visualization



















