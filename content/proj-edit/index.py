#!/usr/bin/env python3

'''
    This is a sample project that is added to the site. The idea here is
    that nothing in this project can syntax error (down) the site.
    It is imported under a try: except clause, and it is calling only the
    URL registration functions and macro definitons.
    Also, included a default web page function as index.html or as '/'
'''

import os, sys, time
import wsgi_util, wsgi_func, wsgi_data, wsgi_global

#print("Loading", "'" + os.path.basename(__file__)  + "'" )

ppp = __file__.split('/')
plen = len(ppp)
modname = ppp[plen-2] + "-" + ppp[plen-1]

print("Loaded mod:", modname)

from . import macros

localdb = None

def fill_data(strx, context):

    global localdb
    if not localdb:
        try:
            localdb = wsgi_data.wsgiSql("data/%s_data.sqlt" % modname)
        except:
            print("Could not create local data for %s", modname)

    #print("strx", strx)
    out = ""
    res = localdb.getall()
    for aa in res:
        #out += aa[2][3:-2] + " &nbsp; "
        out += str(aa) + " &nbsp; "
    return out

def got_index(config, url, query, request, template = "", fname = ""):

    if config.pgdebug > 3:
        print("got_index() url=%s"% url, "query=%s" %query,
                    "request=%s" % request, "template=%s" % template, "fname=%s" % fname)

    if config.pgdebug > 0:
        print("editor: got_index() url = '%s'" % url)

    #print("Editor page, cwd:", os.getcwd())
    #print("Config values:", wsgi_conf.showvals())

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

    content = wsgi_util.process_default(config, url, query, request, template, fname, macros.local_table)
    return content

# ------------------------------------------------------------------------
# Add all the functions for the urls;
# This function/code is called when the module is loaded
#

'''
Initializee the current module
'''

#print("Called  initialization for '%s'" % modname)
if not localdb:
    try:
        localdb = wsgi_data.wsgiSql("data/%s_data.sqlt" % modname)
    except:
        print("Could not create local data for %s", modname)

# Upon loading ... add urls and add macros

try:
    #print("Initializing", "'" + __file__ + "'" )
    # Add default enties to table
    wsgi_global.add_one_url("/editor", got_index, "index.html", __file__)
    wsgi_global.add_one_url("/editor/index.html", got_index, "index.html", __file__)

except:
    print("Cannot initialize", modname, sys.exc_info())

#vvv = locals().copy()
#    #print("vvv", vvv)
#    for vv in vvv:
#        if  "macros" in vv:
#            #print("vv", vv, vvv[vv]);
#            for aa in dir(vvv[vv]):
#                #print("aa", aa);
#                if "_mac_" in aa[:5]:
#                    val = getattr(vvv[vv], aa)
#                    print("Added:", aa[5:]) #, val[:12])
#                    add_local_func(aa[5:],  val)

# EOF
