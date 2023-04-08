#!/usr/bin/env python3

'''
    This is a sample project that is added to the site. The idea here is
    that nothing in this project can syntax error (down) the site.
    It is imported under a try: except clause, and it is calling only the
    URL registration functions and macro definitons.
    Also, included a default web page function as index.html or as '/'
'''

import os, sys, time, uuid
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

    #carry.mydb =  modname #"prog-edit"
    carry.mydb =  "proj-rows"
    print("carry cookies", carry.mainclass.good_cookies)
    if not "Auth" in carry.mainclass.good_cookies:
        print("need auth")
        try:
            sess = str(uuid.uuid4())
            carry.mainclass.wanted_cookies.append(("Auth", sess, 1))
            pass
        except:
            wsgi_util.put_exception("Auth cookie")

    if carry.query:
        print("idx carry.query", carry.query)
        #print("keys", carry.query.keys())
        if "db" in carry.query.keys():
            mydbx = carry.query["db"][0].strip('"')
            # Check if DB is there
            fname = wsgi_data.soft_dbfile(mydbx)
            #print("File:", "'" + fname + "'")
            if os.path.isfile(fname):
                #print("File OK", fname)
                carry.mydb = mydbx
        if "logout" in carry.query.keys():
            print("logout", carry.mainclass.good_cookies)
            delcookie = []
            for aa in  carry.mainclass.good_cookies:
                if aa[0] != "Auth":
                    delcookie.append(aa)
            carry.mainclass.good_cookies = delcookie
            print("logout", carry.mainclass.good_cookies)

    #print("op on", carry.mydb)

    if carry.request:
        #print("idx carry.request", carry.request[:24])
        rq = [] ; par = []
        for aa in carry.request:
            if aa[0] != "db":
                rq.append(aa[1])
                par.append(aa[0])
            else:
                # Set the data base
                mydbx = aa[1].strip('"')
                # Check if DB is there
                fname = wsgi_data.soft_dbfile(mydbx)
                #print("File:", "'" + fname + "'")
                if os.path.isfile(fname):
                    #print("File OK", fname)
                    carry.mydb = mydbx

        #print("data rq", rq)
        if len(rq) == 1:
            if "Confirm" in rq[0]:
                sss = par[0].split("_")
                #print("rq del id: ", sss[1]);
                db = wsgi_data.soft_opendb(carry, carry.mydb)
                db.delrecall(sss[1])
        else:
            try:
                #startt = time.perf_counter()
                #wsgi_data.load_data_func("load_data proj-edit", carry)
                #var = getattr(carry, "proj-edit")
                #print("res", var.res)

                db = wsgi_data.soft_opendb(carry, carry.mydb)
                rrr = ""
                try:
                    # Add filename field from old data (if empty)
                    if not rq[5]:
                        old_rec = db.getbyord(rq[6])
                        if old_rec:
                            #print("old_rec", old_rec)
                            rrr = old_rec[5]
                    else:
                        rrr = rq[5]
                except:
                    wsgi_util.put_exception("padding field")

                #print("Saving", rq[1])
                db.put(rq[0], rq[1], rq[2], rq[3], rq[4], rrr)
                wsgi_data.soft_closedb(db)

                # Measure time needed
                #print("database op %f msec " %  ((time.perf_counter() - startt) * 1000))
            except:
                #print("Cannot put data")
                wsgi_util.put_exception("in put index data")

    carry.local_table = common.local_table

    #if not carry.query and not carry.request:
    # Present default
    #print("<center>Editor has no task to do in: '%s'" % carry.url)

    wsgi_data.load_data_func("load_data " + carry.mydb, carry)

    var = getattr(carry, carry.mydb)
    #for aa in var.res:
    #    print("res", aa[2], " - ", aa[4][:24] + "...")

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
