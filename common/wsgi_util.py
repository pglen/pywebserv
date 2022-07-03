#!/usr/bin/env python3

''' The simplest web server, utilities module. This is where we parse the
    incoming (loaded) files for macros. The substitution occures in steps
    recursively.
'''

import sys, os, time, re, traceback

try:
    import wsgi_global, wsgi_parse
except:
    print("Cannot import", sys.exc_info())
    pass

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
        if  os.path.exists(fn1):
            found = fn1
            break
        fn2 = config.mypath + os.sep + "html"  + fn
        #print("test fn2", fn2)
        if  os.path.exists(fn2):
            found = fn2
            break
        fn3 = config.mypath + os.sep + "html" + fn + ".html"
        #print("test fn3", fn3)
        if  os.path.exists(fn3):
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
                cumm += "File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print( "Could not print trace stack. ", sys.exc_info())

    print(cumm)
    #syslog.syslog("%s %s %s" % (xstr, a, b))

# These are ENV items we want to skip for our display

nogo = ("OPENHAB", "XDG_", "LS_", "SHELL", "SESSION", "QT",
             "LESS", "SSH", "GTK", "SHLVL", "XAUTH", "PANEL", "PATH", "DISPLAY",
                "MANDAT", "WINDOW", "TERM", "GDM", "VIRT", "HUB", "VTE")

def printenv(environ, all=False):
    for aa in environ.keys():
        #print("aa", aa)
        fff = True
        for cc in nogo:
            if cc in aa:
                fff = False
        if fff or all:
            print(aa, environ[aa])

        #if "HTTP_" in aa:
        #    print(aa, environ[aa])
    print()

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


# ------------------------------------------------------------------
# Resolve paths, read file, expand template

def process_default(config, url, query, request, template, fname, local_table):

    print("process_default() local_table: ", local_table[:1], "\n")

    if not template:
        template = wsgi_util.resolve_template(config, url, fname)
    else:
        template = os.path.dirname(fname) + os.sep + template

    #print("using template", template)

    if template and os.path.exists(template):
        buff = ""
        try:
            with open(template, 'r') as fh:
                buff = fh.read()
        except:
            print("Cannot read template", sys.exc_info())

        # Recursively process
        content = wsgi_parse.recursive_parse(buff, fname, local_table)
    else:
        content = "Index file (dyn) " + url + " " +  template + " " + str(query) + " "

    return content


# EOF