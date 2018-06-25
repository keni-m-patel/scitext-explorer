
# coding: utf-8

# In[8]:


#Import different documents from a file
#Must give path
#Works for text files and PDFs
#Turns files into a list of strings

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

def complete_tokenize(documents):
    tokenized_documents=list()
    print("Adding and Removing Stopwords from NLTK Set of English Stopwords")
    stop = set(stopwords.words('english'))
    add_stop = 'add'
    remove_stop = 'remove'
    add_remove_stop = int(input('To LOOK at Set of Stopwords Enter 1. To ADD Stopwords Enter 2. To REMOVE Stopwords Enter 3. To CONVERT to Original Stopwords Enter 4. Otherwise Enter 5: '))
    while add_remove_stop != 5:
        if add_remove_stop == 1:
            print(stop)
        elif add_remove_stop == 2:
            while add_stop != str(1):
                add_stop = input('Enter a stopword to add. When you are no longer want to add more stop words, enter 1. \n')
                stop.add(add_stop)
                if add_stop != str(1):
                    print('Stopword has been added')
        elif add_remove_stop == 3:
            while remove_stop != str(1):
                remove_stop = input('Enter a stopword to remove. When you are no longer want to remove more stop words, enter 1. \n')
                stop.remove(remove_stop)
                if remove_stop != str(1):
                    print('Stopword has been added')
        elif add_remove_stop == 4:
            stop = set(stopwords.words('english'))
        else:
            print("Error: that input was incorrect")
        add_remove_stop = int(input('To LOOK at Set of Stopwords Enter 1. To ADD Stopwords Enter 2. To REMOVE Stopwords Enter 3. To CONVERT to Original Stopwords Enter 4. Otherwise Enter 5: '))

       
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

def stem_tokens(documents):  
    ps = PorterStemmer()
    stem_words=list()
    stem_docs=list()
    for tokens in documents:
        for item in tokens:
            stem_words.append(ps.stem(item))
        stem_docs.append(stem_words)
        stem_words = list()
    return stem_docs


#Lemmatizes tokens
#List of strings

def lemma(documents):
    lem_words=list()
    lem_docs=list()
    wordnet_lemmatizer = WordNetLemmatizer()
    for no_stops in documents:
        for t in no_stops:
            lemmatized = wordnet_lemmatizer.lemmatize(t)
            lem_words.append(lemmatized)
        lem_docs.append(lem_words)
        lem_words = list()
    return lem_docs
