#!/usr/bin/env python3

'''
    This is a sample project that is added to the site. The idea here is
    that nothing in this project can down the site, oly the page. (like: syntax error)
    It is imported under a try: except clause, and it is calling only the
    URL registration functions.
    Also, included a default web page function as index.html or as '/'
'''

import os, sys, time

import wsgi_util, wsgi_func, wsgi_data, wsgi_global, wsgi_parse

#print("Loading", "'" + os.path.basename(__file__)  + "'" )

ppp = __file__.split('/')
plen = len(ppp)
modname = ppp[plen-2] + "-" + ppp[plen-1]

print("Loaded mod:", modname)

from . import macros, swear

def got_index(config, url, query, request, template = "", fname = ""):

    #print("got_index()", "url:", url, "query:", query)
    #print(wsgi_conf.config.showvals())

    if Config.pgdebug > 3:
        print("got_index() url=%s"% url, "query=%s" %query,
                    "request=%s" % request, "template=%s" % template, "fname=%s" % fname)
    if Config.verbose:
        print("got_index() url = '%s'" % url)

    if request:
        process_submit(request)

    content = wsgi_util.process_default(config, url, query, request, template, fname, macros.local_table )
    return content

def fill_data(strx, context):

    try:
        localdb = wsgi_data.wsgiSql("data/%s_data.sqlt" % modname)
    except:
        print("Could not create / open local data for %s", modname)

    #print("strx", strx)
    out = ""
    res = localdb.getall()
    for aa in res:
        out += "'" + aa[1] + "'  &nbsp;  '" + aa[2] + "' &nbsp; '" + aa[3] + "'<br>"
    localdb.close()
    return out

def got_log(config, url, query, request, template = "", fname = ""):
    content = wsgi_util.process_default(config, url, query, request, template, fname, macros.local_table)
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
    for aa in request[:-1]:  # do not post last (submit entry)
        bb = swear.filter_words(aa[1])
        #print("de-sweared", bb)
        sss.append(bb)

    #print("raw data", str(request), sss, type(sss))

    try:
        localdb = wsgi_data.wsgiSql("data/%s_data.sqlt" % modname)
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
    wsgi_global.add_one_url("/", got_index, "index.html", __file__)
    wsgi_global.add_one_url("/index.html", got_index, "index.html", __file__)
    wsgi_global.add_one_url("/log.html", got_log, "log.html", __file__)

    wsgi_global.add_one_func("show_submit", show_submit_func)
    wsgi_global.add_one_func("feed_data", fill_data)
    wsgi_global.add_one_func("CompanyName", "UPP, United Planet Peace")

except:
    print("Cannot add module globals:", "'" + modname + "'", sys.exc_info())

# EOF