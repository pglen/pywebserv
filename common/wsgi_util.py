#!/usr/bin/env python3

''' The simplest web server, utilities module. This is where we parse the
    incoming (loaded) files for macros. The substitution occures in steps
    recursively.
'''

import sys, os, time, re, traceback, datetime, base64
import wsgi_global, wsgi_parse, wsgi_crypt

#try:
#    import wsgi_global, wsgi_parse
#except:
#    print("Cannot import", sys.exc_info())

verbose = 0

def xint(val):

    ''' Safe alternative to int() -- returns 0 if invalid number '''

    try:
        ret = int(val)
    except:
        if verbose > 1:
            print("Invalid number in parsing int", val)
        ret = 0
    return ret

# ------------------------------------------------------------------------

def  resolve_template(config, fn, name):

    # Iterate 'lookfor' combos; the html template can be local, html static,

    #print("resolve_template()", config.mypath, fn, name)

    fname = os.path.basename(name)
    fname2 = os.path.splitext(fname)[0] + ".html"
    #print("respath", os.path.dirname(name) + os.sep + fname2)

    found = ""
    while True:
        fn1 =  os.path.dirname(name) + os.sep + fname2
        #print("test fn1", fn1)
        if  os.path.isfile(fn1):
            found = fn1
            break
        fn2 = config.mypath + os.sep + "html"  + fn
        #print("test fn2", fn2)
        if  os.path.isfile(fn2):
            found = fn2
            break
        fn3 = config.mypath + os.sep + "html" + fn + ".html"
        #print("test fn3", fn3)
        if  os.path.isfile(fn3):
            found = fn3
            break
        break;

    #print("resolve_template(), found: ", found)

    return found

# ------------------------------------------------------------------------
# Utils below

def put_exception(xstr):

    ''' Give some indication of exceptions
    in the html output stream and the controlling terminal
    '''

    cumm = xstr + " "
    a,b,c = sys.exc_info()
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt:
                # do not print sys
                if "importlib" not in aa[0]:
                    cumm += "File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print( "Could not print trace stack. ", cumm, sys.exc_info())

    print(cumm)
    #syslog.syslog("%s %s %s" % (xstr, a, b))

# These are ENV items we want to skip for our display

nogo = ("OPENHAB", "XDG_", "LS_", "SHELL", "SESSION", "QT",
             "LESS", "SSH", "GTK", "SHLVL", "XAUTH", "PANEL", "PATH", "DISPLAY",
                "MANDAT", "WINDOW", "TERM", "GDM", "VIRT", "HUB", "VTE")

def printobj(theobj):
    print("Class", str(theobj.__class__) )
    for aa in dir(theobj):
        if aa[:2] != "__":
            ooo = getattr(theobj, aa)
            if "method" not in str(type(ooo)):
                print(aa, "=", ooo)

def printenv(environ, all=False):
    print("-----------------")
    for aa in environ.keys():
        #print("aa", aa)
        fff = True
        for cc in nogo:
            if cc in aa:
                fff = False
        if fff or all:
            print(aa, "=", environ[aa])

        #if "HTTP_" in aa:
        #    print(aa, environ[aa])
    #print("-----------------")
    print()

def getwenv(environ, all=False):
    ret = ""
    for aa in environ.keys():
        #print("aa", aa)
        fff = True
        for cc in nogo:
            if cc in aa:
                fff = False
        if fff or all:
            ret += aa + " " + str(environ[aa]) + "<br>"

        #if "HTTP_" in aa:
        #    print(aa, environ[aa])
    ret += "\n"
    return ret;

def gethttpenv(environ, all=False):
    cnt = 0; ret = "<table>"

    for aa in environ.keys():
        if not "HTTP_" in aa[:5] and \
                not "CONTENT_" in aa[:8] and \
                        not "QUERY_" in aa[:5]:
            continue
        #print("aa", aa)
        fff = True
        for cc in nogo:
            if cc in aa:
                fff = False
        if fff or all:
            if cnt % 2 == 0:
                ret += "<tr>"
            ret += "<td>" + aa + " " + str(environ[aa]) + "<br>"
        cnt+= 1
    ret += "\n"
    ret += "</table>"
    return ret;

