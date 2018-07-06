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

class Visualization(object):

    def __init__(self, data, config_file):
        self.corpus = data
        pass # because the next line doesn't actually work yet, need to build a preprocessing.yaml file
        self.config = utilities.get_config(config_file)
        print('\n\n\n\nRunning the following visualization:\n\n')
        print(self.config)
        
    def __iter__(self):
        for item in self.corpus:
            yield item

    def run(self):
        result_dict = {}
        
        if 'kmean_hist' in self.config:
            k = kmean_hist(self.corpus)
            k.run()
            result_dict['kmean_hist'] = k.output
        
        output_text = ""
        for vis,result in result_dict.items():
            output_text += "\n\nvisualization: {}\n\nresult:\n\n {}\n\n".format(alg,result)

        print(output_text)
        return output_text

class VectorSpaceModels(object):
    
    def __init__(self, corpus):
        self.corpus = corpus
        self.dtm = None
        self.vectorizer = None
        self.dist = None

class kmean_hist(VectorSpaceModels):
    def __init__(self, corpus, dist):
        super().__init__(corpus)      
        
        self.dist = dist   
        models = dict()
        models[index] = {'KMeans Model': km,
                             'KMeans Centroids': km.cluster_centers_.argsort()[:, ::-1],
                             'Document-Clustering': Counter(clusters),
                             'Frame': pd.DataFrame({'Cluster': clusters})}
                                                    #'Document Name': docnames})}
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