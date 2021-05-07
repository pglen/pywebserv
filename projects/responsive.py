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

def got_resp(config, url, query, request, template = ""):

    #print("got_resp() config.mypath", config.mypath, "url", url, "query", query)
    found = ""
    fn = urlparse(url).path

    if not template:
        template = wsgi_util.resolve_template(config, url, __file__)

    #print("found local file", found)
    if  template:
        #content = "Index file exists " + url + " " +  str(query) +
        with open(template, 'r') as fh:
            buff = fh.read()
        #print("buff", buff)
        # Recursively process
        content = wsgi_util.recursive_parse(buff)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " "
    return content

def     my_img_func(arg):
        print("my_img_func", arg)

# ------------------------------------------------------------------------
# Add all the functions for the urls; this function is called
# When the url is accessed

sys.path.append("../")

from wsgi_global import add_one_url

add_one_url("/responsive", got_resp)
add_one_url("/responsive.html", got_resp)
add_one_url("/rr", got_resp)

# ------------------------------------------------------------------------
# Add all the functions and the macro names here
# Simply refer to the macro in the html temple, and it will get called
# and the output substituted

from wsgi_global import add_one_func

add_one_func("image2", my_img_func)

# EOF