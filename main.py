
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
# if select something (ie for PP) that doesn't work for ALG or VIZ, spit out warning
'''


corpus = Corpus('./config/data/pdf_files.yaml')


tokens = corpus()


tokenized_docs = []


for doc in tokens:
    tokenized_docs.append(doc)
    

doc_names = corpus.get_file_names()



<<<<<<< HEAD
token_dict = dict(zip(doc_names, chain(tokenized_docs, repeat(None))))
=======
#token_dict = dict(zip(doc_names, chain(tokenized_docs, repeat(None))))


#print(file_object)
#print(file_object.grouping)
#print(file_object.config)
>>>>>>> 2cbfa9d9f2f72b4ad2c89555968bec3affe43fdf


alg = Algorithm(tokens, './config/algorithms.yaml')


vis = Visualization( './config/visualization.yaml',alg, doc_names)


vis.run()

