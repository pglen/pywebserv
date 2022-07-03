#!/usr/bin/env python3

''' The simplest web server, utilities module. This is where we parse the
    incoming (loaded) files for macros. The substitution occures in steps
    recursively.
'''

import sys, os, time, re, traceback

try:
    import wsgi_global
    import wsgi_util
except:
    print("Cannot import", sys.exc_info())
    pass

# ------------------------------------------------------------------------

def _parse_items(item, context, table):

    # Scan backwards so items can be overridden
    for ii in range(len(table)-1, -1, -1):
        aa = table[ii]
        #print("aa", aa)
        if item[2:-2] == aa[0]:
            if type(aa[1]) == str:
                return aa[1]
            if type(aa[1]) == type(table):
                cccc = ""
                try:
                    cccc = aa[1](item, context)
                except:
                    #print("_local_items", sys.exc_info())
                    pass
                return cccc
    return item

def _global_items(item, context):

    # Scan backwards so items can be overridden
    for ii in range(len(wsgi_global.global_table)-1, -1, -1):
        aa = wsgi_global.global_table[ii]
        #print("aa", aa)
        if item[2:-2] == aa[0]:
            if type(aa[1]) == str:
                return aa[1]
            if type(aa[1]) == type(_global_items):
                cccc = ""
                try:
                    cccc = aa[1](item, context)
                except:
                    print("global_items", sys.exc_info())
                return cccc
    return item

# Parameterized last

def _global_para_items(item, context, table):

    print("item", "'" + item + "'")

    # rescan for parameterized
    for aa in table:
        if item[2:-2].split()[0] == aa[0]:
            if type(aa[1]) == type(_global_para_items):
                cccc = ""
                try:
                    cccc = aa[1](item, context)
                except:
                    #print("para items", sys.exc_info())
                    pass
                return cccc

    erritem = str(item[2:-2])
    if erritem[0] == '#':
        #print("Ignoring commented:", erritem)
        return ""

    # Inject error message
    return "<font color=red>!!" + str(item[2:-2]) + "!!</font>"

# Parse buffer

def _parse_buffer(buff, flag, regex, context, table):

    count = 0 ;     prog = 0
    rrr = re.compile(regex)
    arr = []
    while(True):
        frag = re.search(rrr, buff[prog:])
        if not frag:
            arr.append(buff[prog:])
            break
        #print ("match", frag)
        bbb = prog+frag.start()
        eee = prog+frag.end()
        arr.append(buff[prog:bbb])
        #print("match", buff[bbb:eee])
        if flag:
            conv = _parse_items(buff[bbb:eee], context, table)
        else:
            conv = _global_para_items(buff[bbb:eee], context, table)

        arr.append(conv)
        prog += frag.end()
        count += 1

    #print("parsed", count)
    #print ("arr", arr)
    return arr, count

# ------------------------------------------------------------------------

def _parse_one(buff, context, flag, tablex, regex):

    content = ""

    # Recursively process
    cnt2 = 10; old_cnt = 0
    content = buff
    while(True):
        arr, cnt = _parse_buffer(content, flag, regex, context, tablex)
        content = ""
        for aa in arr:
            content += str(aa)
        #print("recursive", cnt)
        if cnt <= 1:
            break
        if cnt2 <= 0:
            break
        cnt2 -= 1
        if old_cnt == cnt:
            break
        old_cnt = cnt

    return content

# ------------------------------------------------------------------------
# Parse buffer

def recursive_parse(buff, context, local_table, regex = "{ .*? }"):

    regex2 = "[ .*? ]"

    #print("recursive_parse() buff:", buff, "local_table: ", local_table[:1], "\n")
    # Recursively process

    #try:
    #    parsed2 = _parse_one(buff, context, False, local_table, regex)
    #except:
    #    wsgi_util.put_exception("exception in first parser", )
    #    parsed2 = buff
    #
    try:
        parsed3 = _parse_one(buff, context, False, wsgi_global.global_table, regex)
    except:
        wsgi_util.put_exception("exception in second parser ", )
        parsed3 = buff

    try:
        parsed4 = _parse_one(parsed3, context, False, wsgi_global.global_table, regex2)
    except:
        wsgi_util.put_exception("exception in third parser ", )
        parsed4 = buff

    return parsed4

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

# EOF