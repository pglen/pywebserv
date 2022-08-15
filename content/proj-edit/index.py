#!/usr/bin/env python3

'''
    This is a sample project that is added to the site. The idea here is
    that nothing in this project can syntax error (down) the site.
    It is imported under a try: except clause, and it is calling only the
    URL registration functions and macro definitons.
    Also, included a default web page function as index.html or as '/'
'''

import os, sys, time
import wsgi_util, wsgi_func, wsgi_data, wsgi_global, wsgi_swear

#print("Loading", "'" + os.path.basename(__file__)  + "'" )

ppp = __file__.split('/')
plen = len(ppp)
modname = ppp[plen-2] + "-" + ppp[plen-1]
projname = ppp[plen-2]

#print("Loaded proj:", projname)
#print("Loaded mod:", modname)

from . import macros
from . import editor
from . import common

localdb = None

def got_index(config, url, query, request, template = "", fname = ""):

    if config.pgdebug > 3:
        print("got_index() url=%s"% url, "query=%s" %query,
                    "request=%s" % request, "template=%s" % template )# , "fname=%s" % fname)

    if config.pgdebug > 0:
        print("editor: got_index() url = '%s'" % url)

    if request:
        rq = []
        for aa in request:
            rq.append(aa[1])

        #print("data", rq)
        #print("database", "data/%s.sqlt" % projname)

        try:
            #startt = time.perf_counter()
            localdb = wsgi_data.wsgiSql("data/%s.sqlt" % projname)
            localdb.put("key_" + rq[0], rq[0], rq[1], rq[2], "")
            localdb.close()
            # Measure time needed
            #print("database op %f msec " %  ((time.perf_counter() - startt) * 1000))
        except:
            print("Cannot put data")
            wsgi_util.put_exception("in index data")

    wcontext = wsgi_util.wContext(config, url, query)
    wcontext.request    = request
    wcontext.template   = template
    wcontext.fname      = fname
    wcontext.local_table = common.local_table

    content = wsgi_util.process_default2(wcontext)

    try:
        localdb = wsgi_data.wsgiSql("data/%s.sqlt" % projname)
        #localdb.putlog("log_" + sss, sss, "", "", "")
        localdb.close()
    except:
        print("Cannot put log data")
        wsgi_util.put_exception("in index data")

    return content

# ------------------------------------------------------------------------
# Add all the functions for the urls;
# This function/code is called when the module is loaded
#

'''
Initialize the current module
'''

try:
    #print("Initializing", "'" + __file__ + "'" )
    # Add default enties to table
    wsgi_global.add_one_url("/editor/", got_index,   "index.html", __file__)
    wsgi_global.add_one_url("/editor/index.html",   got_index, "index.html", __file__)
    wsgi_global.add_one_url("/editor/editor.html",  editor.got_editor, "editor.html", __file__)

except:
    print("Cannot initialize", modname, sys.exc_info())

# EOF


