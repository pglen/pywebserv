#!/usr/bin/env python3

'''
    This is a sample project that is added to the site. The idea here is
    that nothing in this project can syntax error (down) the site.
    It is imported under a try: except clause, and it is calling only the
    URL registration functions.
    Also, included a default web page function as index.html or as '/'
'''

import os, sys, time

import wsgi_util, wsgi_func, wsgi_data, wsgi_global

try:
    import macros
except:
    print("Cannot import macros", sys.exc_info())
    wsgi_util.put_exception("import macros")

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

    if config.conf.pgdebug > 3:
        print("got_index() url=%s"% url, "query=%s" %query,
                    "request=%s" % request, "template=%s" % template, "fname=%s" % fname)

    if config.conf.verbose:
        print("got_index() url = '%s'" % url, "request_org=", config.mainclass.request_org)

    #print("got_index() request", request)
    #print("got_index() config", config.showvals(), url, query)

    if url == "/":
        url = "/index.html"

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

    content = wsgi_util.process_default(config, url, query, request, template, fname)
    return content


def got_log(config, url, query, request, template = "", fname = ""):
    content = wsgi_util.process_default(config, url, query, request, template, fname)
    return content


# ------------------------------------------------------------------------
# Add all the functions for the urls;
# This function is called when the module is loaded
#

def initialize():

    '''
    Initializee the current module
    '''

    global localdb
    #print("Called  initialization for '%s'" % modname)
    if not localdb:
        try:
            localdb = wsgi_data.wsgiSql("data/%s_data.sqlt" % modname)
        except:
            print("Could not create local data for %s", modname)


# Upon loading ... add macros

sitestyle = '''
<style>
.container {
  position: relative;
  width: 50%;
}
.image {
  opacity: 1;
  display: inline;
  height: auto;
  transition: .5s ease;
  backface-visibility: hidden;
}
.container {
  position: relative;
  width: 50%;
}
.container:hover .image {
  opacity: 0.3;
}
.container:hover .middle {
  opacity: 1;
}

a:link, a:visited {
    //color: black;
    text-decoration: none;
    decoration: none;
}

</style>
'''

#mycolor = "#cccccc"

def mac_func_one(strx, context):
    return strx + " Function body here " + str(context)

modname = os.path.splitext(os.path.basename(__file__))[0]

try:
    #print("Initializing", "'" + modname + "'" )
    # Add default enties to table
    wsgi_global.add_one_url("/", got_index, "index.html", __file__)
    wsgi_global.add_one_url("/index.html", got_index, "index.html", __file__)
    wsgi_global.add_one_url("/log.html", got_log, "log.html", __file__)

    wsgi_global.add_one_func("feed_data", fill_data)
    wsgi_global.add_one_func("Company Name", "UPP, United Planet Peace")
    wsgi_global.add_one_func("sitestyle", sitestyle)
    #wsgi_global.add_one_func("mycolor", mycolor)

except:
    print("Cannot initialize", modname, sys.exc_info())
    wsgi_util.put_exception("initialize error")

initialize()

# EOF