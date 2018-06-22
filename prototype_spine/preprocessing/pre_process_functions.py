
# coding: utf-8

# In[8]:


#Import different documents from a file
#Must give path
#Works for text files and PDFs
#Turns files into a list of strings
### IMPORTS ###  (just copy paste any new imports you need as lines of code)
import yaml
from preprocessing import text_import as timp, complete_tokenize as ctkn
from algorithms import BOW

### IMPORTING ###

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


#Removes stop words and punctuation and makes letter lowercase
#Then does tokenization
#Keeps form of list of strings, but breaks it into words
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

def complete_tokenize(documents):
    tokenized_documents=list()
    stop = set(stopwords.words('english'))
    Add_Stop = int(input('To Add a Stop Word Enter 1. Press 2 if not. '))
    while Add_Stop == 1:
        look_at_stop = int(input("Press 1 to look at set of stop words. Press 2 if not. "))
        if look_at_stop == 1:
            print(stop)
        stop_word_added = input('Enter a stop word to add: ')
        if stop_word_added not in stop:
            stop.add(stop_word_added)
        else:
            print("That word is alredy in the set of stop words!")
        Add_Stop = int(input('To Add Another Stop Word Enter 1. Press 2 if not. '))
    Remove_Stop = int(input('To Remove a Stop Word Enter 1. Press 2 if not. '))
    while Remove_Stop == 1:
        look_at_stop_1 = int(input("Press 1 to look at set of stop words. Press 2 if not."))
        if look_at_stop_1 == 1:
            print(stop)
        stop_word_removed = input('Enter a stop word to remove: ')
        if stop_word_removed in stop:
            stop.remove(stop_word_removed)
        else:
            print("That word is not in the set of stop words!")
        Remove_Stop = int(input('To Remove Another Stop Word Enter 1. Press 2 if not. '))
    for text in documents:   
        # TO DO: word_tokenize chapter_one
        tokens = word_tokenize(text)   
        # Convert the tokens into lowercase
        lower_tokens = [t.lower() for t in tokens]
        # Retain alphabetic words: alpha_only
        alpha_only = [t for t in lower_tokens if t.isalpha()]
        ## Retrieve list of NLTK Stopwords for English
    
        # Remove all stop words: no_stops
        no_stops = [w for w in alpha_only if w not in stop]       
        tokenized_documents.append(no_stops)
    return tokenized_documents


#Stems tokens
#List of strings

### WORD STEMMING ###
import nltk 
from nltk.stem import PorterStemmer


def stem_tokens(documents):  
    ps = PorterStemmer()
    stem_words=list()
    stem_docs=list()
    for tokens in documents:
        for item in tokens:
            stem_words.append(ps.stem(item))
    return stem_docs


#Lemmatizes tokens
#List of strings


def lemma(documents):
    lem_docs=list()
    wordnet_lemmatizer = WordNetLemmatizer()
    for no_stops in documents:
        for t in no_stops:
            lemmatized = wordnet_lemmatizer.lemmatize(t)
            lem_docs.append(lemmatized)
    return lem_docs

