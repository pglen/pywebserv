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

from . import macros
from . import common

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

    content = ""

    #print("carry.request", carry.request)
    #print("carry.query", carry.query)

    carry.prog = carry.prog2 = 0
    if carry.query:
        if "step" in carry.query:
            iii = wsgi_util.xint(carry.query['step'][0])
            carry.prog = iii
        if "step2" in carry.query:
            iii = wsgi_util.xint(carry.query['step2'][0])
            carry.prog2 = iii

    if carry.request:
        process_submit(carry.request)

    # Decorate before calling main
    carry.local_table = common.local_table

    # Load data (needs early load, so do the function)
    #<!-- needs to preload data before everything -->

    # Call these before parse; if used as a macro it will not load
    # as the parser is not a multi pass parser (not practical in python)
    wsgi_data.load_data_func("load_data proj-rows", carry)
    wsgi_data.load_data_func("load_data proj-edit", carry)

    content += wsgi_util.process_default(config, carry)
    return content

def got_log(config, carry):

    carry.local_table = common.local_table
    content = wsgi_util.process_default(config, carry)
    return content

# This can be shown on an HTML page

def show_submit_func(strx, context):
    strz =  "Submit here:"
    print(strz, Config.tostr())
    print(Config.mainclass.request)
    eee = str(Config.mainclass.request)
    #eee = "<br>" + wsgi_util.gethttpenv(Config.mainclass.environ)
    #eee = wsgi_util.getwenv(Config.mainclass.environ)
    return context, " ", eee

def process_submit(request):

    #print(Config.mainclass.request)

    sss = []
    # Save it
    for aa in request[:-1]:  # do not post last (submit button entry)
        bb = wsgi_swear.filter_words(aa[1])
        #print("de-sweared", bb)
        sss.append(bb)

    #print("raw data", str(request), sss, type(sss))

    try:
        localdb = wsgi_data.wsgiSql("data/%s.sqlt" % modname)
    except:
        print("Could not create / open local data for %s", modname)

    #print("sss", sss)
    localdb.put(sss[0], sss[1], sss[2], "", "")
    localdb.close()

# ------------------------------------------------------------------------
# Add all the functions for the urls;
# This function is called when the module is loaded
#

'''
Initialize the current module
'''

try:
    # Add default enties to tables
    wsgi_global.urlmap.add_one_url("/", got_index, "index.html", __file__)
    wsgi_global.urlmap.add_one_url("/index.html", got_index, "index.html", __file__)
    wsgi_global.urlmap.add_one_url("/log.html", got_log, "log.html", __file__)

    #wsgi_global.urlmap.add_one_url("/test_resize.html", got_index, "test_resize.html", __file__)
    wsgi_global.gl_table.add_one_func("show_submit", show_submit_func)

    wsgi_global.gl_table.add_one_func("CompanyName", "UPP, United Planet Peace")
    #wsgi_global.gl_table.add_one_func("fill_data", fill_data)

except:
    print("Cannot add module globals:", "'" + modname + "'", sys.exc_info())

# EOF