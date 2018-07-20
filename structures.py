
# MAKE CORPUS NOT A PARENT AND MAKE IT A CONTROLLER CLASS THAT 
# TAKES IN ONE CONFIG FILE AND SPITS OUT AN OBJ BASED ON DOC TYPE
'''
todo:
1) test DOTCSV class
2) make DotXML? do microsoft word stuff
3) HTML parsing 
4) 

'''

import os
import ntpath
import utilities
import logging
import decorators
import json
from PyPDF2 import PdfFileReader as PDFR
import csv
from preprocess import Preprocessor
import glob



logger = logging.getLogger(__name__)

# @decorators.log(logger)
class Corpus(object):

    def __init__(self, config_file, group_by=None):
        self.config = utilities.get_config(config_file) # read the config file and set the log_file name
        self.path = self.config['directory']
        self.files = glob.glob(self.path + '*')

        if group_by:
            self.grouping = group_by
        else:
            self.grouping = self.config['group_by']
        self.filetype = None
        print('\n\n\n\nReading in {} file(s) from {}\n\n'.format(len(self.files), config_file))


    def __call__(self):

        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.files]])
        # print('\n\n\nfile type: \n\n', filetype, '\n\n')
        
        if filetype == {'.txt'}:
            t = DotTXT(self.files, self.grouping)
            return t

        elif filetype == {'.pdf'}:
            p = DotPDF(self.files, self.grouping)
            return p

        elif filetype == {'.csv'}:
            c = DotCSV(self.files, self.grouping)
            return c
        
        elif filetype == {'.json'}:
            j = Tweets(self.files, self.grouping)
            return j

        else:
            print('\n\n ERROR: filetype not set or filetype is not recognized/compatible\n\n')
            print('filetypes found: \n\n', filetype)


    def get_file_names(self):
        return [os.path.splitext(ntpath.basename(f))[0] for f in self.files]

    # def __log(self):
    #     logger.info('Data Map created for: ' + ', '.join(self.config['files']))
    


class DotPDF(object):
    '''
    .PDF object class
    reads in PDFs and can iterate by page or by doc
    in future should be iterable by sentence or maybe paragraph
    '''

    def __init__(self, files, group_by='doc'):
        self.files = files
        self.__read_data(self.files)
        self.grouping = group_by
        self.msg_flag = 1  # flag if preprocessing message should be sent by __iter__, should only do once.


    def __iter__(self):
        # custom iterator function that defines how to iterate over 
        # records according to the configuration specified
        # INTERFACE DEFINITION: this iterator should always yield a string
        if self.msg_flag:
            print('\n\n\n\nRunning the following preprocessing actions:\n\n')
            print(utilities.get_config('./config/preprocessing.yaml'))
            self.msg_flag = 0

        if self.grouping == 'doc':
            for PDFObj in self.data_map:
                pdf_reader = PDFR(PDFObj)
                text_file = ""
                for pg_num in range(pdf_reader.numPages):
                    page_text = pdf_reader.getPage(pg_num).extractText()
                    text_file = text_file + ' ' + page_text
                yield Preprocessor(text_file,'./config/preprocessing.yaml', self.files).run()
            self.__read_data(self.files) # get data    

        elif self.grouping == 'page':
            for PDFObj in self.data_map:
                pdf_reader = PDFR(PDFObj)
                for pg_num in range(pdf_reader.numPages):
                    page_text = pdf_reader.getPage(pg_num).extractText()
                    yield Preprocessor(page_text,'./config/preprocessing.yaml', self.files).run()
            self.__read_data(self.files) # get data    

    
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        if self.grouping == 'doc':
            return len(list(self.files))
        elif self.grouping == 'page':
            total_num_pages = 0
            for PDFObj in self.data_map:
                total_num_pages += PDFR(PDFObj).numPages
            return total_num_pages

    def __read_data(self, files):
        # print('\n\n\n files: ', files)
        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.files]])
        # print('\n\n\nfile type: \n\n', filetype, '\n\n')
        
        if filetype == {'.pdf'}:
            self.data_map = map(lambda x: open(os.path.join('', x),'rb'), self.files)

        else: 
            print('ERROR: NON-PDF PASSED TO PDF CLASS')


