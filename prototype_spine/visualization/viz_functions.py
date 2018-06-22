from wordcloud import WordCloud
import matplotlib.pyplot as plt

def bow_to_fs(bow_dict):
    fs = ''
    for word,freq in bow_dict.items():
        for i in range(freq):
            fs = fs + word + ' '
    return fs

def bow_to_wordcloud(bow):
    print('bow:', bow)

    docs = bow_to_fs(bow)
    print('docs:', docs)
    wc = WordCloud().generate(docs)
    plt.imshow(wc, interpolation ='bilinear')
    plt.axis('off')
    wc = WordCloud(max_font_size=40).generate(docs)
    return plt.show()


