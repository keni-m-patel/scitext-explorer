# -*- coding: utf-8 -*-
"""
Created on Fri Jul  6 08:22:02 2018

@author: 597667
"""
import inspect
import utilities
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.cluster import KMeans, MiniBatchKMeans
from algorithms import Algorithm
from sklearn.manifold import mds, TSNE
import pandas as pd



from collections import defaultdict, Counter

from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances

class Visualization(object):

    def __init__(self, config_file, alg, doc_names):
        #self.corpus = data
        #pass # because the next line doesn't actually work yet, need to build a preprocessing.yaml file
        self.config = utilities.get_config(config_file)
        self.alg=alg
        self.doc_names = doc_names
        print('\n\n\n\nRunning the following visualization:\n\n')
        print(self.config)
        
    def __iter__(self):
        for item in self.corpus:
            yield item

    def run(self):
        result_dict = {}
        
        if 'kmean_hist' in self.config:
            k = kmean_hist(self.alg.run(), self.doc_names)
            k.run()
            #result_dict['kmean_hist'] = k.output
            
            if self.config['tsne']:
                t = tsne(self.alg.run(), self.doc_names, k.dtm_lsa)
                t.run()
                result_dict['tsne'] = t.output
                
                if 'export_scatter_plot' in self.config:
                    sp = File_Export()
                    sp.export_scatter_plot(t.output, k.clusters_and_names)
                    
    
        if 'export_word_cloud' in self.config:
            wc = File_Export() #,self.corpus):                   ###GET THIS TO WORK
            wc.export_word_cloud(self.alg.run())
        
        
        output_text = ""
        for vis,result in result_dict.items():
            output_text += "\n\nvisualization: {}\n\nresult:\n\n {}\n\n".format(alg,result)

        print(output_text)
        return output_text

class VectorSpaceModels(object):
    
    def __init__(self, doc_names): #, corpus):
        #self.corpus = corpus
        self.doc_names = doc_names
        self.dtm = None
        self.vectorizer = None
        self.dist = None
        

class kmean_hist(VectorSpaceModels):
    def __init__(self, result_dict, doc_names): #,corpus):
        super().__init__(doc_names)      
        
        self.dtm_lsa = result_dict['latent_semantic_analysis']['dtm_lsa']  
        
    def run(self):
            km_dict = dict()
            max_clusters = 2
    
            for index in range(2,max_clusters + 1):
                km = KMeans(n_clusters = index,  init = 'k-means++', max_iter = 1000, random_state = 1423)
                km.fit(self.dtm_lsa)
                clusters = km.labels_.tolist()
                km_dict[index] = Counter(clusters)
                
                
            models = dict()
            models[index] = {'KMeans Model': km,
                                 'KMeans Centroids': km.cluster_centers_.argsort()[:, ::-1],
                                 'Document-Clustering': Counter(clusters),
                                 'Frame': pd.DataFrame({'Document Name': self.doc_names, 'Cluster': clusters})}
            
            
            self.clusters_and_names = models[index]['Frame']
            
            #self.clusters_and_names.columns['docnames','labels']
            #self.clusters_and_names['title'] = self.clusters_and_names['labels']
           
            
            
            background = 'gray'
            higlight = '#2171b5'
            accent = 'dimgray'
            font_size = 10.0
            index = 0
            for key,val in models.items():
    
                if index%5 == 0:
                    fig = plt.figure(figsize=(12,2))
    
                ax = fig.add_subplot(151 + index%5)
    
                x = [k for k,v in sorted(val['Document-Clustering'].items())]
                y = [v for k,v in sorted(val['Document-Clustering'].items())]
    
                plt.bar(x,y,width = 0.8, color = background)
    
                plt.title(str(key) + ' Document\nClusters', fontweight = 'normal', color = accent)
    
                plt.grid(False)
                ax.tick_params(direction='out', length = 4, width = 1, colors = background,
                               labelsize = font_size, labelcolor = background)
    
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
    
                plt.savefig('Corpus2 Clusters ' + str(index) + '.png', transparent = True, bbox_inches = 'tight', dpi = 600)
    
                index += 1
                

class tsne(kmean_hist):
    def __init__(self, result_dict, doc_names, dtm_lsa):
        #super().__init__(doc_names)      
        
        self.dist = dtm_lsa         

        
    def run(self):
        random_state = 1423
        tsne_matrix = TSNE(n_components=2, perplexity=30.0, early_exaggeration=12.0, learning_rate=200.0, 
                           n_iter=1000, n_iter_without_progress=300, min_grad_norm=1e-07, metric='euclidean', 
                           init='random', verbose=0, random_state = random_state, method='barnes_hut', angle=0.5)

        
        position = tsne_matrix.fit_transform(self.dist)
        
        
        x, y = position[ 0, : ], position[1, : ]
        print(x,y)
        self.output = pd.DataFrame({'x' : x, 'y' : y})
        
          
class File_Export(VectorSpaceModels):
    
    def __init__(self): #,corpus):
        #super().__init__(doc_names) #corpus)
        
        results_dict = None
        

    def export_word_cloud(self, result_dict): #, alg.wordfreq):
        
        self.word_frequency = result_dict['word_frequency']
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('word_cloud_form.xlsx', engine='xlsxwriter')
        #bow_max.to_excel(writer, sheet_name='Sheet1')
        self.word_frequency.to_excel(writer, sheet_name='Sheet1')
        # Get the xlsxwriter objects from the dataframe writer object.

        #worksheet = writer.sheets['Sheet1']
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        
    
        
    def export_scatter_plot(self, x_and_y, clusters_and_names):
        
        self.x_and_y = x_and_y
        self.clusters_and_names = clusters_and_names
        self.clusters_and_names.columns = ['docnames', 'label']
        self.clusters_and_names['title'] = self.clusters_and_names['label']
        scatter_plot_data = self.clusters_and_names.join(self.x_and_y)
        scatter_plot_data = scatter_plot_data.set_index('docnames')
        
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('scatter_plot_form.xlsx', engine='xlsxwriter')
        #bow_max.to_excel(writer, sheet_name='Sheet1')
        scatter_plot_data.to_excel(writer, sheet_name='Sheet1')
        # Get the xlsxwriter objects from the dataframe writer object.

        #worksheet = writer.sheets['Sheet1']
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()