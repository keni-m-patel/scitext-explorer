
import inspect
import utilities
import matplotlib.pyplot as plt

from sklearn.cluster import KMeans
from sklearn.manifold import TSNE

import pandas as pd

from collections import Counter



class Visualization(object):

    def __init__(self, config_file, config_file_alg, alg):
        #self.corpus = data
        #pass # because the next line doesn't actually work yet, need to build a preprocessing.yaml file
        self.config = utilities.get_config(config_file)
        self.config_alg = utilities.get_config(config_file_alg)
        self.alg_ran=alg.results
        self.doc_names = alg.doc_ids
        
        
    def __iter__(self):
        for item in self.corpus:
            yield item

    def run(self):
        
        print('\n\n\n\nRunning the following visualization:\n\n')
        print(self.config)
        
        self.result_dict = {}
            
        if self.config['kmean_hist'] and self.config_alg['latent_semantic_analysis']:
            k = kmean_hist(self.alg_ran, self.config_alg['kmeans'], self.doc_names)
            k.run()
            self.result_dict['kmean_hist'] = k.output

  
            if self.config['tsne']:
                t = tsne(self.alg_ran, self.doc_names, k.dtm_lsa)
                t.run()
                self.result_dict['tsne'] = t.output
                
                if self.config['export_scatter_plot_excel_data']:
                    sp = File_Export()
                    sp.export_scatter_plot_excel_data(t.output, k.clusters_and_names)
                    
                if self.config['export_bokeh']:
                    b = File_Export()
                    b.export_bokeh( t.output, k.models, t.output, self.doc_names)
                    
    
        if self.config['export_word_cloud_excel_data'] and self.config_alg['word_frequency_table']:
            wc = File_Export() #,self.corpus):                   ###GET THIS TO WORK
            wc.export_word_cloud_excel_data(self.alg_ran)
        
        if self.config['export_bar_graph_excel_data'] and self.config_alg['word_frequency_table']:
            bg = File_Export() #,self.corpus):                   ###GET THIS TO WORK
            bg.export_bar_graph_excel_data(self.alg_ran)
        
        output_text = ""
        for vis,result in self.result_dict.items():
            output_text += "\n\nvisualization: {}\n\nresult:\n\n {}\n\n".format(vis,result)

        #print(output_text)
        return output_text

class VectorSpaceModels(object):
    
    def __init__(self, doc_names): #, corpus):
        #self.corpus = corpus
        self.doc_names = doc_names
        self.dtm = None
        self.vectorizer = None
        self.dist = None
        self.cluster_colors = {0: '#a6cee3', 
                               1: '#1f78b4', 
                               2: '#b2df8a', 
                               3: '#33a02c', 
                               4: '#fb0a99',
                               5: '#e31a1c',
                               6: '#fdbf6f',
                               7: 'yellow',
                               8: '#ff7f00',
                               9: '#cab2d6',
                               10: 'gray'}
       
class kmean_hist(VectorSpaceModels):
    """Plots histogram of clusters"""
    def __init__(self, result_dict, config_alg, doc_names): #,corpus):
        super().__init__(doc_names)      
        
        self.dtm_lsa = result_dict['latent_semantic_analysis']['dtm_lsa']  
        self.max_clusters = config_alg
        
    def run(self):
            km_dict = dict()

            self.models = dict()
            color_dict = dict()
    

            for index in range(2,self.max_clusters + 1):
                km = KMeans(n_clusters = index,  init = 'k-means++', max_iter = 1000, random_state = 1423)
                km.fit(self.dtm_lsa)
                clusters = km.labels_.tolist()

                km_dict[index] = Counter(clusters)
                self.models[index] = {'KMeans Model': km,
                                     'KMeans Centroids': km.cluster_centers_.argsort()[:, ::-1],
                                     'Document-Clustering': Counter(clusters),
                                     'Document Cluster Id': clusters,
                                     'Cluster Colors': [self.cluster_colors[cluster] for cluster in clusters],
                                     'Frame': pd.DataFrame({'Document Name': self.doc_names, 'Cluster': clusters})}

            self.output = self.models
            

            color_dict[index] = [self.cluster_colors[cluster] for cluster in clusters] 
            self.clusters_and_names = self.models[index]['Frame']
            
            background = 'purple'
            accent = 'purple'
            font_size = 10.0
            index = 0
            for key,val in self.models.items():
    
                if index%5 == 0:
                    fig = plt.figure(figsize=(12,2))
    
                ax = fig.add_subplot(151 + index%5)
    
                self.x = [k for k,v in sorted(val['Document-Clustering'].items())]
                self.y = [v for k,v in sorted(val['Document-Clustering'].items())]
    
                plt.bar(self.x,self.y,width = 0.8, color = background)
    
                plt.title(str(key) + ' Document\nClusters', fontweight = 'normal', color = accent)
    
                plt.grid(False)
                ax.tick_params(direction='out', length = 4, width = 1, colors = background,
                               labelsize = font_size, labelcolor = background)
    
                ax.spines['right'].set_visible(False)
                ax.spines['left'].set_visible(False)
                ax.spines['top'].set_visible(False)
                ax.spines['bottom'].set_visible(False)
    
                plt.savefig('Hist_Clusters' + str(index) + '.png', transparent = True, bbox_inches = 'tight', dpi = 600)
    
                index += 1

