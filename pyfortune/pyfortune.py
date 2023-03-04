#!/usr/bin/env python3

import os, sys, glob, getopt, time, random
import string, signal, stat, shutil, math

from fortune import *

initdir =  "/usr/share/pyfortune/datfiles/"

def help():

    print()
    print("Usage: " + sys.argv[0] + " [options]")
    print()
    print("Options:    -v        - Verbose")
    print("            -f file   - Show fortune from file")
    print("            -d dir    - Show random fortune from directory")
    print("            -h        - Help")
    print("            -o        - Allow offensive material, 1:10 mixing ratio")
    print()

# ------------------------------------------------------------------------
# Start of program:

if __name__ == '__main__':

    verbose     = False
    offensive   = False
    showfile    = ""
    startdir = os.getcwd()
    fname = ""

    # Make sure we have installation, else work from source
    if not os.path.isdir(initdir) :
        initdir = startdir + os.sep + "datfiles" + os.sep

    if not os.path.isdir(initdir) :
        print("Cannot find init dir, giving up")
        sys.exit(0)

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

    if verbose and offensive:
        print("Offensive random selection", initdir)

    #if verbose:
    #    print("File:", fname)

    if showfile != "":
        print("showing file", showfile)
        fort = showfile
    else:
        fort = randfortune(initdir, offensive)
        print(fort)

