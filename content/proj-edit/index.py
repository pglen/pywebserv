#!/usr/bin/env python3

'''
    This is a sample project that is added to the site. The idea here is
    that nothing in this project can syntax error (down) the site.
    It is imported under a try: except clause, and it is calling only the
    URL registration functions and macro definitons.
    Also, included a default web page function as index.html or as '/'
'''

import os, sys, time
import wsgi_util, wsgi_func, wsgi_data, wsgi_global,  wsgi_util

#print("Loading", "'" + os.path.basename(__file__)  + "'" )
modname = __file__.split('/')[-2]
#print("Loaded mod:", modname)

from . import macros
from . import editor
from . import common

def got_index(config, carry):

    if config.verbose > 1:
        print("got_index() url", carry.url)

    if config.pgdebug > 1:
        print("got_index()", "url:", carry.url, "request:", carry.request)

    if config.pgdebug > 2:
        print(config.getvals())

    if config.pgdebug > 3:
        print("got_index() url=%s"% carry.url, "query=%s" % carry.query,
                    "request=%s" % carry.request,
                         "template=%s" % carry.template, "fname=%s" % carry.fname)

    if carry.request:

        #print("carry.request", carry.request)

        rq = []
        for aa in carry.request:
            rq.append(aa[1])

        print("data rq", rq)
        #print("save to database", "data/%s.sqlt" % modname)
        try:
            #startt = time.perf_counter()
            wsgi_data.soft_opendb(carry, modname)

            #localdb = wsgi_data.wsgiSql("data/%s.sqlt" % modname)
            carry.localdb.put(rq[0], rq[1], rq[2], rq[3], "")

            #localdb.close()
            # Measure time needed
            #print("database op %f msec " %  ((time.perf_counter() - startt) * 1000))
        except:
            print("Cannot put data")
            wsgi_util.put_exception("in index data")

    carry.local_table = common.local_table
    content = wsgi_util.process_default(config, carry)
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
    wsgi_global.urlmap.add_one_url("/editor/", got_index,   "index.html", __file__)
    #wsgi_global.add_one_url("/editor", got_index,   "index.html", __file__)
    wsgi_global.urlmap.add_one_url("/editor/index.html",  got_index, "index.html", __file__)
    wsgi_global.urlmap.add_one_url("/editor/editor.html",  editor.got_editor, "editor.html", __file__)

    #wsgi_util.dump_table("Global Table", wsgi_global.global_table)
    #wsgi_util.dump_global_table()

except:
    print("Cannot initialize", modname, sys.exc_info())


# EOF