class tsne(kmean_hist):
    """Initiates tsne for demsionality reduction"""
    def __init__(self, result_dict, doc_names, dtm_lsa):
        #super().__init__(doc_names)      
        
        self.dist = dtm_lsa         

        
    def run(self):
        random_state = 1423
        tsne_matrix = TSNE(n_components=2, perplexity=30.0, early_exaggeration=12.0, learning_rate=200.0, 
                           n_iter=1000, n_iter_without_progress=300, min_grad_norm=1e-07, metric='euclidean', 
                           init='random', verbose=0, random_state = random_state, method='barnes_hut', angle=0.5)

        
        position = tsne_matrix.fit_transform(self.dist)
        
        x, y = position[:, 0], position[:, 1]
        
        self.output = pd.DataFrame(position)
        
          
class File_Export(VectorSpaceModels):

    def __init__(self):
        #super().__init__(doc_names) #corpus)
        self.result_dict = None
    
    def export_word_cloud_excel_data(self, result_dict):
        '''Creates an excel file for a Tableau WordCloud'''
        self.word_frequency = result_dict['word_frequency']
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('word_cloud_data.xlsx', engine='xlsxwriter')
        #bow_max.to_excel(writer, sheet_name='Sheet1')
        self.word_frequency.to_excel(writer)
        # Get the xlsxwriter objects from the dataframe writer object.

        #worksheet = writer.sheets['Sheet1']
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        

        print("word_cloud_data.xlsx can be found in the scitext-explorer file and is ready to be used in Tableau")
        
    def export_bar_graph_excel_data(self, result_dict):
        '''Creates an excel file for a Tableau Bar Graph'''

        
        self.bar_graph = result_dict['word_frequency'][:10]
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('bar_graph_data.xlsx', engine='xlsxwriter')
        #bow_max.to_excel(writer, sheet_name='Sheet1')
        self.bar_graph.to_excel(writer, index = False)
        # Get the xlsxwriter objects from the dataframe writer object.

        #worksheet = writer.sheets['Sheet1']
        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        print("bar_graph_data.xlsx can be found in the scitext-explorer file and is ready to be used in Tableau")
       
    def export_scatter_plot_excel_data(self, x_and_y, clusters_and_names):
        '''Creates an excel file for a Tableau ScatterPlot'''
        self.x_and_y = x_and_y
        self.clusters_and_names = clusters_and_names
        self.clusters_and_names.columns = ['docnames', 'cluster']
        self.x_and_y.columns = ['x','y']
        self.scatter_plot_data = self.clusters_and_names.join(self.x_and_y)
        self.scatter_plot_data = self.scatter_plot_data.set_index('docnames')
        
        # Create a Pandas Excel writer using XlsxWriter as the engine.
        writer = pd.ExcelWriter('scatter_plot_data.xlsx', engine='xlsxwriter')
       
        # Get the xlsxwriter objects from the dataframe writer object.


        # Close the Pandas Excel writer and output the Excel file.
        writer.save()
        print("scatter_plot_data.xlsx can be found in the scitext-explorer file and is ready to be used in Tableau")

    def export_bokeh(self, x_and_y, models, output, doc_names):
        '''Creates an excel file for a Bokeh ScatterPlot'''

        clusters =  models
        base = {'x': output.ix[:,0].tolist(), 
                'y': output.ix[:,1].tolist(),
                'docname': doc_names}
       
        for key,val in sorted(clusters.items()):
             
            base[key] = [pair for pair in zip(val['Document Cluster Id'],val['Cluster Colors'])]
        
        column_order = ['docname','x','y'] + sorted(list(clusters.keys()))
        df = pd.DataFrame(base)[column_order]
        
        df.to_excel('Bokeh_Test.xlsx', index = False)
