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

def got_resp(config, url, query, request, template = "", fname = ""):

    #print("got_resp() config.mypath=", config.mypath, "url=", url, "query=", query)
    print("got_resp() template=", template, "fname=", fname)

    found = ""
    fn = urlparse(url).path

    if not template:
        template = wsgi_util.resolve_template(config, url, __file__)
    else:
        template = os.path.dirname(__file__) + os.sep + template

    #print("found local file", found)
    if  template:
        #content = "Index file exists " + url + " " +  str(query) +
        with open(template, 'r') as fh:
            buff = fh.read()
        #print("buff", buff)
        # Recursively process
        content = wsgi_util.recursive_parse(buff, __file__)
    else:
        content = "Index file (dyn) " + url + " " +  str(query) + " "
    return content

def my_img_func(arg, context):
    #print("my_img_func", arg)
    #return "image here"
    return ""

def my_style_func(arg, context):
    #print("style func here", arg)
    return "style here"

# Expand arguments

def siteicon_func(arg, context):
    ssss = wsgi_util.recursive_parse(arg, context, "\[ .*? \]")
    sss = ssss.split()
    # Concat arguments to str
    strx = "\""
    for aa in  sss[3:-1]:
        strx += aa + " "
    strx += "\""

    #print("strx", strx)

    cwd = os.path.dirname(os.getcwd())
    print("cwd", cwd)

    # Travel down the dependency list
    while True:
        fname = os.path.dirname(context) + os.sep + sss[2]
        if os.path.isfile(fname):
            break
        fname = cwd + os.sep + "content/siteicons" + os.sep + sss[2]
        if os.path.isfile(fname):
            fname = fname[len(cwd)+8:]
            break
        fname = cwd + os.sep + "content/media" + os.sep + sss[2]

        if os.path.isfile(fname):
            fname = fname[len(cwd)+8:]
            break
        fname = cwd + os.sep + "content/html" + os.sep + sss[2]
        if os.path.isfile(fname):
            fname = fname[len(cwd)+8:]
            break
        break

    #if not os.path.isfile(fname):
    #    print("Icon file does not exist")

    return "<img src=" + fname + " title=" + strx + ">"

# ------------------------------------------------------------------------
# Add all the functions for the urls; this function is called
# When the url is accessed

sys.path.append("../")

from wsgi_global import add_one_url

add_one_url("/test/responsive", got_resp, "", __file__)

# ------------------------------------------------------------------------
# Add all the functions and the macro names here
# Simply refer to the macro in the html temple, and it will get called
# and the output substituted

from wsgi_global import add_one_func

add_one_func("image2", my_img_func)
add_one_func("style", my_style_func)
add_one_func("siteicon", siteicon_func)
add_one_func("forw", "media-skip-backward.png")

#add_one_func("include", include_function)

# EOF