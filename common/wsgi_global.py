#!/usr/bin/env python3

''' These tags / funtions / tables are global to the site '''

import sys

# Get strings and functions

from wsgi_style import *
from wsgi_res   import *
from wsgi_func  import *

# A list of variables and strings

global_table = [
    ["header2", header2],
    ["var", "<font size=+1>variable { deep } </font>"],
    ["no problem", "recursive expansion is not even a <b>little</b> problem ... "],
    ["spacer", "<table><tr><td></table>"],
    ["mycolor", "bgcolor=#aaffbb"],
    ["thumbwidth", "120"],
    ["thumbheight", "80"],
    ["Company Name", "PGlen.com"],
  ]

# ------------------------------------------------------------------------
# URL to function mapping

class UrlMap():

    ''' This calss stores the URL to function mapping '''

    def __init__(self):

        self.urls = []

    def add(self, url, func, page):
        # Got one already?
        for aa in self.urls:
            if aa[0] == url:
                return
        self.urls.append((url, func, page))

    def lookup(self, url):
        #print("Looking up url", url)
        for aa in self.urls:
            #print("src url", aa[0], aa[1])
            if aa[0] == url:
                return aa[1], aa[2]
        return None, None

# URL to function table
urlmap =  UrlMap()

# ------------------------------------------------------------------------
# Add a new project function;

def     add_one_func(mname, mfunc, mpage = None):

    '''
        Add a macro function here. The macro is substituted
        by the output of the function. Macro syntax is words sourrounded by
        '{ ' and ' }' as in { macro }
    '''
    try:
        global_table.append([mname, mfunc])
    except:
        print("Cannot add global table item", sys.exc_info())

# ------------------------------------------------------------------------
# Add functions to URL map
# One may override any file; in that case the values are filled in

# We build it dynamically, so error is flagged

def     add_one_url(url, mfunc, mpage = None):

    '''
    Add a url and a function here. Also, an optional template. The template is assumed
    to be in the same directory as the script. If no template is added, the following
    places will be searched: the project "./" directory,  the /static/ directory.
    If the template cannot be found, the return of the function output is delivered as
    it was generated.
    '''

    global urlmap
    try:
        urlmap.add(url, mfunc, mpage)
    except:
        print("Cannot add url map", sys.exc_info())

    #print("urlmap", urlmap.urls)


def     getprojects():

    '''
        Add (import) projects in this directory for automatic inclusion into the site.
        The initial project dir is called 'projects'
    '''

    ret = []
    try:
        from importlib import import_module

        pdir = "projects"
        sys.path.append(pdir)
        files = os.listdir(pdir)
        for aa in files:
            if aa[-3:] == ".py" and aa != "__init__.py":
                if os.path.exists(pdir + os.sep + aa):
                    #print("importing", aa)
                    try:
                        import_module( aa[:-3])
                    except:
                        wsgi_util.put_exception("Cannot import module: '%s' " % aa)
                        msg = "Module %s failed to load" % aa
                        #print("msg", msg)
                        ret = [msg.encode("utf-8"),]
                        return ret
    except:
        #print("Cannot import guest project", sys.exc_info())
        wsgi_util.put_exception("Cannot import")
        ret = [b"Some modules failed to load"]

    return ret

# EOF

