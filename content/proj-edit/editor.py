 #!/usr/bin/env python3

import sys
import  wsgi_util, wsgi_func, wsgi_global, wsgi_data

from . import common

'''
    Data Editor
'''

def got_editor(config, url, query, request, template = "", fname = ""):

    #print("Called editor")
    wcontext = wsgi_util.wContext(config, url, query)
    wcontext.request    = request
    wcontext.template   = template
    wcontext.fname      = fname
    wcontext.local_table = common.local_table

    #print(common.local_table)

    content = wsgi_util.process_default2(wcontext)

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

