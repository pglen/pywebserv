#!/usr/bin/env python3

'''
    This is a sample project that is added to the site. The idea here is
    that nothing in this project can syntax error (down) the site.
    It is imported under a try: except clause, and it is calling only the
    URL registration functions.
    Also, included a default web page function as index.html or as '/'
'''

import os, sys, time

import wsgi_util, wsgi_func, wsgi_data, wsgi_global, wsgi_parse

#print("Loading", "'" + os.path.basename(__file__)  + "'" )

gl_config = None

try:
    import macros
except:
    print("Cannot import macros", sys.exc_info())
    wsgi_util.put_exception("import macros")

localdb = None

def got_index(config, url, query, request, template = "", fname = ""):

    global gl_config
    gl_config = config

    print("got_index()", "url:", url, "query:", query)
    print("gl_config:"); print(gl_config.showvals())

    if gl_config.conf.pgdebug > 3:
        print("got_index() url=%s"% url, "query=%s" %query,
                    "request=%s" % request, "template=%s" % template, "fname=%s" % fname)

    if gl_config.conf.verbose:
        print("got_index() url = '%s'" % url, "request_org=", gl_config.mainclass.request_org)

    #print("got_index() request", request)

    #if url == "/":
    #    url = "/index.html"

    if request:
        sss = ""
        # Save it
        for aa in request:
            print(aa)
            if aa[0] == "textx":
                sss = aa[1]
                break
        #print("raw data", sss, type(sss))
        localdb.put("key_" + sss, sss, "", "", "")
        localdb.putlog("log_" + sss, sss, "", "", "")

    #print("loc", macros.local_table)

    content = wsgi_util.process_default(config, url, query, request, template, fname, macros.local_table )
    return content

def fill_data(strx, context):

    global localdb
    if not localdb:
        try:
            localdb = wsgi_data.wsgiSql("data/%s_data.sqlt" % modname)
        except:
            print("Could not create / open local data for %s", modname)

    #print("strx", strx)
    out = ""
    res = localdb.getall()
    for aa in res:
        #out += aa[2][3:-2] + " &nbsp; "
        out += str(aa) + " &nbsp; "
    return out

def got_log(config, url, query, request, template = "", fname = ""):
    content = wsgi_util.process_default(config, url, query, request, template, fname, macros.local_table)
    return content

# ------------------------------------------------------------------------
# Add all the functions for the urls;
# This function is called when the module is loaded
#

def initialize():

    '''
    Initializee the current module
    '''

    try:
        # Add default enties to tables
        wsgi_global.add_one_url("/", got_index, "index.html", __file__)
        wsgi_global.add_one_url("/index.html", got_index, "index.html", __file__)
        wsgi_global.add_one_url("/log.html", got_log, "log.html", __file__)

        #wsgi_global.add_one_func("feed_data", fill_data)
        wsgi_global.add_one_func("CompanyName", "UPP, United Planet Peace")

    except:
        print("Cannot add module globals:", "'" + modname + "'", sys.exc_info())

    global localdb
    #print("Called  initialization for '%s'" % modname)
    if not localdb:
        try:
            localdb = wsgi_data.wsgiSql("data/%s_data.sqlt" % modname)
        except:
            print("Could not create local data for %s", modname)

modname = os.path.splitext(os.path.basename(__file__))[0]

initialize()

# EOF