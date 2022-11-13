 #!/usr/bin/env python3

import sys
import  wsgi_util, wsgi_func, wsgi_global, wsgi_data

'''
    Local macros and data. Register it after init or use the "_mac_ prefix to auto register
'''

from . import common

ppp = __file__.split('/')
plen = len(ppp)
modname = ppp[plen-2] + "-" + ppp[plen-1]
projname = ppp[plen-2]

# ------------------------------------------------------------------------

def  proj(strx, context):
    pass
    print("filling in projname", projname)
    return projname

try:
    wsgi_util.add_locals(locals().copy(), common.local_table)
    wsgi_util.add_local_func("proj", proj, common.local_table)

except:
    #print("Exception on editor init vars", sys.exc_info())
    wsgi_util.put_exception("in resp")
    raise

