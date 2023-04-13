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

def _func_center_donate(strx, context):

    contents = '''<center><h1>Donations</h1></center>'''

    contents += '''<table width=100%% border=0><tr><td>
    &nbsp; &nbsp; As a new organization we need donations for many many aspects of our
    operation. Resources for renting our home office, and all the expenses that
    go along with the physical location. We already have some foundational
    resources, but more needed to hire personnel. Of course, the largest
    expense is letting our presence known in the world.
    <p>
    &nbsp; &nbsp; Establishing a legal department is also on the top of our organizational
     list. Extending our
    IT infrastructure to be more interactive to allow us to create the forum
    that is global, and listen to ideas, collect them / implement them for the benefit
    of all.
    <p>
    &nbsp; &nbsp; Please contact us with details of your donation at
    admin@unitesplanetpeace.com. One may also donate to the founder of
    unitedplanetpeace.com on Paypal Below:
    <p>
    <a href= https://www.paypal.com/donate/?hosted_button_id=B37Q8LJY5KZSY>
    <center><font size=+1> [ Donate to United Planet Peace ] </font></center> </a>
    </table>
    <p>
    &nbsp; &nbsp; ... or contact us with donation details:
     <p>
    <table width=100%% border=0>

    <tr><td>&nbsp; &nbsp; <td> Peter Glen: <td>PeterGlen@unitedplanetpeace.com
    <tr><td>&nbsp; &nbsp; <td> Administrator: <td>  admin@unitedplanetpeace.com
    <tr><td>&nbsp; &nbsp; <td> Founder:    <td> peterglen99@gmail.com

    </table>   <p>

    <center><img src=%s> <center>

    <p><center><a href=/index.html>
     [ Back to Home Page ]</center></a> <p>

     ''' %  "/static/QRCode.png"

    return contents

#(context.configx.datapath + "static/QRCode.png")

# ------------------------------------------------------------------------
# Add all the functions for the urls;
# This function is called when the module is loaded
#

'''
Initialize the current module
'''

try:
    # Add default enties to tables
    wsgi_global.urlmap.add_one_url("/donate/", got_index, "index.html", __file__)
    wsgi_global.urlmap.add_one_url("/donate/index.html", got_index, "index.html", __file__)
    wsgi_util.add_all_vars(locals().copy(), local_table)
except:
    print("Cannot add module globals:", "'" + modname + "'", sys.exc_info())

