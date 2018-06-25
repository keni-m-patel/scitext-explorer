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

### CONSTANTS ###
DEBUG = 0 # if true, print debugging statements
DATA_PATH = 'data/'
CONFIG_PATH = 'configuration/'

### IMPORTS ###

from main_logic import read_config_file, preprocess_data, apply_algorithms, run_visualizations

def main():

    # get user selections and path
    user_data_path, selected_prepro, selected_algs, selected_viz = read_config_file()

    # do preprocessing
    processed_data = preprocess_data(user_data_path, selected_prepro)

    # apply algs
    post_algs_data = apply_algorithms(processed_data, selected_algs)

    # run viz
    print(run_visualizations(post_algs_data, selected_viz))

    if DEBUG:
        print('end')



if __name__ == '__main__':
    if DEBUG:
        print('start')
    main()

    




















