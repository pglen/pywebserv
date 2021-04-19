#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time, re
import multiprocessing
from wsgiref import simple_server, util

# Persitent info here

myglobal = 1234

from wsgi_global import *
from wsgi_util import *

local_table = [
                ["crap", "Just a crappy message"],
              ]

# No tag found, search local items
#    for aa in local_table:
#        if item[2:-2] == aa[0]:
#            return aa[1]

def got_aa(config, url, query):
    content = "AA file " + url + str(query) + " " + str(myglobal)
    return content

def got_bb(config, url, query):
    content = "bb file " + url + str(query) + " " + str(myglobal)
    return content

def got_index(config, url, query):

    #print("conf", config.mypath)

    fn2 = config.mypath + os.sep + url
    if  os.path.exists(fn2):
        content = "Index file exists " + url + " " +  str(query) + " " + str(myglobal)
        with open(fn2, 'r') as fh:
            buff = fh.read()

        #print("buff", buff)
        # Recursively process
        content = buff
        while(True):
            arr, cnt = parse_buffer(content)
            content = ""
            for aa in arr:
                content += aa

            print("recursive", cnt)
            if cnt <= 1:
                break

    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " " + str(myglobal)
    return content

# ------------------------------------------------------------------------

def     generate_content(url, query):

    print("Request:",  url)
    translate_url(url)
    content = "hello world, url="  + url
    return [bytes(content, "utf-8")]

# ------------------------------------------------------------------------
# Add functions to URL map
# One may override any file; in that case the values are filled in

def reg_all(urlmap):

    urlmap.add("/aa", got_aa)
    urlmap.add("/bb", got_bb)
    urlmap.add("/index.html", got_index)

# EOF


