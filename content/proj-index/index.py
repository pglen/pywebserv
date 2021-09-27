#!/usr/bin/env python3

'''
    This is a sample project that is added to the site. The idea here is
    that nothing in this project can syntax error (down) the site, as it is
    imported under a try: except clause, and it is calling only the
    URL registration functions
    Also, included a default web page function as index.html or as '/'
'''

import os, sys, random, datetime, time, codecs
import wsgi_util, wsgi_func

def fill_data(strx):
    global configx
    #print("strx", strx)
    out = ""
    res = configx.mainclass.sql.getall()
    for aa in res:
        #out += aa[2][3:-2] + " &nbsp; "
        out += str(aa) + " &nbsp; "
    return out

def got_index(config, url, query, request, template = "", fname = ""):

    global configx
    configx = config
    #print("got_index() url", url, "query", query, "request", request, "template", template, "fname", fname)
    #print("got_index() request_org=", config.mainclass.request_org)
    #print("got_index() request", request)

    if url == "/":
        url = "/index.html"

    if request:
        sss = ""
        # Save it
        for aa in request:
            print(aa)
            if aa[0] == "textx":
                sss = aa[1]
                break

        print("raw data", sss, type(sss))
        config.mainclass.sql.put("key_" + sss, sss, "", "", "")
        config.mainclass.sql.putlog("log_" + sss, sss, "", "", "")

    if not template:
        template = wsgi_util.resolve_template(config, url, __file__)
    else:
        template = os.path.dirname(__file__) + os.sep + template

    #print("using template", template)

    if template and os.path.exists(template):
        #content = "Index file exists " + url + " " +  str(query) + " "
        with open(template, 'r') as fh:
            buff = fh.read()
        # Recursively process
        content = wsgi_util.recursive_parse(buff)
    else:
        content = "Index file (dyn) " + url + " " +  template + " " + str(query) + " "
    return content

# ------------------------------------------------------------------------
# Add all the functions for the urls;
# This function is called when the module is loaded
#

from wsgi_global import add_one_url

def initialize():
    print("called initialization")
    pass

modfname = os.path.basename(__file__)
try:
    #print("initiaizing", modfname)
    sys.path.append("../")
    # Add default enties to table
    add_one_url("/", got_index, "index.html", __file__)
    add_one_url("/index.html", got_index, "index.html", __file__)
    from wsgi_global import add_one_func
    add_one_func("feed_data", fill_data)
except:
    print("Cannot initialize", modfname, sys.exc_info())

# EOF