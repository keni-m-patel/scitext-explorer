
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
import utilities
import logging
import decorators
from PyPDF2 import PdfFileReader as PDFR
import csv

from nltk import sent_tokenize, word_tokenize, pos_tag



logger = logging.getLogger(__name__)

# @decorators.log(logger)
class Corpus(object):

    def __init__(self, config_file, group_by=None):
        self.config = utilities.get_config(config_file) # read the config file and set the log_file name
        if group_by:
            self.grouping = group_by
        else:
            self.grouping = self.config['group_by']
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
                yield text_file
            self.__read_data(self.config) # get data    

        elif self.grouping == 'page':
            for PDFObj in self.data_map:
                pdf_reader = PDFR(PDFObj)
                for pg_num in range(pdf_reader.numPages):
                    page_text = pdf_reader.getPage(pg_num).extractText()
                    yield page_text
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
            self.data_map = map(lambda x: open(os.path.join(self.config['directory'], x),'rb'), self.config['files'])
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
            yield doc
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
            self.data_map = map(lambda x: open(os.path.join(self.config['directory'], x)).read(), self.config['files'])
        else:
            print('ERROR: NON-TXT PASSED TO TXT CLASS')



#################################################
##    non-functional, start for DotCSV class  ###
#################################################

# TRY PANDAS pd.readcsv()
class DotCSV(DotTXT): 

    def __init__(self, config_file, group_by):
        self.grouping = group_by
        self.config = config_file
        self.__read_data(self.config)
        # self.__log() # log things
        

    def __iter__(self):
        
        for csv_file in self.data_map:
            reader = csv.reader(csv_file, delimiter=',')
            if self.grouping == "row":
                for row in reader:
                    # print('ROW: \n', row)
                    row_cells = ""
                    for cell in row:
                        # print('cell: \n', cell)
                        row_cells += ' ' + cell + ' '
                    yield row_cells

            elif self.grouping == "col":
                columns = zip(*reader)
                col_text = ""
                for column in columns:
                        # print ('COLUMN:\n\n', column )
                        for cell in column:
                            col_text += ' ' + cell + ' '
                        yield col_text

        self.__read_data(self.config) # get data    
            
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

    def __read_data(self, config):
        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.config['files']]])
        
        if filetype == {'.csv'}:
            # map to implement "lazy loading"; only read files as we need
            self.data_map = map(lambda x: open(os.path.join(self.config['directory'], x),'rU'), self.config['files'])
        else:
            print('ERROR: NON-CSV PASSED TO CSV CLASS')
        