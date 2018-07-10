
import logging
from structures import Corpus
from algorithms import Algorithm
from visualization import Visualization
from itertools import chain, repeat




logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(name)s %(levelname)s %(message)s',
                    filename='scitext.log',
                    filemode='w')
'''
TODO:
# if select something (ie for PP) that doesn't work for ALG or VIZ, spit out warning
'''


corpus = Corpus('./config/data/text_files.yaml')


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


vis = Visualization( './config/visualization.yaml',alg, doc_names)


vis.run()

