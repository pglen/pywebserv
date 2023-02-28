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

    if carry.query:
        print("idx carry.query", carry.query)

    if carry.request:
        #print("idx carry.request", carry.request)
        rq = [] ; par = []
        for aa in carry.request:
            rq.append(aa[1])
            par.append(aa[0])

        #print("data rq", rq)
        if len(rq) == 1:
            if "Confirm" in rq[0]:
                sss = par[0].split("_")
                print("rq del id: ", sss[1]);
                wsgi_data.soft_opendb(carry, modname)
                carry.localdb.delrecall(sss[1])
        else:
            try:
                #startt = time.perf_counter()
                wsgi_data.soft_opendb(carry, modname)
                carry.localdb.put(rq[0], rq[1], rq[2], rq[3], rq[4], rq[5])
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
    # These are test entries
    #wsgi_global.urlmap.add_one_url("/editor2/", got_index,   "index.html", __file__)
    #wsgi_global.urlmap.add_one_url("/editor", got_index,   "index.html", __file__)

    # Add default enties to table
    wsgi_global.urlmap.add_one_url("/editor/", got_index, "index.html", __file__)
    wsgi_global.urlmap.add_one_url("/editor/index.html",  got_index, "index.html", __file__)
    wsgi_global.urlmap.add_one_url("/editor/editor.html", editor.got_editor, "editor.html", __file__)

    #wsgi_util.dump_table("Global Table", wsgi_global.global_table)
    #wsgi_util.dump_global_table()

except:
    print("Cannot initialize", modname, sys.exc_info())

# EOF
