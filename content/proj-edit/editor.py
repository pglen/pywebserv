 #!/usr/bin/env python3

import sys
import  wsgi_util, wsgi_func, wsgi_global, wsgi_data

from . import common
from . import macros

ppp = __file__.split('/')
modname = ppp[-2]
#print("modname", modname)

'''
    Data Editor; list of data
'''

def got_editor(config, carry):

    #wsgi_util.printobj(carry)

    content = ""
    carry.cdata   = ""

    if config.verbose:
        print("got_index() url = '%s'" % carry.url)

    if 1: #config.pgdebug > 1:
        print("got_index()", "url:", carry.url, "query:", carry.query,
                 "request", carry.request)

    if config.pgdebug > 2:
        print(wsgi_conf.config.showvals())

    if config.pgdebug > 3:
        print("got_index() url=%s"% carry.url, "query=%s" % carry.query,
                    "request=%s" % carry.request,
                         "template=%s" % carry.template, "fname=%s" % carry.fname)
    if carry.request:

        print("carry.request", carry.request)

        wsgi_data.soft_opendb(carry, modname)

        if carry.request[0][1] == "Edit":
            rq = carry.request[0][0].split("_")
            print("rq edit data", rq[1])
            #global gl_arr
            #gl_arr = []
            res = macros.fill_data(carry.localdb, 1) #int(rq[1][3:]))
            print("res:", res)
            if res:
                carry.cdata += "<table border=1>"

                for aa in range(len(res)):
                    carry.cdata += \
                        "<tr><td>key   <td> : &nbsp;  " + \
                            "<td><textarea cols=64 rows=4 name='aa_%d' % aa>" + \
                                str(res[aa]) + "</textarea><p>"

                carry.cdata += "</table>"

        if carry.request[0][1] == "Add New":
            #print ("adding new data")
            carry.cdata += "<table border=1>"
            carry.cdata += "<tr><td>key   <td> : &nbsp;  <td><textarea cols=48 rows=4 name=aa1>"  + "</textarea><p>"
            carry.cdata += "<tr><td>arg 1 <td> : &nbsp;  <td><textarea cols=48 rows=4 name=aa2>"  + "</textarea><p>"
            carry.cdata += "<tr><td>arg 2 <td> : &nbsp;  <td><textarea cols=48 rows=4 name=aa3>"  + "</textarea><p>"
            carry.cdata += "<tr><td>arg 3 <td> : &nbsp;  <td><textarea cols=48 rows=4 name=aa4>"  + "</textarea><p>"
            carry.cdata += "<tr><td>arg 4 <td> : &nbsp;  <td><textarea cols=48 rows=4 name=aa5>"  + "</textarea><p>"
            carry.cdata += "</table>"

        if carry.request[0][1] == "Del":
            rq = carry.request[0][0].split("_")
            #print("rq delete data", rq[1])

            #carry.localdb.put("key_" + rq[0], rq[0], rq[1], rq[2], "")

    carry.local_table = common.local_table

    content += wsgi_util.process_default(config, carry)
    #print("content", content)

    return content

def one_center(strx, context):

    #print("context", context)
    print(context.getvals())

    content = "<form action=index.html method=post >"
    content += "<td width=70% align=center valign=top><p><p>"

    if context.request[0][1] == "Edit":
        content += "Record %d" % int(context.request[0][0][3:])
    else:
        content += "New Record "

    content += "<p><p> " + context.cdata  + "<p>"
    content += "<input type=submit value='Save Data'>"
    content += "</form >"
    return content

try:
    wsgi_util.add_locals(locals().copy(), common.local_table)
    wsgi_util.add_local_func("one_center", one_center, common.local_table)

except:
    #print("Exception on editor init vars", sys.exc_info())
    wsgi_util.put_exception("in Editor")
    raise

