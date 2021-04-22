#!/usr/bin/env python3

# These tags are global to the site

import sys

# Get strings and functions

from wsgi_style import *
from wsgi_res   import *
from wsgi_func  import *

# A list of variables and strings / functions

global_table = [
    ["header2", " <font size=+2>Sub Header here</font>"],
    ["var", "<font size=+1>variable { deep } </font>"],
    ["no problem", "recursive expansion is not even a <b>little</b> problem ... "],
    ["spacer", "<table><tr><td></table>"],
    ["mycolor", "bgcolor=#aaffbb"],
    ["thumbwidth", "120"],
    ["thumbheight", "80"],
    ["Company Name", "PGlen Computing"],
  ]

# ------------------------------------------------------------------------
# Add a new project;

def add_one_func(mname, mfunc, mpage = None):

    try:
        global_table.append([mname, mfunc])
    except:
        print("Cannot add global table item", sys.exc_info())


# ------------------------------------------------------------------------
# URL to function mapping

class UrlMap():

    def __init__(self):
        self.urls = []

    def add(self, url, func):
        # Got one already?
        for aa in self.urls:
            if aa[0] == url:
                return
        self.urls.append((url, func))

    def lookup(self, url):
        for aa in self.urls:
            #print("urls", aa[0], aa[1])
            if aa[0] == url:
                return aa[1]
        return None

# URL to function table
urlmap =  UrlMap()

# ------------------------------------------------------------------------
# Add functions to URL map
# One may override any file; in that case the values are filled in

# We build it dynamically, so error is flagged

def add_one_url(url, mfunc, mpage = None):

    global urlmap
    try:
        urlmap.add(url, mfunc)
    except:
        print("Cannot add url map", sys.exc_info())
    #print("urlmap", urlmap.urls)

def build_table():

    try:
        add_one_func("header", header)
        add_one_func("footer", footer)
        add_one_func("bigtext", bigtext)
        add_one_func("deep", deep_func)
        add_one_func("crap", crap_func)
        add_one_func("app_one", app_one_func)
        add_one_func("app2", app_two_func)
        add_one_func("image", image_func)
        add_one_func("mystyle", mystyle)
        add_one_func("imgrow", imgrow)
        add_one_func("article", article)
        add_one_func("article2", article2)

    except:
        print("Cannot build global table", sys.exc_info())

build_table()

# ------------------------------------------------------------------------
# Add projects here

#def getproject(proj):

try:
    from projects.wsgi_proj import *
except:
    print("Cannot import guest project", sys.exc_info())

# EOF







