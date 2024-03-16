#!/usr/bin/python3

import os, sys, getopt, errno
from common import wsgi_str

cwdx = ""
arrx = []

def listdir(dirx):
    global cwdx, arrx
    listx = os.listdir(".")
    for aa in listx:
        #print(aa)
        if aa[0] == ".":
            continue
        if "__" in aa:
            continue
        # Exclude unlikely directories
        ignore = ["build", "test", "old", "doc", "content",]
        if os.path.isdir(aa):
            was = False
            for bb in ignore:
                if bb in aa:
                    was = True
            if was:
                continue

            #print("dir", "'" + aa + "'")
            cwdx += aa  + os.sep
            #print("cwdx", "'" + cwdx + "'")
            os.chdir(aa)
            listdir(".")
            os.chdir("..")
            cwdx = cwdx[:-len(aa) -1]
            #print("cwdx", "'" + cwdx + "'")

        elif aa[-3:] == ".py":
            # Exclude non documentables
            ignore = ["gendocs", "setup", "test", "conf.py", "__", "install", ]
            was = False
            for bb in ignore:
                if bb in aa:
                    was = True
            if was:
                continue
            curr = cwdx + aa
            #print(curr)
            arrx.append(curr)

listdir(".")

for aa in arrx:
    print(aa)
    old = os.getcwd()
    #print("old", old)
    #print("dir", os.path.dirname(aa))
    os.system("PYTHONPATH=%s:%s:%s pdoc --force --html -o doc %s" % \
                                (os.path.dirname(aa), "common", "pydbase", aa))
    #os.chdir(old)

# EOF