
# coding: utf-8

# In[21]:





# In[81]:


import pandas as pd
import numpy as np

# Import packages. Don't worry aobut these too much right now.
import nltk

# TO DO: Import sent_tokenize from nltk.tokenize and then import word_tokenize from nltk.tokenize
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize

from nltk.corpus import stopwords

import glob
import PyPDF2


# In[82]:


def text_import(path):
    files = glob.glob(path + '*')
    documents=list()
    for textfile in files[:]:
        if '.txt' in textfile:
            textfile_open = open(textfile,'r')
            textfileReader = textfile_open.read()
            textfile_1 = ''
            textfile_1 = textfileReader
            documents.append(textfile_1)
        elif '.pdf' in textfile:
            pdfFileObj = open(textfile, 'rb')
            pdfReader = PyPDF2.PdfFileReader(pdfFileObj)
            textfile_1 = ''
            for page in range(0,pdfReader.numPages):
                textfile_1 += pdfReader.getPage(page).extractText()
            documents.append(textfile_1)
        else:
            print('File Error: Cannot read file type for ' + textfile + '\n')
    
    return documents


# In[83]:


path='/Users/Brendan Gochett/Project/'
documents=text_import(path)
print(documents)                


# In[84]:


def complete_tokenize(documents):
    tokenized_documents=list()
    for text in documents:
    
        # TO DO: word_tokenize chapter_one
        tokens = word_tokenize(text)
    
        # Convert the tokens into lowercase
        lower_tokens = [t.lower() for t in tokens]

        # Retain alphabetic words: alpha_only
        alpha_only = [t for t in lower_tokens if t.isalpha()]

        ## Retrieve list of NLTK Stopwords for English
        stop = set(stopwords.words('english'))

        # Remove all stop words: no_stops
        no_stops = [w for w in alpha_only if w not in stop]
        
        tokenized_documents.append(no_stops)

    return tokenized_documents


# In[118]:


tokens=complete_tokenize(documents)

print(tokens)


# In[142]:


from collections import Counter

# Create a Counter with the lowercase tokens
def bow(documents):
    new_docs=list()
    for i in range(len(documents)-1):
        for t in documents:
            bow_simple = Counter(t)
            new_docs.append(bow_simple)
    return new_docs
bow(tokens)


# In[120]:


import nltk 
from nltk.stem import PorterStemmer
from nltk.tokenize import sent_tokenize, word_tokenize


def stem_tokens(documents):  
    ps = PorterStemmer()
    stem_docs=list()
    for i in documents:
        for item in i:
            ps.stem(item)
            stem_docs.append(ps.stem(item))
    return stem_docs
    
stem_tokens(tokens)


# In[140]:


import re
import nltk
from nltk.tokenize import sent_tokenize
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from collections import Counter




from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

def lemma(documents):
    lem_docs=list()
    wordnet_lemmatizer = WordNetLemmatizer()
    for no_stops in documents:
        for t in no_stops:
            lemmatized = wordnet_lemmatizer.lemmatize(t)
            bow = Counter(lemmatized)
            lem_docs.append(bow)

    return lem_docs

lemma(tokens)


# In[137]:


print(lemma(tokens))


# In[141]:


pwd

