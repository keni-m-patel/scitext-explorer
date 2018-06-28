DEBUG = 0

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import interactive
from random import shuffle
import glob


def bow_to_fs(bow_dict):
    word_list = []
    for word,freq in bow_dict.items():
        for i in range(freq):
            word_list.append(word)

    if DEBUG:
        print('\n\n\nword_list: \n', word_list)

    shuffle(word_list)
    shuffled_word_list = word_list

    fs = ''
    for w in shuffled_word_list:
        fs = fs + ' ' + w
    return fs


def multiple_bow_to_wordcloud(list_of_bow):
    for i in range(len(list_of_bow)): 
        bow = list_of_bow[i]
        docs = bow_to_fs(bow)

        if DEBUG:
            print('\n\n\n bow: \n', bow)
            print('\n\n\n fs docs: \n', docs)
        plt.figure(i)
        wc = WordCloud().generate(docs)
        plt.imshow(wc, interpolation='bilinear')
        plt.axis('off')
        wc = WordCloud(max_font_size=40).generate(docs)
    return plt.show()



import pandas as pd


def document_names(path):
    files = glob.glob(path + '*')
    document_names=list()
    for textfile in files[:]:
        if '.txt' in textfile:
            ext = ".txt"
            fileNameOnly = textfile[len(path):textfile.find(ext) + len(ext)]
            document_names.append(fileNameOnly)
        elif '.pdf' in textfile:
            ext = ".pdf"
            fileNameOnly = textfile[len(path):textfile.find(ext) + len(ext)]
            document_names.append(fileNameOnly)
        else:
            print(" ")
    return document_names


def bow_to_dataframe(bow, path):
    bow_df = pd.DataFrame.from_records(bow)
    bow_df = bow_df.T
    bow_df.columns = document_names(path)
    bow_df = bow_df.fillna(0)
    pd.options.display.float_format = '{:,.0f}'.format
    return bow_df




