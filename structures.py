#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 20:53:26 2018

@author: patelkm
"""
# MAKE CORPU NOT A PARENT AND MAKE IT A CONTROLLER CLAS THAT 
# TAKES IN ONE CONFIG FILE AND SPITS OUT AN OBJ BASED ON DOC TYPE
'''
todo:
1) test DOTPDF class
2) test DOTTXT class
3) emancipate DOT* from Corpus, make Corpus a controller class instead
4) add TFIDF instead of CountVectorizer to algs for LSA ::::: done

'''

import os
import utilities
import logging
import decorators
from PyPDF2 import PdfFileReader as PDFR
import csv


logger = logging.getLogger(__name__)

# @decorators.log(logger)
class Corpus(object):

    def __init__(self, config_file, group_by='doc'):
        self.config = utilities.get_config(config_file) # read the config file and set the log_file name
        self.__read_data(self.config) # get data    
        self.__log() # log things
        self.grouping = group_by
        
    def __iter__(self):
        # custom iterator function that defines how to iterate over 
        # records according to the configuration specified
        # INTERFACE DEFINITION: this iterator should always yield a string
        for doc in self.data_map:
            yield doc
    
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

    def __log(self):
        logger.info('Data Map created for: ' + ', '.join(self.config['files']))




class DotPDF(object):
    def __init__(self, config_file, group_by='doc'):
        self.config = config_file
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

        elif self.grouping == 'page':
            for PDFObj in self.data_map:
                pdf_reader = PDFR(PDFObj)
                for pg_num in range(pdf_reader.numPages):
                    page_text = pdf_reader.getPage(pg_num).extractText()
                    yield page_text

    
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        if group_by == 'doc':
            return len(list(self.config['files']))
        elif group_by == 'page':
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
            pass # LOG A WARNING that there shouldn't be non-PDF files 


class DotTXT(object):
    def __init__(self, config_file, group_by='doc'):
        self.config = config_file
        self.__read_data(self.config)
        self.__log() # log things
        self.grouping = group_by

    def __iter__(self):
        # custom iterator function that defines how to iterate over 
        # records according to the configuration specified
        # INTERFACE DEFINITION: this iterator should always yield a string
        for doc in self.data_map:
            yield doc
    
    def __len__(self):
        # we may want to do some introspection of our data objects; how many records
        # are in this data source? HINT: it depends on how we split it into records
        return len(list(self.config['files']))

    def __read_data(self, config):
        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.config['files']]])
        
        if filetype == {'.pdf'}:
            # map to implement "lazy loading"; only read files as we need
            self.data_map = map(lambda x: open(os.path.join(self.config['directory'], x)).read(), self.config['files'])


#################################################
##  this may not be functional, is untested   ###
#################################################

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

        # csv_dict_reader, but it does stuff on the whole file, not ne thing at a time
        reader = csv.DictReader(file_obj, delimiter=',')
        field_names = csv.fieldnames()  # list of strings

        if grouping == "row":
            for row in reader:
                yield row
        elif grouping == "col":
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

        if grouping == "row":
            return size(reader)
        elif grouping == "col":
            return len(reader.next())

    def __read_data(self, config):
        # let's determine the file types we're dealing with
        filetype = set([ext for filename,ext in [os.path.splitext(file) for file in self.config['files']]])
        
        if filetype == {'.pdf'}:
            # map to implement "lazy loading"; only read files as we need
            self.data_map = map(lambda x: open(os.path.join(self.config['directory'], x)).read('rb'), self.config['files'])

        