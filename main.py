
import logging
from structures import Corpus
from algorithms import Algorithm
from visualization import Visualization




logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename='scitext.log',
                    filemode='w')
'''
TODO:
# ADD MERGE class and functionality with master config and then allow link to all config classes
'''
'''
corpus_list = [Corpus(config_file) for config_file in utilities.get_config('./config/master.yaml')]
corpus_list = [corpus() for corpus in corpus_list]
corpi = Merge(corpus_list)
# run stuff
'''

corpus = Corpus('./config/data/pdf_files.yaml')


tokens = corpus()


tokenized_docs = []


for doc in tokens:
    tokenized_docs.append(doc)
    

doc_names = corpus.get_file_names()



#token_dict = dict(zip(doc_names, chain(tokenized_docs, repeat(None))))


#print(file_object)
#print(file_object.grouping)
#print(file_object.config)


alg = Algorithm(tokens, './config/algorithms.yaml')

alg_ran = alg.run()

vis = Visualization( './config/visualization.yaml', './config/algorithms.yaml', alg_ran, doc_names)


vis.run()

