#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time, re

# Persitent info here

import  wsgi_util, wsgi_data

# No tag found, search local items

def got_404(config, url, query):

    if  os.path.exists(url):
        with open(url, 'r') as fh:
            buff = fh.read()
        # Recursively process
        content = wsgi_util.recursive_parse(buff)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " "
    return content

def got_500(config, url, query):

    fn2 = config.mypath + os.sep + url
    if  os.path.exists(fn2):
        with open(fn2, 'r') as fh:
            buff = fh.read()
        # Recursively process
        content = wsgi_util.recursive_parse(buff)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " "
    return content

# EOF


