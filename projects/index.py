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
        out += aa[2][3:-2] + " &nbsp; "
    return out

def got_index(config, url, query, request, template = ""):

    global configx
    configx = config
    #print("got_index() url", url, "query", query, "request", request, "template", template)
    #print("got_index() request_org=", config.mainclass.request_org)

    print("got_index() request", request)

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

    if not template:
        template = wsgi_util.resolve_template(config, url, __file__)
    else:
        template = config.mypath + os.sep + os.path.dirname(__file__) + os.sep + template

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
# Add all the functions for the urls; this function is called
# When the url is accessed

sys.path.append("../")

from wsgi_global import add_one_url

# Add default enties to table
add_one_url("/", got_index, "index.html")
add_one_url("/index.html", got_index, "index.html")

from wsgi_global import add_one_func

add_one_func("feed_data", fill_data)

# EOF