class DotTXT(object):
    '''
    .txt object 
    can read in .txt files and iterate by doc. in the future, should also iterate by sentences. 
    '''

    def __init__(self, files, group_by='doc'):
        self.files = files
        self.__read_data(self.files) # get data    
        self.grouping = group_by
        self.msg_flag = 1
        
    def __iter__(self):
        # custom iterator function that defines how to iterate over 
        # records according to the configuration specified
        # INTERFACE DEFINITION: this iterator should always yield a string
        if self.msg_flag:
            print('\n\n\n\nRunning the following preprocessing actions on group of files:\n\n')
            print(utilities.get_config('./config/preprocessing.yaml'))
            self.msg_flag = 0

        for doc in self.data_map:
            yield Preprocessor(doc,'./config/preprocessing.yaml', self.files).run()
        self.__read_data(self.files) # get data    

    
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        return len(list(self.config['files']))
        
    def __read_data(self, files):
        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.files]])
        
        if filetype == {'.txt'}:
            # map to implement "lazy loading"; only read files as we need
            self.data_map = map(lambda x: open(os.path.join('', x)).read(), self.files)        
        else:
            print('ERROR: NON-TXT PASSED TO TXT CLASS')


class DotCSV(DotTXT): 
    '''
    CSV class for corpus of .csv files. 
    can iterate by rows or by columns
    '''

    def __init__(self, files, group_by):
        self.grouping = group_by
        self.files = files
        self.__read_data(self.files)
        self.msg_flag = 1
        # self.__log() # log things
        

    def __iter__(self):
        if self.msg_flag:
            print('\n\n\n\nRunning the following preprocessing actions on group of files:\n\n')
            print(utilities.get_config('./config/preprocessing.yaml'))
            self.msg_flag = 0

        for csv_file in self.data_map:
            reader = csv.reader(csv_file, delimiter=',')
            if self.grouping == "row":
                for row in reader:
                    # print('ROW: \n', row)
                    row_cells = ""
                    for cell in row:
                        # print('cell: \n', cell)
                        row_cells += ' ' + cell + ' '
                    # print('row_cells:\n', row_cells)
                    yield Preprocessor(row_cells,'./config/preprocessing.yaml', self.files).run()

            elif self.grouping == "col":
                columns = zip(*reader)
                col_text = ""
                for column in columns:
                        # print ('COLUMN:\n\n', column )
                        for cell in column:
                            col_text += ' ' + cell + ' '
                        yield Preprocessor(col_text,'./config/preprocessing.yaml', self.files).run()
        self.__read_data(self.files) # get data   

            
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        num_rows = 0
        num_cols = 0    

        if self.grouping == "row":
            for csv_file in self.data_map:
                reader = csv.reader(csv_file, delimiter=',')
                for row in reader:
                    num_rows += 1
            return num_rows

        elif self.grouping == "col":
            for csv_file in self.data_map:
                reader = csv.reader(csv_file, delimiter=',')
                first_row = True
                for row in reader:
                    if not first_row:
                        break
                    num_cols += len(row)
                    first_row = False
            return num_cols


    def __read_data(self, files):
        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.files]])
        
        if filetype == {'.csv'}:
            # map to implement "lazy loading"; only read files as we need
            self.data_map = map(lambda x: open(os.path.join('', x),'rU'), self.files)        
        else:
            print('ERROR: NON-CSV PASSED TO CSV CLASS')



 
class Tweets(object):

    def __init__(self, files, group_by):
        self.files = files
        self.__read_data(self.files)
        self.grouping = group_by
        self.msg_flag = 1
      

    def __iter__(self):  
        if self.msg_flag:
            print('\n\n\n\nRunning the following preprocessing actions on group of files:\n\n')
            print(utilities.get_config('./config/preprocessing.yaml'))
            self.msg_flag = 0
        for doc in self.data_map:
            tweets = json.loads(doc.read(), encoding = "utf-8")
            for tweet in tweets:
                yield Preprocessor(tweet['Text'],'./config/preprocessing.yaml', self.files).run()
        self.__read_data(self.files)

    def __len__(self):
        pass


    def __read_data(self, files):
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.files]])
        if filetype == {'.json'}:
            self.data_map = map(lambda x: open(os.path.join('', x),'rU'), self.files)
        else:
            print("ERROR: NON-JSON PASSED TO TWEET CLASS")


class Merge(object):
 
    # class to merge a list corpus objects into one 
    # to let all docs be iterable as part of  merged corpus

    def __init__(self, corpus_list):
        self.corpus_list = corpus_list

    def __iter__(self):
        for corpus in self.corpus_list:
            for doc in corpus:
                yield doc 






