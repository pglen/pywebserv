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

def got_resp(config, url, query):

    #print("got_resp() config.mypath", config.mypath, "url", url, "query", query)
    found = ""
    fn = urlparse(url).path

    # Iterate 'lookfor' combos; the html template can be local, html static,
    while True:
        fn1 = config.mypath + os.sep  + __file__[:-3] + ".html"
        print("fn1", fn1)
        if  os.path.exists(fn1):
            found = fn1
            break

        fn2 = config.mypath + os.sep + "html"  + fn
        print("fn2", fn2)
        if  os.path.exists(fn2):
            found = fn2
            break

        fn3 = config.mypath + os.sep + "html" + fn + ".html"
        print("fn3", fn3)
        if  os.path.exists(fn3):
            found = fn3
            break
        break;

    #print("found local file", found)
    if  found:
        #content = "Index file exists " + url + " " +  str(query) +
        with open(found, 'r') as fh:
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
add_one_url("/rr", got_resp)

# ------------------------------------------------------------------------
# Add all the functions and the macro names here
# Simply refer to the macro in the html temple, and it will get called
# and the output substituted

from wsgi_global import add_one_func

add_one_func("image2", my_img_func)

# EOF