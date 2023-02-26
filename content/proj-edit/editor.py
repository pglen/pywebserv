 #!/usr/bin/env python3

import sys
import  wsgi_util, wsgi_func, wsgi_global, wsgi_data, wsgi_str

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

    content = "";  carry.cdata   = ""

    if config.verbose:
        print("got_index() url = '%s'" % carry.url)

    if config.pgdebug > 1:
        print("got_index()", "url:", carry.url, "query:", carry.query,
                 "request", carry.request)

    if config.pgdebug > 2:
        print(wsgi_conf.config.showvals())

    if config.pgdebug > 3:
        print("got_index() url=%s"% carry.url, "query=%s" % carry.query,
                    "request=%s" % carry.request,
                         "template=%s" % carry.template, "fname=%s" % carry.fname)
    if carry.request:
        #print("carry.request", carry.request)
        wsgi_data.soft_opendb(carry, modname)
        #print("db", carry.localdb)

        if carry.request[0][1] == "Edit":
            rq = carry.request[0][0].split("_")
            print("rq edit data:", rq)

            carry.xdata = []; carry.hdata = []
            #macros.fill_data(carry, carry.localdb, rq[1])
            res = carry.localdb.getbyord(rq[1])
            print("res:", res)
            if not res:
                #delete(carry.localdb)
                print("Cannot load data", rq[1], carry.localdb)
                content += "Cannot load data for record: " + str(rq[1])
                return content
            carry.cdata += "<table border=0>"
            #fnames = ("key", "arg 1", "arg 2","arg 3","arg 4", "arg 5")
            carry.cdata += "Key: '" +  str(res[0]) + "'<p>"
            carry.cdata += "<input type=hidden name=key value=%s" % (str(res[0])) + ">"

            for aa in range(len(res)-1):
                carry.cdata += \
                    "<tr><td> " + "arg %d" % (aa) + " <td> : &nbsp;  " + \
                        "<td><textarea cols=64 rows=4 name='aa_%d'" % (aa) + ">" + \
                            str(res[aa+1]) + "</textarea><p>"
            carry.cdata += "</table>"

        elif carry.request[0][1] == "Add New":
            #print ("adding new data")
            carry.cdata += "<table border=0>"
            carry.cdata += "<tr><td>key   <td> : &nbsp;  <td><textarea cols=48 rows=4 name=aa1>"  + "</textarea><p>"
            carry.cdata += "<tr><td>arg 1 <td> : &nbsp;  <td><textarea cols=48 rows=4 name=aa2>"  + "</textarea><p>"
            carry.cdata += "<tr><td>arg 2 <td> : &nbsp;  <td><textarea cols=48 rows=4 name=aa3>"  + "</textarea><p>"
            carry.cdata += "<tr><td>arg 3 <td> : &nbsp;  <td><textarea cols=48 rows=4 name=aa4>"  + "</textarea><p>"
            carry.cdata += "<tr><td>arg 4 <td> : &nbsp;  <td><textarea cols=48 rows=4 name=aa5>"  + "</textarea><p>"
            carry.cdata += "</table>"

        elif "Del" in carry.request[0][1]:
            rq = carry.request[0][0].split("_")
            print("rq delete data", rq[1])
        else:
            print("Invalid (unimplemented) command code")

    wsgi_data.soft_closedb(carry, modname)

    carry.local_table = common.local_table

    content += wsgi_util.process_default(config, carry)
    #print("content", content)

    return content

def one_center(strx, context):

    #print("context", context)
    #print(context.getvals())

    content = "<form action=index.html method=post >"
    content += "<td width=70% align=center valign=top><p><p>"

    if context.request[0][1] == "Edit":
        content += "Editing Record Num: %d" % int(context.request[0][0][3:])
    elif context.request[0][1] == "Add New":
        content += "New Record "
    elif "Del" in context.request[0][1]:
        content += "Delete"
    else:
        content += "Invalid context"

    content += "<p> " + context.cdata  + "<p>"

    if context.request[0][1] == "Edit" or \
            context.request[0][1] == "Add New":
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
