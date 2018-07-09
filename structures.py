
# MAKE CORPUS NOT A PARENT AND MAKE IT A CONTROLLER CLASS THAT 
# TAKES IN ONE CONFIG FILE AND SPITS OUT AN OBJ BASED ON DOC TYPE
'''
todo:
1) test DOTCSV class
2) make DotXML? do microsoft word stuff
3) HTML parsing 
4) 

'''
#JUST PUT PREPROCESSOR IN HERE
import os
import utilities
import logging
import decorators
from PyPDF2 import PdfFileReader as PDFR
import csv
from os import listdir
from os.path import isfile, join
from preprocess import Preprocessor


logger = logging.getLogger(__name__)

# @decorators.log(logger)
class Corpus(object):

    def __init__(self, config_file, group_by='doc'):
        self.config = utilities.get_config(config_file) # read the config file and set the log_file name
        self.grouping = group_by
        self.filetype = None
        print('\n\n\n\nReading in the following files:\n\n')
        print(self.config)



    def __call__(self):

        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.config['files']]])
        
        if filetype == {'.txt'}:

            t = DotTXT(self.config, self.grouping)
            return t

        elif filetype == {'.pdf'}:
            p = DotPDF(self.config, self.grouping)
            return p

        elif filetype == {'.csv'}:
            c = DotCSV(self.config, self.grouping)
            return c

        else:
            print('filetype not set or filetype is not recognized/compatible')

    def get_file_names(self):
        onlyfiles = [f for f in self.config['files']] 
        return onlyfiles
        

    # def __log(self):
    #     logger.info('Data Map created for: ' + ', '.join(self.config['files']))
    
   


class DotPDF(object):
    def __init__(self, config, group_by='doc'):
        self.config = config
        self.__read_data(self.config)
        self.grouping = group_by


    def __iter__(self):
        # custom iterator function that defines how to iterate over 
        # records according to the configuration specified
        # INTERFACE DEFINITION: this iterator should always yield a string
        if self.grouping == 'doc':
            for PDFObj in self.data_map:
                pdf_reader = PDFR(PDFObj)
                text_file = ""
                for pg_num in range(pdf_reader.numPages):
                    page_text = pdf_reader.getPage(pg_num).extractText()
                    text_file = text_file + ' ' + page_text
                yield Preprocessor(text_file,'./config/preprocessing.yaml').run()
            self.__read_data(self.config) # get data    

        elif self.grouping == 'page':
            for PDFObj in self.data_map:
                pdf_reader = PDFR(PDFObj)
                for pg_num in range(pdf_reader.numPages):
                    page_text = pdf_reader.getPage(pg_num).extractText()
                    yield Preprocessor(page_text,'./config/preprocessing.yaml').run()
            self.__read_data(self.config) # get data    

    
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        if self.grouping == 'doc':
            return len(list(self.config['files']))
        elif self.grouping == 'page':
            total_num_pages = 0
            for PDFObj in self.data_map:
                total_num_pages += PDFR(PDFObj).numPages
            return total_num_pages

    def __read_data(self, config):
        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.config['files']]])
        
        if filetype == {'.pdf'}:
            # map to implement "lazy loading"; only read files as we need
            self.data_map =map(lambda x: open(os.path.join(self.config['directory'], x),'rb'), self.config['files'])
        else: 
            print('ERROR: NON-PDF PASSED TO PDF CLASS')


class DotTXT(object):

    def __init__(self, config, group_by='doc'):
        self.config = config
        self.__read_data(self.config) # get data    
        self.grouping = group_by
        
    def __iter__(self):
        # custom iterator function that defines how to iterate over 
        # records according to the configuration specified
        # INTERFACE DEFINITION: this iterator should always yield a string
        for doc in self.data_map:
            yield Preprocessor(doc,'./config/preprocessing.yaml').run()
            self.__read_data(self.config) # get data    

    
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        return len(list(self.config['files']))
        
    def __read_data(self, config):
        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.config['files']]])
        
        if filetype == {'.txt'}:
            # map to implement "lazy loading"; only read files as we need
            #self.data_map = map(lambda x: open(os.path.join(self.config['directory'], x)).read(), self.config['files'])
            self.data_map = map(lambda x: open(os.path.join(self.config['directory'], x)).read(), self.config['files'])
        else:
            print('ERROR: NON-TXT PASSED TO TXT CLASS')



#################################################
##    non-functional, start for DotCSV class  ###
#################################################
'''
class DotCSV(DotTXT): 
    def __init__(self, config_file, group_by=None):
        self.config = config_file
        self.__read_data(self.config)
        self.__log() # log things
        self.grouping = group_by

    def __iter__(self):
        # custom iterator function that defines how to iterate over 
        # records according to the configuration specified
        # INTERFACE DEFINITION: this iterator should always yield a string

        # csv_dict_reader, but it does stuff on the whole file, not one thing at a time
        reader = csv.DictReader(file_obj, delimiter=',')
        field_names = csv.fieldnames()  # list of strings

        if self.grouping == "row":
            for row in reader:
                yield row
        elif self.grouping == "col":
            for field_name in field_names:
                column = []
                for row in reader:
                    column.append(row[field_name])
                yield column
            
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        reader = csv.DictReader(file_obj, delimiter=',')
        field_names = csv.fieldnames()  # list of strings

        if self.grouping == "row":
            return size(reader)
        elif self.grouping == "col":
            return len(reader.next())

    def __read_data(self, config):
        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.config['files']]])
        
        if filetype == {'.csv'}:
            # map to implement "lazy loading"; only read files as we need
            self.data_map = map(lambda x: open(os.path.join(self.config['directory'], x)).read('rb'), self.config['files'])
        else:
            print('ERROR: NON-CSV PASSED TO CSV CLASS')

'''

        