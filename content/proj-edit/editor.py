 #!/usr/bin/env python3

import sys, uuid
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
    if carry.query:
        print("editor carry.query", carry.query)

    if carry.request:
        print("editor carry.request", carry.request)
        wsgi_data.soft_opendb(carry, modname)
        #print("db", carry.localdb)

        if carry.request[0][1] == "Edit":
            carry.xdata = []; carry.hdata = []
            rq = carry.request[0][0].split("_")
            #print("rq edit data:", rq)
            res = carry.localdb.getbyord(rq[1])
            #print("res:", res)

            carry.cdata += "<font size=+2>Key: '" +  str(res[0]) + "'</font><p>"
            carry.cdata += "Editing Record Num: %d<p>" % int(carry.request[0][0][3:])

            #macros.fill_data(carry, carry.localdb, rq[1])
            if not res:
                #delete(carry.localdb)
                print("Cannot load data", rq[1], carry.localdb)
                content += "Cannot load data for record: " + str(rq[1])
                return content
            carry.cdata += "<table border=0>"
            #fnames = ("key", "arg 1", "arg 2","arg 3","arg 4", "arg 5")
            carry.cdata += "<input type=hidden name=key value=%s" % (str(res[0])) + ">"

            for aa in range(len(res)-1):
                if aa == len(res)-2:
                    carry.cdata += \
                    "<tr><td> " + "arg %d" % (aa) + " <td> : &nbsp;  " + \
                        "<td><textarea readonly cols=64 rows=4 name='aa_%d'" % (aa) + ">" + \
                            str(res[aa+1]) + "</textarea><p>"
                else:
                    carry.cdata += \
                    "<tr><td> " + "arg %d" % (aa) + " <td> : &nbsp;  " + \
                        "<td><textarea cols=64 rows=4 name='aa_%d'" % (aa) + ">" + \
                            str(res[aa+1]) + "</textarea><p>"

            carry.cdata += "</table>"
            carry.cdata += "<br><input type=submit value=' Save Record '>"

        elif carry.request[0][1] == "Add New":
            #print ("adding new data")
            uuidx = str(uuid.uuid4())
            carry.cdata += "<font size=+2><b>New Record</b></font>"
            carry.cdata += "<table border=0>"
            carry.cdata += "<tr><td>key : <td>&nbsp; <td>%s" % uuidx

            # Name the text areas in ascending order, so the ...
            #  order is kept when saving; also the file field too;

            carry.cdata += "<tr><td><td><textarea hidden cols=48 rows=1 name=aa1>"
            carry.cdata += uuidx
            carry.cdata +=  "</textarea><p>"

            carry.cdata += "<tr><td>Title: <td> &nbsp;  <td><textarea cols=48 rows=4 name=aa2>"  + "</textarea><p>"
            carry.cdata += "<tr><td>Sidebar: <td> &nbsp;  <td><textarea cols=48 rows=4 name=aa3>"  + "</textarea><p>"
            carry.cdata += "<tr><td>Main Text: <td> &nbsp;  <td><textarea cols=48 rows=4 name=aa4>"  + "</textarea><p>"
            carry.cdata += "<tr><td>Bottom Text: <td> &nbsp;  <td><textarea cols=48 rows=4 name=aa5>"  + "</textarea><p>"
            carry.cdata += "<tr><td>Upload Image:<td> &nbsp; <td align=right>"
            carry.cdata += "<input type=file id=myFile name=aa6, accept:'image/png, image/jpeg'>"
            carry.cdata += "</table>"
            carry.cdata += "<br><input type=submit value=' Create Record '>"

        elif "Del" in carry.request[0][1]:
            carry.cdata += "<font size=+2><b>Delete Operation</b></font><p>"

            rq = carry.request[0][0].split("_")
            #print("rq delete data %d " % (int(rq[1])))
            res = carry.localdb.getbyord(rq[1])

            carry.cdata += "<table border=0>"
            carry.cdata += "<tr><td align=center>" + \
                            "Request to delete record %d <p>'%s'<p>" % \
                                (int(rq[1]), res[1])

            carry.cdata += "</table>"

            carry.cdata += "<input type=submit name=rm_%d value='  Cancel Delete  '>  &nbsp; " % int(rq[1])
            carry.cdata += "<input type=submit name=rm_%d value='  Confirm Delete  '>  "  % int(rq[1])

            #content +=

        else:
            content += "<b>invalid opcode</b>"
            print("Invalid (unimplemented) command code")

    wsgi_data.soft_closedb(carry, modname)

    carry.local_table = common.local_table

    content += wsgi_util.process_default(config, carry)
    #print("content", content)

    return content

def one_center(strx, context):

    #print("context", context)
    content = "<form action=index.html method=post enctype=multipart/form-data>"
    content += "<td width=70% align=center valign=top><p><p>"
    content += "<p> " + context.cdata  + "<p>"
    content += "</form >"
    return content

try:
    wsgi_util.add_locals(locals().copy(), common.local_table)
    wsgi_util.add_local_func("one_center", one_center, common.local_table)

except:
    #print("Exception on editor init vars", sys.exc_info())
    wsgi_util.put_exception("in Editor")
    raise
