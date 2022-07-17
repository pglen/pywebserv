#!/usr/bin/env python3

# ------------------------------------------------------------------------
# This is a sample project that is added to the site. The idea here is
# that nothing in this project can syntax error (down) the site, as it is
# imported under a try: except clause, and it is calling only the
# URL registration functions
# ------------------------------------------------------------------------

import os, sys, random, datetime, time
from urllib.parse import urlparse, unquote, parse_qs

ppp = __file__.split('/'); plen = len(ppp)
modname = ppp[plen-2] + "-" + ppp[plen-1]

print("Loaded mod:", modname)

import wsgi_global, wsgi_util, wsgi_func, wsgi_parse

def got_resp(config, url, query, request, template = "", fname = ""):

    #print("got_resp() config.mypath=", config.mypath, "url=", url, "query=", query)
    #print("got_resp() template=", template, "fname=", fname)

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
        content = wsgi_parse.recursive_parse(buff, __file__, None)
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

# Expand arguments:
#   image _name tooltip_str

def siteicon_func(arg, context):

    ssss = wsgi_parse.parse_buffer(arg, "\[ .*? \]", context, wsgi_global.global_table)[0]
    ss = ""
    for aa in ssss:  ss += aa
    sss = str.split(ss)
    #print("args spaced:", sss)
    if len(sss) < 4:
        sss.append("Icon")

    cwd = os.path.dirname(os.getcwd())
    #print("cwd", cwd)

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

    # Concatinate remaining arguments
    mmm = "'"
    for ss in sss[3:len(sss)-1]:  mmm += ss + " "
    mmm += "'"
    return "<img src=" + fname + " title=" + mmm + ">"

# ------------------------------------------------------------------------
# Add all the functions for the urls; this function is called
# When the url is accessed

wsgi_global.add_one_url("/responsive", got_resp, "responsive.html", __file__)

# ------------------------------------------------------------------------
# Add all the functions and the macro names here
# Simply refer to the macro in the html temple, and it will get called
# and the output substituted

wsgi_global.add_one_func("image2", my_img_func)
wsgi_global.add_one_func("style", my_style_func)
wsgi_global.add_one_func("siteicon", siteicon_func)
wsgi_global.add_one_func("forw", "media-skip-forward.png")

# EOF