def print_httpenv(environ):
    for aa in environ.keys():
        if "HTTP_" in aa[:5]:
            print(aa, "'" + environ[aa] + "'")
    print(" --- end env")

def append_file(strx):

    weblog = "./data/weblog.txt"
    fp = open(weblog, "a")

    if not fp:
        print("Cannot open log %s" % weblog, os.getcwd())
        return

    fp.write(strx)
    fp.close()

# ------------------------------------------------------------------------
# Resolve paths, read file, expand template

def process_default(configx, carryon):

    #print("using template", context.template, "fname", context.fname)

    if configx.verbose > 3:
        print("process_default() with local_table len ", len(carryon.local_table))

    if configx.pgdebug > 5:
        if carryon.local_table:
            dump_table("Local Table:", carryon.local_table)
            #dump_table_funcs("Local Table Functs:", carryon.local_table)
            pass

    try:
        if not carryon.template:
            template = resolve_template(carryon.config, carryon.url, carryon.fname)
        else:
            template = os.path.dirname(carryon.fname) + os.sep + carryon.template
    except:
        put_exception("Cannot create / open template");

    if configx.verbose > 3:
        print("using template", template)

    if template and os.path.isfile(template):
        buff = ""
        try:
            with open(template, 'r') as fh:
                buff = fh.read()
        except:
            print("Cannot read template", sys.exc_info())

        # Recursively process
        content = wsgi_parse.recursive_parse(buff, carryon, carryon.local_table)
    else:
        content = "Index file (dyn) " + carryon.url + " " +  \
                        carryon.template + " " + str(carryon.query) + " "

    return content


def dump_local_table(tabx):
    ''' Dump named internal table '''

    print("Local Table:")
    for aa in tabx:
        print (wsgi_str.strpad(aa[0]) + " = ", wsgi_str.strunesc(str(aa[1])[:36]), end="\n")
    print("Local Table End")

#def dump_table_funcs(strx, tabx):
#    ''' Dump named internal table functions '''
#    print (strx)
#    for aa in tabx:
#        if type(aa[1]) == type(dump_table_funcs):
#            print ("'" + aa[0] + "' = ", str(aa[1]) + "'")
#    print()


def add_locals(locs, local_table):

    #print("locs", locs)
    for aa in locs:
        if "_mac_" in aa[:5]:
            #if Config.verbose:
            #    print("Added:", aa[5:]) #, locs[aa][:12])

            add_local_func(aa[5:], locs[aa], local_table)

    #print("Local table: len=%d", len(local_table))
    #for aa in local_table:
    #    print(" '" + aa[0] + "'", end = " ")
    #print ("\ntable end")

# ------------------------------------------------------------------------
# Add a new project function;

def add_local_func(mname, mfunc, table):

    '''
         Add a macro function or string here. The macro is substituted
        by the output of the function.
    '''

    #print("local_func:", mname)

    try:
        #see if there is an entry already
        for aa in table:
            if aa[0] == mname:
                #print("Duplicate function/macro", mname, mfunc)
                return True
        table.append([mname, mfunc])
    except:
        print("Cannot add local table item", sys.exc_info())
    return False

def _check_type(locvars, aa):
    ''' See if it is str and func '''
    if type(locvars[aa]) == type(""):
        #print("Global str:", "'" + aa[6:] + "' = " , locvars[aa][:12].replace("\n", "\\n") )
        pass
    elif type(locvars[aa]) == type(add_local_vars):
        #print("Global func:", "'" + aa[6:] + "' = " , locvars[aa])
        pass
    else:
        print("Invalid type definition", "'" + aa + "'")
        return True

# ------------------------------------------------------------------------
# Scan for _func_ in the name

def add_local_funcs(locvars, table):

    try:
        for aa in locvars:
            #print("Adding local func", aa, type(locvars[aa]))
            if type(locvars[aa]) == type(add_local_funcs):
                # Do not add hidden
                if "_func_" == aa[:6]:
                    #print("Adding local func2", aa)
                    add_local_func(aa[6:],  locvars[aa], table)

    except:
        print("Exception on add_local_funcs", sys.exc_info())
        put_exception("loc func")

# ------------------------------------------------------------------------
# Scan for _func_ in the name

