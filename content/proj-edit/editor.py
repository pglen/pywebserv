#!/usr/bin/env python3

import sys, uuid, os
import  wsgi_util, wsgi_func, wsgi_global, wsgi_data, wsgi_str

from . import common
from . import macros

ppp = __file__.split('/')
modname = ppp[-2]
#print("modname", modname)

'''
    Data Editor; list of data
'''

field_names = ("Title:", "Sidebar:","Main Text:","Bottom Text:", "Image File:")

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

    if not carry.query and not carry.request:
        carry.cdata += "<table border=0 width=100%>"
        carry.cdata += "<tr><td><center>Editor has no task to do in: '%s'" % carry.url
        carry.cdata += "</table>"
        carry.local_table = common.local_table
        sss = wsgi_util.process_default(config, carry)
        return sss

    if carry.query:
        print("editor carry.query", carry.query)

    #carry.mydb = modname
    carry.mydb = "proj-rows"
    opcode = ""; opnum = 0

    if carry.request:
        print("editor carry.request", carry.request)

        for aa in carry.request:
            if "db" == aa[0]:
                mydbx = aa[1].strip('"')
                # Check if DB is there
                fname = wsgi_data.soft_dbfile(mydbx)
                #print("File:", "'" + fname + "'")
                if os.path.isfile(fname):
                    print("File OK", fname)
                    carry.mydb = mydbx
            if "logout" == aa[0]:
                #print("logout button")
                opcode = "logout"
            if "exp" == aa[0]:
                print("export button")
                opcode = "export"

        #print("op on", mydb)

        db = wsgi_data.soft_opendb(carry, carry.mydb)
        #print("db", db)

        carry.cdata += "<table border=0 width=100%>"

        for aa in  carry.request:
            #print("aa", aa)
            if "add" in aa[0]:
                opcode = aa[1]
            elif aa[0][:3] == "ed_" or aa[0][:4] == "del_":
                opcode = aa[1]
                rq = aa[0].split("_")
                if len(rq) > 1:
                    opnum = int(rq[1])

        #print ("opcode", opcode, "opnum", opnum)

        if opcode == "Edit":
            carry.xdata = []; carry.hdata = []
            #print("rq edit data:", rq)
            res = db.getbyord(opnum)
            #print("res:", res)

            carry.cdata += "<input type=hidden name=db value=%s" % carry.mydb + ">"

            carry.cdata += "<tr><td>Key:  "
            carry.cdata += "<td><font size=+1>"  +  res[0].decode() + "</font>"
            carry.cdata += "<tr><td>Record: "
            carry.cdata += "<td> %d" % int(opnum)

            #macros.fill_data(carry, carry.localdb, rq[1])
            if not res:
                #delete(carry.localdb)
                print("Cannot load data", rq[1], carry.localdb)
                content += "Cannot load data for record: " + str(rq[1])
                return content

            #print("res", res)

            carry.cdata += "<input type=hidden name=aa_0 value=%s" % res[0].decode() + ">"
            carry.cdata += "<input type=hidden name=aa_6 value=%s" % rq[1] + ">"

            for aa in range(len(res)-1):
                if aa == len(res)-2:
                    carry.cdata +=  "<tr><td><td align=center>"
                    carry.cdata +=  \
                     "Add if image replacement is intended, else old image preserved.<p>"
                    carry.cdata += \
                     "<input type=file id=myFile name=aa_5, accept:'image/png, image/jpeg'>"
                elif aa == len(res)-4:
                    carry.cdata += \
                    "<tr><td> " + "%s" % (field_names[aa]) + "  " + \
                        "<td><textarea cols=64 rows=8 name='aa_%d'" % (aa+1) + ">" + \
                            str(res[aa+1]) + "</textarea>"
                else:
                    carry.cdata += \
                    "<tr><td> " + "%s" % (field_names[aa]) + "  " + \
                        "<td><textarea cols=64 rows=4 name='aa_%d'" % (aa+1) + ">" + \
                            str(res[aa+1]) + "</textarea>"

            carry.cdata += "</table>"
            carry.cdata += "<center><input type=submit value=' Save Record '>"

        elif opcode == "Add New":
            #print ("adding new data")
            uuidx = str(uuid.uuid4())
            carry.cdata += "<table border=0 width=100%>"
            carry.cdata += "<tr><td align=center colspan=2>"
            carry.cdata += "<font size=+2><b>New Record</b></font>"
            carry.cdata += "<tr><td align=center colspan=2>"
            carry.cdata += "<tr><td>Key:<td>%s" % uuidx

            # Name the text areas in ascending order, so the ...
            #  order is kept when saving; also the file field too;

            carry.cdata += "<input type=hidden name=db value=%s" % carry.mydb + ">"

            carry.cdata += "<tr><td><textarea hidden cols=48 rows=1 name=aa_1>"
            carry.cdata += uuidx
            carry.cdata +=  "</textarea><p>"

            carry.cdata += "<tr><td>" + field_names[0] + " <td><textarea cols=60 rows=4 name=aa_2>"  + "</textarea><p>"
            carry.cdata += "<tr><td>" + field_names[1] + " <td><textarea cols=60 rows=4 name=aa_3>"  + "</textarea><p>"
            carry.cdata += "<tr><td>" + field_names[2] + " <td><textarea cols=60 rows=4 name=aa_4>"  + "</textarea><p>"
            carry.cdata += "<tr><td>" + field_names[3] + " <td><textarea cols=60 rows=4 name=aa_5>"  + "</textarea><p>"
            carry.cdata += "<tr><td> Upload Image:<td align=right>"
            carry.cdata += "Select for new image submission <input type=file id=myFile name=aa_6, accept:'image/png, image/jpeg'>"
            carry.cdata += "<tr><td align=center colspan=2>"
            carry.cdata += "</table>"
            carry.cdata += "<center><input type=submit value=' Create Record '>"

        elif "Del" in opcode:
            carry.cdata += "<tr><td align=center><font size=+2><b>Delete Operation</b></font><p>"

            #rq = carry.request[0][0].split("_")
            #print("rq delete data %d " % (int(rq[1])))

            carry.cdata += "<input type=hidden name=db value=%s" % carry.mydb + ">"

            db = wsgi_data.soft_opendb(carry, carry.mydb)
            res = db.getbyord(opnum)
            if not res:
                res = ("", "")

            carry.cdata += "<tr><td align=center>" + \
                            "Request to delete record %d <p>'%s'<p>" % \
                                (opnum, res[1])

            carry.cdata += "<input type=submit name=rm_%d value='  Cancel Delete  '>  &nbsp; " % int(rq[1])
            carry.cdata += "<input type=submit name=rm_%d value='  Confirm Delete  '>  "  % int(rq[1])

        elif "logout" == opcode:
            carry.cdata += "<table border=0 width=100%>"
            carry.cdata += "<tr><td align=center colspan=2>"
            carry.cdata += "<font size=+2>Logged Out</font><p>"
            carry.cdata += "<a href=index.html> Back to Login</a>"
            carry.cdata += "</table>"
            carry.needpass = True
            carry.mainclass.wanted_cookies.append(("Auth", "", 1))

        elif "export" == opcode:
            carry.cdata += "<table border=0 width=100%>"
            carry.cdata += "<tr><td align=center colspan=2>"
            carry.cdata += "<font size=+2>Exporting</font><p>"
            carry.cdata += "<a href=index.html> Back to Login</a>"
            carry.cdata += "</table>"

        else:
            carry.cdata += "<table width=100%>"
            carry.cdata += "<tr><td align=center><font size=+2>" + \
                            "Invalid / Unimplemented opcode '%s'</font><p> db='%s'</b>" % \
                                     (opcode, carry.request[0][1])
            print("Invalid (unimplemented) command code")
            carry.cdata += "</table>"

    #wsgi_data.soft_closedb(carry, carry.mydb)
    carry.cdata += "</table>"

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
