#!/usr/bin/env python3

import os, sys, glob, getopt, time, random
import string, signal, stat, shutil, math

initdir =  "/usr/share/pyfortune/datfiles/"

def help():

    print()
    print("Usage: " + sys.argv[0] + " [options]")
    print()
    print("Options:    -v        - Verbose")
    print("            -f file   - Show fortune from file")
    print("            -d dir    - Show fortune from directory")
    print("            -h        - Help")
    print("            -o        - Allow offensive material, 1:10 mixin")
    print()

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':

    verbose     = False
    offensive   = True
    showfile    = ""
    startdir = os.getcwd()
    fname = ""

    opts = []; args = []
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hvf:d:o")
    except getopt.GetoptError as err:
        print("Invalid option(s) on command line:", err)
        sys.exit(1)

    #print "opts", opts, "args", args

    for aa in opts:
        if aa[0] == "-h": help();  exit(1)
        if aa[0] == "-v": verbose = True
        if aa[0] == "-o":
            if verbose:
                print("Offensive mix in")
            offensive = True

        if aa[0] == "-d":
            initdir = aa[1] + "/"
            if verbose:
                print("Init dir:", initdir)
            if not os.path.isdir(initdir):
                print("No such dir:", initdir)
                exit(2)

        if aa[0] == "-f":
            showfile = aa[1]
            if verbose:
                print("Show File:", showfile)
            if not os.path.isfile(showfile):
                print("No such file:", showfile)
                exit(3)

    ddd = os.listdir(initdir)
    if len(ddd) == 0:
        print("No files in:", initdir)
        exit(2)
    lim = len(ddd)

    for fname in ddd:
        #print("Checking:", fname)
        try:
            fp = open(initdir + "//" + fname, encoding='utf-8')
        except:
            print("Cannot open:",  fname, sys.exc_info()[1])

        try:
            buff = fp.read()
        except:
            print("Cannot fread from:",  fname, sys.exc_info()[1])


    '''
    if verbose:
        print("Listing fortune from:", fname)

    if not os.path.isfile(fname):
        print("File is not a regular file:", fname)
        exit(4)

    try:
        fp = open(fname, encoding='utf-8')
    except:
        print("Cannot open:",  fname, sys.exc_info()[1])
        exit(1)

    try:
        buff = fp.read()
    except:
        print("Cannot fread from:",  fname, sys.exc_info()[1])
        exit(1)

    buff2 = buff.split("\n%\n")
    idx =  int(random.random() * len(buff2))
    print(buff2 [idx])

'''