def add_global_funcs(locvars, table):

    try:
        for aa in locvars:
            #print("Adding local func", aa, type(locvars[aa]))
            if type(locvars[aa]) == type(add_local_funcs):
                # Do not add hidden
                if "_gfunc_" == aa[:7]:
                    #print("Adding global func2", aa)
                    wsgi_global.gl_table.add_one_func(aa[7:], locvars[aa])

    except:
        print("Exception on add_global_funcs", sys.exc_info())
        put_exception("glob func")


def add_local_vars(locvars, table):

    '''
         Add all local varables here. A copy of the vars is received
         for non changing array
         Scan for _mac_ in the name

    '''

    try:
        for aa in locvars:
            # These become locals
            if "_mac_" in aa[:5]:
                if _check_type(locvars, aa):
                    continue
                #print("Adding:", "'" + aa[5:] + "' = " , locvars[aa][:12].replace("\n", "\\n") )
                add_local_func(aa[5:],  locvars[aa], table)
    except:
        print("Exception on add_local_vars", sys.exc_info())
        put_exception("loc")


def add_global_vars(locvars, table):

    '''
         Add all global varables here. A copy of the vars is received
         for non changing array
         Scan for _glob_ in the name
'''

    try:
        for aa in locvars:
            # These become globals (site wide)
            if "_glob_" in aa[:6]:
                if _check_type(locvars, aa):
                    continue
                wsgi_global.gl_table.add_one_func(aa[6:], locvars[aa])
    except:
        print("Exception on add_local_vars", sys.exc_info())
        put_exception("loc")

def dump_global_table():

    print("Global Table:")
    wsgi_global.gl_table.dump_table()
    print("Global Table End")

# ------------------------------------------------------------------------
# This is a collection of all automatic var adds

def add_all_vars(locvars, table):

    # This adds local the variables pre - marked for a purpose
    add_local_vars(locvars, table)
    add_local_funcs(locvars, table)

    # This adds global the variables pre - marked for a purpose
    add_global_vars(locvars, table)
    add_global_funcs(locvars, table)

# ------------------------------------------------------------------------

def hash32(strx):

    ''' Deliver a 32 bit hash of the passed entity '''

    #print("hashing", strx)
    lenx = len(strx);  hashx = int(0)
    for aa in strx:
        aaa = ord(aa)
        hashx +=  int( (aaa << 12) + aaa)
        hashx &= 0xffffffff
        hashx = int(hashx << 8) + int(hashx >> 8)
        hashx &= 0xffffffff
    return hashx

def decode_cookie_header(name, value):

    ''' Decode the encrypted cookie, verify '''
    name = name.strip()
    value = value.strip("; ")
    # Test damage
    #value = "a" + value

    try:
        #print("decode_cookie_header", name, value)
        ddd     = base64.b64decode(value.encode())
    except:
         #put_exception("exception on decode_cookie_header")
         return name + "-Damaged", "Damaged Cookie"

    #print("after base", ddd)
    deco    = wsgi_crypt.xdecrypt(ddd, "1234")
    #print("deco", deco)
    sss = deco.split(b"+", 1)
    try:
        hhh = "%08x" % hash32(sss[0].decode())
        hhh = hhh.encode()
    except:
        # No hash arrived, add fake values to trigger damage control
        hhh = "0"
        sss = ("No Value", "No value")
        pass
    # Hash checks out?
    if sss[0] !=  hhh:
        #print("Damaged cookie", sss, hhh)
        deco = b"Damaged Cookie"
    return name, sss[1].decode()

def set_cookie_header(name, value, minutes=60):

    dt = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
    fdt = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')
    secs = minutes * 60
    vvv = "%08x" % hash32(value) + "+" + str(value)
    vvvv = vvv.encode()
    #print("vvvv", vvvv)
    org2    = wsgi_crypt.xencrypt(vvvv, "1234")
    enco        = base64.b64encode(org2).decode()
    #print("enco", enco)
    ccc = 'Set-Cookie', '{}={}; Expires={}; Max-Age={}; SameSite=Strict; Path=/' \
                                            .format(name, enco, fdt, secs)
    #print("cookie", ccc)
    return ccc

# EOF
