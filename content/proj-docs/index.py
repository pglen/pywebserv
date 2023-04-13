#!/usr/bin/env python3

'''
    This is a sample project that is added to the site. The idea here is
    that nothing in this project can down the site, can down only the page.
    (like a syntax error)
    It is imported under a try: except clause, and it is calling only the
    URL registration functions.
    Also, included a default web page function as index.html or as '/'

    The statement above turns out to be false, if this file contains
    items the site is dependent upon. Naturally, this goes without saying.
'''

import os, sys, time

import wsgi_util, wsgi_func, wsgi_data
import wsgi_global, wsgi_parse, wsgi_swear, wsgi_conf

ppp = __file__.split('/')
modname = ppp[-2]
#print("Loaded mod:", modname)

#from . import macros
#from . import common

local_table = []

def got_index(config, carry):

    if config.verbose > 1:
        print("got_index() url = '%s'" % carry.url)

    if config.pgdebug > 1:
        print("got_index()", "url:", carry.url, "query:", carry.query)

    if config.pgdebug > 2:
        print("wsgi_conf", config.getvals())

    if config.pgdebug > 3:
        print("got_index() url=%s"% carry.url, "query=%s" % carry.query,
                    "request=%s" % carry.request,
                         "template=%s" % carry.template, "fname=%s" % carry.fname)

    #print("carry.request", carry.request)
    #print("carry.query", carry.query)
    carry.local_table = local_table
    content = wsgi_util.process_default(config, carry)
    return content

def _func_center_docs(strx, context):

    contents = "<center><h1>Documents</h1></center>"
    contents += "<table border=0><tr><td>"
    contents += "<font size=+1>"
    contents += '''&nbsp; &nbsp; Here you see a list of documents that are
    submitted to the site.
    Choose a link of interest. If you have a document that
    you would like to include, please email the admin. <p>
    '''

    ddd = context.configx.datapath + "/docs/"
    lll = os.listdir(ddd)
    for aa in lll:
        if aa[-3:] != "odt":
            contents += "<a href=" + "/docs/" + os.sep + aa + ">"
            contents += " [ " + aa + " ]  </a> &nbsp; &nbsp;"
    contents += "<p>"
    contents += "Originals in open document format:<p>"
    for aa in lll:
        if aa[-3:] == "odt":
            contents += "<a href=" + "/docs/" + os.sep + aa + ">"
            contents += " [ " + aa + " ]  </a> &nbsp; &nbsp;"
    contents += "</font><p>"

    contents += "<center><a href=/index.html>"
    contents += " [ Back to Home Page ]</center> "
    contents += "</table>"

    return contents
# ------------------------------------------------------------------------
# Add all the functions for the urls;
# This function is called when the module is loaded
#

'''
Initialize the current module
'''

try:
    # Add default enties to tables
    wsgi_global.urlmap.add_one_url("/docs/", got_index, "index.html", __file__)
    wsgi_global.urlmap.add_one_url("/docs/index.html", got_index, "index.html", __file__)
    wsgi_util.add_all_vars(locals().copy(), local_table)
except:
    print("Cannot add module globals:", "'" + modname + "'", sys.exc_info())

