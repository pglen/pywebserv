#!/usr/bin/env python3

''' The simplest web server
    data module for error files
'''

import sys, os, mimetypes, time, re

# Persitent info here

import  wsgi_util, wsgi_data, wsgi_parse, wsgi_global

def got_404(config, url, query):

    '''! The error file from 404
    '''
    if  os.path.exists(url):
        with open(url, 'r') as fh:
            buff = fh.read()
        # Recursively process
        content = wsgi_parse.recursive_parse(buff, None, None)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " "
    return content

def got_500(config, url, query):

    '''! The error file from 500
    '''

    #fn2 = config.mypath + os.sep + url
    if  os.path.exists(url):
        with open(url, 'r') as fh:
            buff = fh.read()
        # Recursively process
        content = wsgi_parse.recursive_parse(buff, None, None)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " "
    return content

# EOF


