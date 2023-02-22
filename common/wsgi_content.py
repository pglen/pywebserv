#!/usr/bin/env python3

''' The simplest web server
    data module for error files
'''

import sys, os, mimetypes, time, re

# Persitent info here

import  wsgi_util, wsgi_data, wsgi_parse, wsgi_global, wsgi_str

def got_404(context, url, query, fn = ""):

    '''! The error file from 404
    '''

    #print("404", context)

    local_table = []
    fn2 = wsgi_str.strtrim(os.path.basename(fn))
    wsgi_util.add_local_func("errfname", fn2, local_table)

    #wsgi_util.dump_table("Local Table", local_table)
    #wsgi_util.dump_table("Global Table", wsgi_global.gl_table.mytable)

    if  os.path.isfile(url):
        with open(url, 'r') as fh:
            buff = fh.read()
        # Recursively process
        content = wsgi_parse.recursive_parse(buff, context, local_table)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " "
    return content

def got_500(context, url, query):

    '''!
        The error file from 500
    '''

    local_table = []
    #fn2 = config.mypath + os.sep + url
    if  os.path.isfile(url):
        with open(url, 'r') as fh:
            buff = fh.read()
        # Recursively process

        content = wsgi_parse.recursive_parse(buff, context, local_table)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " "
    return content

# EOF


