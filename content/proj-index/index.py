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

    if not template:
        template = wsgi_util.resolve_template(config, url, __file__)
    else:
        template = os.path.dirname(__file__) + os.sep + template

    #print("using template", template)

    if template and os.path.exists(template):
        buff = ""
        #content = "Index file exists " + url + " " +  str(query) + " "
        try:
            with open(template, 'r') as fh:
                buff = fh.read()
        except:
            print("reason", sys.exc_info())

        # Recursively process
        content = wsgi_util.recursive_parse(buff, __file__)
    else:
        content = "Index file (dyn) " + url + " " +  template + " " + str(query) + " "
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


# Upon loading ...

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

def mac_func_one(strx, context):
    return strx + " Function body here " + str(context)

mac_header2 = '''
<form method=post>
    <table width=100% border=0>
        <tr><td>
        <a href=index.html>
        <font size=+2><b>Welcome to UPP, </a> </font> United Planet Peace
        <!-- (under construction, check back later) --!>

        <td align=right>
            Quick feedback:  &nbsp;
            <input type=text name="hell" value="Feed back Title">
            <input type=text name="textx" value="Feedback Content">
            <input type=submit name='hello' value='Submit'>
        <td>
        </table>
</form>
'''

modname = os.path.splitext(os.path.basename(__file__))[0]

try:
    #print("Initializing", "'" + modname + "'" )
    # Add default enties to table
    wsgi_global.add_one_url("/", got_index, "index.html", __file__)
    wsgi_global.add_one_url("/index.html", got_index, "index.html", __file__)
    wsgi_global.add_one_func("feed_data", fill_data)
    wsgi_global.add_one_func("Company Name", "UPP")
    wsgi_global.add_one_func("sitestyle", sitestyle)

except:
    print("Cannot initialize", modname, sys.exc_info())
    wsgi_util.put_exception("initialize error")

initialize()

# Auto add macro entries

try:
    vvv = vars().copy()
    for name in vvv:
        if type(name) == type('a') or type(name) == type(initialize):
            if "mac_" == name[:4]:
                print("Adding", name, type(name))
                wsgi_global.add_one_func(name, vvv[name])

except:
    print("Exception on init vars", sys.exc_info())

# EOF