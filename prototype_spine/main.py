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

### IMPORTS ###
import yaml
import glob # ?? import here or in each file??
from preprocessing import text_import as timp, complete_tokenize as ctknz
from algorithms import BOW



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
    data = user_config['data']
    preprocessing = user_config['preprocessing']
    algorithms = user_config['algorithms']
    visualization =  user_config['visualization']

    return data, preprocessing, algorithms, visualization

def preprocess_data(data, preprocessing, algorithms, visualization)

    # ASSUMPTION: for now we assume only one text file inputted, 
    #             but text will be a list of strings that are filenames

    path  = 'data/{}'.format(text)

    if DEBUG:
        print(path, filenames)



    # text import/text to string
    files_as_strings = text_import(path, text)
    output = files_as_strings
    

    # we can make this better-organized later...
    # later this will have multiple if statements , or some other way of organizing
    # do this for each possibility
    if preprocessing['complete_tokenize']:
        ## IMPORT step from preprocessing file
        import complete_tokenize
        output = complete_tokenize(files_as_strings)

    # if preprocessing['stopwords']:
    #    do this other thing ...

    # for 



    return output


def apply_algorithms(data):

    # do algs
    if algorithms['BOW']:
        # import and apply BOW alg
        # immport bow alg
        # output = bow_alg(data)

    # apply other algs maybe??

    return output


def run_visualizations(data):

    # do viz
    if visualization['WordCloud']:
        # import and apply WC alg
        # immport WC_viz function
        # output = WC_viz(processed_data)

    # apply other visualizations maybe??

    return output





      

    print('Algorithms:')
    for alg in algorithms:
      print('  {}: {}'.format(alg, algorithms[alg]))




if __name__ == '__main__':
    d,p,a,v = read_config_file()
    # do preprocessing
    processed_data = preprocess_data(d,p,a,v)
    algs_done_data = apply_algorithms(processed_data)
    return run_visualizations(algs_done_data)

    # do algs
    # do visualization



















