#!/usr/bin/env python3

'''
    Search for functions by 'def ' string
'''

import sys, os, time
import mimetypes, subprocess


def append_filename(nnn):
    global fnamearr, statarr

    if os.path.isfile(nnn):
        fff = os.stat(nnn).st_mtime
        # Two synchronized arrays
        fnamearr.append(nnn)
        statarr.append(fff)

# ------------------------------------------------------------------------
# Scan all files in one deep directory

def  rescan():
    global fnamearr, statarr

    fnamearr = []; statarr = []
    fnamearr2a = os.listdir()
    #print("fnamearr2a", fnamearr2a)

    for aaa in fnamearr2a:
        if os.path.isdir(aaa):
            # No need for these files
            if "__" in aaa:
                continue
            if ".git" in aaa:
                continue
            if "data" in aaa:
                continue
            _rescan(aaa)
        if os.path.isfile(aaa):
             append_filename(aaa)
    #print("fnamearr", fnamearr)

# ------------------------------------------------------------------------

def _rescan(dirx):

    fnamearr2 = os.listdir(dirx)
    for aa in range(len(fnamearr2)):
        nnn = dirx + os.sep + fnamearr2[aa]
        #print("nnn", nnn)
        if os.path.isfile(nnn):
             append_filename(nnn)
        elif os.path.isdir(nnn):
            _rescan(nnn)
    return None

# ------------------------------------------------------------------------
# Entry point for the server

if __name__ == '__main__':

    #path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    #port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    global fnamearr, statarr
    rescan()
    #print("fnames", fnamearr)

    for aa in fnamearr:
        got = 0
        if aa[-3:] == ".py":
            fp = open(aa)
            if not fp:
                continue
            vvv = fp.read()
            for bb in vvv.split("\n"):
                if "def " in bb:
                    if not got:
                        print("File:", aa)
                        got = True
                    print(" ", bb)
            fp.close()

# EOF
