#!/usr/bin/python3
# -*- coding: utf-8 -*-
# config.py     written by Duncan Murray 28/7/2014

import os

fldrs = {}
logs = {}
params = {}

# path for personal data location  (TODO - you need to modify this line below!)
fldrs['localPath'] = 'T:\\user\\AIKIF\\' 
fldrs['log_folder'] = 'T:\\user\\AIKIF\\log' 
fldrs['pers_data'] = 'T:\\user\\AIKIF\\pers_data' 
fldrs['pers_credentials'] = 'T:\\user\\AIKIF\\pers_data\\credentials' 

# FOR DEVELOPMENT
#core_folder = 'T:\\user\\dev\\src\\python\\AIKIF' # <-- wtf!!
core_folder = os.path.abspath(os.path.dirname(os.path.abspath(__file__)) + os.sep + ".." ) 
fldrs['root_path'] = core_folder
fldrs['public_data_path'] = core_folder + os.sep + 'data'
fldrs['program_path'] = os.path.abspath(core_folder + os.sep + 'aikif') 

# user defined parameters 
params['AIKIF_version'] = '0.0.9'
params['AIKIF_deploy'] = 'DEV'


# names of logfiles for AIKIF
logs['logFileProcess'] = fldrs['localPath'] + 'log' + os.sep + 'process.log'
logs['logFileSource'] = fldrs['localPath'] + 'log' + os.sep + 'source.log'
logs['logFileCommand'] = fldrs['localPath'] + 'log' + os.sep + 'command.log'
logs['logFileResult'] = fldrs['localPath'] + 'log' + os.sep + 'result.log'

# index files
#                         fldrs['public_data_path'] + os.sep  + 'index' + os.sep + 'ndxWordsToFilesLecture.txt',
#                         fldrs['localPath'] + 'diary' + os.sep + 'filelister2014.csv',

params['index_files'] = [fldrs['public_data_path'] + os.sep  + 'index' + os.sep + 'ndxAll.txt',
                         fldrs['localPath'] + 'pers_data' + os.sep + 'pers_index_final.txt',
                         fldrs['localPath'] + 'pers_data' + os.sep + 'ndx_PCusage.txt'
                        ]


def read_credentials(fname):
    """
    read a simple text file from a private location to get
    username and password
    """
    with open(fname, 'r') as f:
        username = f.readline().strip('\n')
        password = f.readline().strip('\n')
    return username, password

    
def show_config():
    """
    module intended to be imported in most AIKIF utils
    to manage folder paths, user settings, etc.
    Modify the parameters at the top of this file to suit
    """
    
    print("\n---------- Folder Locations ---------")
    for k,v in fldrs.items():
        print(k,v)
    
    print("\n---------- Logfiles ---------")
    for k,v in logs.items():
        print(k,v)
        
    print("\n---------- Parameters ---------")
    for k,v in params.items():
        print(k,v)
    print("\nusage from other programs - returns " + fldr_root())
    
def fldr_root():
    return fldrs['root_path']

if __name__ == '__main__':    
    show_config()