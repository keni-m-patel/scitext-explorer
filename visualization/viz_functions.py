from wordcloud import WordCloud
import matplotlib.pyplot as plt

from random import shuffle

# def bow_to_fs(bow_dict):
#     fs = ''
#     for word,freq in bow_dict.items():
#         for i in range(freq):
#             fs = fs + ' ' + word
#     return fs

def bow_to_fs(bow_dict):
    word_list = []
    for word,freq in bow_dict.items():
        for i in range(freq):
            word_list.append(word)
    print('word_list: \n', word_list)

    shuffle(word_list)
    shuffled_word_list = word_list

    fs = ''
    for w in shuffled_word_list:
        fs = fs + ' ' + w
    return fs

def bow_to_wordcloud(bow):
    print('bow:', bow)

    docs = bow_to_fs(bow)
    print('\n fs docs: \n', docs)
    wc = WordCloud().generate(docs)
    plt.imshow(wc, interpolation='bilinear')
    plt.axis('off')
    wc = WordCloud(max_font_size=40).generate(docs)
    return plt.show()


