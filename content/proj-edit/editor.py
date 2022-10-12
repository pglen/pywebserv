 #!/usr/bin/env python3

import sys
import  wsgi_util, wsgi_func, wsgi_global, wsgi_data

from . import common

'''
    Data Editor
'''

def got_editor(config, carry):

    if config.verbose:
        print("got_index() url = '%s'" % carry.url)

    if config.pgdebug > 1:
        print("got_index()", "url:", url, "query:", query)

    if config.pgdebug > 2:
        print(wsgi_conf.config.showvals())

    if config.pgdebug > 3:
        print("got_index() url=%s"% carry.url, "query=%s" % carry.query,
                    "request=%s" % carry.request,
                         "template=%s" % carry.template, "fname=%s" % carry.fname)
    if carry.request:
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

    carry.local_table = common.local_table
    content = wsgi_util.process_default(config, carry)
    return content


def one_center(strx, context):
    content = "<td width=70% align=center valign=top> <p><p>Center Col <p> <p>"
    return content

try:
    wsgi_util.add_locals(locals().copy(), common.local_table)
    wsgi_util.add_local_func("one_center", one_center, common.local_table)

except:
    #print("Exception on editor init vars", sys.exc_info())
    wsgi_util.put_exception("in Editor")
    raise

