# -*- coding: utf-8 -*-
"""
Created on Mon Jun 25 12:47:46 2018

@author: 597543
"""
from pandas import DataFrame

def document_names(path):
    files = glob.glob(path + '*')
    document_names=list()
    for textfile in files[:]:
        if '.txt' in textfile:
            ext = ".txt"
            fileNameOnly = textfile[len(path):textfile.find(ext) + len(ext)]
            document_names.append(fileNameOnly)
        elif '.pdf' in textfile:
            ext = ".pdf"
            fileNameOnly = textfile[len(path):textfile.find(ext) + len(ext)]
            document_names.append(fileNameOnly)
        else:
            print(" ")
    return document_names


def bow_to_dataframe(bow,path):
    bow_df = DataFrame.from_records(bow)
    bow_df = bow_df.T
    bow_df.columns = document_names(path)
    bow_df = bow_df.fillna(0)
    pd.options.display.float_format = '{:,.0f}'.format
    return bow_df