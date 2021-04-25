#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time, re, traceback
import multiprocessing
from wsgiref import simple_server, util

try:
    from wsgi_global import *
except:
    print("Cannot import", sys.exc_info())
    pass

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

def global_items(item):

    #print("item", "'" + item + "'")
    for aa in global_table:
        if item[2:-2] == aa[0]:
            if type(aa[1]) == str:
                return aa[1]
            if type(aa[1]) == type(global_items):
                try:
                    cccc = aa[1](item)
                except:
                    print(sys.exc_info())
                return cccc

    # "??" #return str(item[2:-2]) + "??"
    return item

# Parameterized last

def global_para_items(item):

    #print("item", "'" + item + "'")
    # rescan for parameterized
    for aa in global_table:
        if item[2:-2].split()[0] == aa[0]:
            if type(aa[1]) == type(global_para_items):
                try:
                    cccc = aa[1](item)
                except:
                    print(sys.exc_info())
                return cccc

    erritem = str(item[2:-2])
    if erritem[0] == '#':
        #print("Ignoring commented:", erritem)
        return ""
    return "!!" + str(item[2:-2]) + "!!"

# Parse buffer

def parse_buffer(buff, flag, regex):

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
            conv = global_para_items(buff[bbb:eee])
        else:
            conv = global_items(buff[bbb:eee])
        arr.append(conv)
        prog += frag.end()
        count += 1

    #print("parsed", count)
    #print ("arr", arr)
    return arr, count

def     recursive_parse(buff, regex = "{ .*? }"):

        # Recursively process
        cnt2 = 4; old_cnt = 0
        content = buff
        while(True):
            arr, cnt = parse_buffer(content, False, regex)
            content = ""
            for aa in arr:
                content += aa

            #print("recursive", cnt)
            if cnt <= 1:
                break
            if cnt2 <= 0:
                break
            cnt2 -= 1
            if old_cnt == cnt:
                break
            old_cnt = cnt

        cnt3 = 4
        while(True):
            arr, cnt = parse_buffer(content, True, regex)
            content = ""
            for aa in arr:
                content += aa

            #print("recursive", cnt)
            if cnt <= 1:
                break

            if cnt3 <= 0:
                break
            cnt3 -= 1
            if old_cnt == cnt:
                break
            old_cnt = cnt

        return content

def put_exception(xstr):

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


