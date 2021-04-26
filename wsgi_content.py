#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time, re
import multiprocessing
from wsgiref import simple_server, util

# Persitent info here

myglobal = 1234

import wsgi_util

local_table = [
                ["crap", "Just a crappy message"],
              ]

# No tag found, search local items

def got_index(config, url, query):

    #print("got_index() conf", config.mypath, "url", url, "query", query)
    #print("type", config.mainclass.method)
    #print("request", config.mainclass.request)

    print("request", str(config.mainclass.request))

    if url == "/":
        url = "/index.html"
    fn2 = config.mypath + os.sep + "/html" + os.sep + url
    if  os.path.exists(fn2):
        #content = "Index file exists " + url + " " +  str(query) + " " + str(myglobal)
        with open(fn2, 'r') as fh:
            buff = fh.read()
        #print("buff", buff)
        # Recursively process
        content = "" #str(config.mainclass.request)
        content += wsgi_util.recursive_parse(buff)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " " + str(myglobal)
    return content

def got_404(config, url, query):

    if  os.path.exists(url):
        with open(url, 'r') as fh:
            buff = fh.read()
        # Recursively process
        content = wsgi_util.recursive_parse(buff)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " " + str(myglobal)

    return content

def got_500(config, url, query):

    fn2 = config.mypath + os.sep + url
    if  os.path.exists(fn2):
        with open(fn2, 'r') as fh:
            buff = fh.read()
        # Recursively process
        content = wsgi_util.recursive_parse(buff)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " " + str(myglobal)
    return content

# EOF


