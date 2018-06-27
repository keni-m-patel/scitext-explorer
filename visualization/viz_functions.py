DEBUG = 0

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from matplotlib import interactive
from random import shuffle


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




