#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time, re
import multiprocessing
from wsgiref import simple_server, util

from wsgi_global import *

nogo = ("OPENHAB", "XDG_", "LS_", "SHELL", "SESSION", "QT",
             "LESS", "SSH", "GTK", "SHLVL", )

def printenv(environ):
    for aa in environ.keys():
        #print("aa", aa)
        fff = True
        for cc in nogo:
            if cc in aa:
                fff = False
        #if fff:
        #    print(aa, environ[aa])

        if "HTTP" in aa:
            print(aa, environ[aa])


# URL to function mapping

class UrlMap():

    def __init__(self):
        self.urls = []

    def add(self, url, func):
        self.urls.append((url, func))

    def lookup(self, url):
        for aa in self.urls:
            if aa[0] == url:
                return aa[1]
        return None

# Parse buffer

def parse_buffer(buff):

    count = 0
    prog = 0
    rrr = re.compile("{ .*? }", )
    arr = []
    while(True):
        frag = re.search(rrr, buff[prog:])
        if not frag:
            arr.append(buff[prog:])
            break
        #print ("match", frag)
        bbb = prog+frag.start()
        eee = prog+frag.end()
        arr.append(buff[prog:bbb])
        conv = global_items(buff[bbb:eee])
        arr.append(conv)
        prog += frag.end()
        count += 1

    #print ("arr", arr)
    return arr, count
