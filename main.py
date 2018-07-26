

import logging
from structures import Corpus, Merge
from algorithms import Algorithm
from visualization import Visualization
import utilities




logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename='scitext.log',
                    filemode='w')
'''
TODO:
# ADD MERGE class and functionality with master config and then allow linek to all config classes

'''
print('\n\nreading from the following configuration files: \n\n ', utilities.get_config('./config/data/master.yaml')['config_files'])

corpus_list = [Corpus(config_file) for config_file in utilities.get_config('./config/data/master.yaml')['config_files']]
corpi = Merge([corpus() for corpus in corpus_list])


alg = Algorithm(corpi, './config/algorithms.yaml')


alg_ran = alg.run()

vis = Visualization( './config/visualization.yaml', './config/algorithms.yaml', alg_ran)


vis.run()
