# move main.py's logic/extra code here

### CONSTANTS ###
DEBUG = 0 # if true, print debugging statements
USER_EX = 1
DATA_PATH = 'data/'
CONFIG_PATH = 'configuration/'

### IMPORTS ###

# config
import yaml

# preprocessing
from preprocessing.pre_process_functions import text_import, complete_tokenize, stem_tokens, lemma as lemmatize_tokens

# algs
from algorithms.algorithms_functions import bow as bow_from_tokens

# viz
from visualization.viz_functions import multiple_bow_to_wordcloud, bow_to_dataframe




def read_config_file():
    
    # open master config file for (currently) 1 key dict on which config file to use
    with open(CONFIG_PATH + 'config.yaml', 'r') as filestream:
        config = yaml.load(filestream)

    user_config = config['user_configuration']

    if DEBUG:
        print('master config file type: {}\n'.format(type(config)) + '\n')
        print('master config dict (k,v) pairs: ', str([(k,config[k]) for k in config.keys()]) )

    # now open the config file specified by the master config dict
    with open(CONFIG_PATH + user_config, 'r') as filestream:
        user_config = yaml.load(filestream)

    if DEBUG:
        print('user config file type: {}\n'.format(type(user_config)) + '\n')
        print('user config dict (k,v) pairs: ', str([(k,user_config[k]) for k in user_config.keys()]) )

    # extract each section's parameters as list or dict
    user_data_path = DATA_PATH + user_config['data']
    preprocessing = user_config['preprocessing']
    user_algs= user_config['algorithms']
    visualization =  user_config['visualization']

    return user_data_path, preprocessing, user_algs, visualization


def preprocess_data(path, prepro_selections):

    # text import, get list of string, each is a document 
    files_as_strings = text_import(path)
    output = files_as_strings
    if DEBUG:
        print('\n\n\nfiles as strings:\n\n', files_as_strings)
    
    # we can make this better-organized later...
    # later this will have multiple if statements , or some other way of organizing
    # do this for each possibility
    if prepro_selections['complete_tokenize']:
        output = complete_tokenize(output)
        if DEBUG:
            print('\n\n\ncomplete_tokenize output:\n\n', output)
        
    if prepro_selections['stem']:
        output = stem_tokens(output)
        if DEBUG:
            print('\n\n\nstem_tokens output:\n\n', output)
    elif prepro_selections['lemmatize']:
        output = lemmatize_tokens(output)
        if DEBUG:
            print('\n\n\nlemmatize_tokens output:\n\n', output)

    return output # this will be a list of lists of tokens, each list represents a document's tokens


def apply_algorithms(data, alg_selections):
    output = data
    # do algs
    if alg_selections['BOW']:
        output = bow_from_tokens(output)
        if DEBUG:
            print('\n\n\nbow applied output:', output)
    # apply other algs/have more options here
    else:
        print('\n\n\nNO ALG SELECTED')
        print('\n\n\ninput: \n\n', data)
        print('\n\n\nalgs selected: \n\n', user_algs)

    return output


def run_visualizations(data, viz_selections, user_data_path):
    output = data

    # this needs to be put into
    # do viz
    if viz_selections['WordCloud']:

        output = multiple_bow_to_wordcloud(output)

        if DEBUG:
            print('\n\n\nWordCloud output:', output)

    elif viz_selections['FrequencyTable']:
        # do a thing
        output = bow_to_dataframe(output, user_data_path)


    # apply other visualizations maybe??
    return output