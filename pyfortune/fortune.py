#!/usr/bin/env python3

''' return a fortune '''

import os, random

def _randfortune(fname):

    try:
        fp = open(fname, encoding='utf-8')
    except:
        print("Cannot open:",  fname, sys.exc_info()[1])
        return "Cannot open fortune"

    try:
        buff = fp.read()
    except:
        print("Cannot fread from:",  fname, sys.exc_info()[1])
        exit(1)

    buff2 = buff.split("\n%\n")
    idx =  int(random.random() * len(buff2))

    #print(buff2[idx])
    return buff2[idx]

# ------------------------------------------------------------------------

def _randfile(initdir, offensive):

    # Mix in offensive
    if offensive:
        if  random.random() <= 0.1:
            if os.path.isfile(initdir + "offensive/"):
                initdir += "offensive/"

    fname = ""
    ddd = os.listdir(initdir)
    if len(ddd) == 0:
        print("No files in:", initdir)
        return fname

    lim = len(ddd)
    while lim >= 0:
        fname = initdir + ddd[int(random.random() * len(ddd))]
        if os.path.isfile(fname):
            break
        lim -= 1

    return fname

def randfortune(initdir, offensive):

    ''' Deliver a fortune, try several times for criteria '''

    tries = 0
    while True:
        if tries > 5:
            fort = "Error generating fortune"
            break
        tries += 1
        fname = _randfile(initdir, offensive)
        if not os.path.isfile(fname):
            print("File is not a regular file:", fname)
            continue
            #exit(4)
        fort  = _randfortune(fname)
        flen = len(fort)
        if flen > 5 and flen < 100:
            break
        #if tries > 0:
        #    print("Error on gen", tries, file=sys.stderr)
    return  fort
