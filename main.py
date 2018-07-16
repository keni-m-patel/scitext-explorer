
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
# ADD MERGE class and functionality with master config and then allow link to all config classes

'''
print('\n\nreading from the following configuration files: \n\n ', utilities.get_config('./config/data/master.yaml')['config_files'])
corpus_list = [Corpus(config_file) for config_file in utilities.get_config('./config/data/master.yaml')['config_files']]
corpi = Merge([corpus() for corpus in corpus_list])
#run stuff


#print('corpi', corpi)
#for c in corpi:
   # print(c)


tokens = corpi  # corpus()


tokenized_docs = []


for doc in tokens:
    tokenized_docs.append(doc)
    

corpus_doc_name_lists = [corpus.get_file_names() for corpus in corpus_list]  # corpus.get_file_names()
doc_names = []
for c_list in corpus_doc_name_lists:
    doc_names += c_list

print('doc_names\n\n', doc_names)


# token_dict = dict(zip(doc_names, chain(tokenized_docs, repeat(None))))


# print(file_object)
# print(file_object.grouping)
# print(file_object.config)



alg = Algorithm(tokens, './config/algorithms.yaml')

alg_ran = alg.run()

vis = Visualization( './config/visualization.yaml', './config/algorithms.yaml', alg_ran, doc_names)


vis.run()

