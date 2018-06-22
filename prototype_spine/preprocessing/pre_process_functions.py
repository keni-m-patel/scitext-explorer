
# coding: utf-8

# In[ ]:


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


#Stems tokens
#List of strings
### WORD STEMMING ###
import nltk 
from nltk.stem import PorterStemmer

def stem_tokens(documents):  
    ps = PorterStemmer()
    stem_docs=list()
    for i in documents:
        for item in i:
            ps.stem(item)
            stem_docs.append(ps.stem(item))
    return stem_docs
    
stem_tokens(tokens)

#Lemmatizes tokens
#List of strings


def lemma(documents):
    lem_docs=list()
    wordnet_lemmatizer = WordNetLemmatizer()
    for no_stops in documents:
        for t in no_stops:
            lemmatized = wordnet_lemmatizer.lemmatize(t)
            bow = Counter(lemmatized)
            lem_docs.append(bow)
    return lem_docs

