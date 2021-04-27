#!/usr/bin/env python3

# ------------------------------------------------------------------------
# This is a sample project that is added to the site. The idea here is
# that nothing in this project can syntax error (down) the site, as it is
# imported under a try: except clause, and it is calling only the
# URL registration functions
# ------------------------------------------------------------------------

import os, sys, random, datetime, time
from urllib.parse import urlparse, unquote, parse_qs

import wsgi_util, wsgi_func

def got_index(config, url, query, template = ""):

    #print("got_index() conf", config.mypath, "url", url, "query", query, "template", template)
    #print("request", str(config.mainclass.request))

    if url == "/":
        url = "/index.html"

    if not template:
        template = wsgi_util.resolve_template(config, url, __file__)
    else:
        template = config.mypath + os.sep + os.path.dirname(__file__) + os.sep + template

    #print("using template", template)

    if template and os.path.exists(template):
        #content = "Index file exists " + url + " " +  str(query) + " "
        with open(template, 'r') as fh:
            buff = fh.read()

        #print("buff", buff)
        # Recursively process
        content = "" #str(config.mainclass.request)
        content += wsgi_util.recursive_parse(buff)
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

