#!/usr/bin/python3

import os, sys, getopt, errno
from common import wsgi_str

import gettext
gettext.bindtextdomain('pyedpro', './locale/')
gettext.textdomain('pyedpro')
_ = gettext.gettext

SIGX = "hashx signature"

def hexx(num):
    return "0x%08x" % num

def validate(fname):

    fp = open(fname)
    hashx = int(0);
    old_hash = str("None")

    old_tell = 0; sum_tell = 0

    while True:
        old_tell = fp.tell()
        line = fp.readline()
        if not line:
            break

        line = line.strip()
        if not line:
            continue
        if line[0] == '#':
            if SIGX in line:
                hhh = str.split(line)
                for aa in hhh:
                    if len(aa) > 2:
                        if aa[:2] == "0x":
                            #print("Old Hash:", aa)
                            old_hash = aa
                            sum_tell = old_tell
            continue


        res = 0
        for aa in line:
            if not str.isspace(aa):
                #print(aa, end="")
                res += ord(aa)
                aaa = ord(aa)
                hashx +=  int( (aaa << 12) + aaa)
                hashx &= 0xffffffff
                hashx = int(hashx << 8) + int(hashx >> 8)
                hashx &= 0xffffffff
        #print()

    if not sum_tell:
        print("seekng EOF")
        sum_tell  = fp.tell()

    fp.close()

    return old_hash, hexx(hashx), sum_tell


def addhash(fname, hashx, stell):
    #print("Adding hash to", fname, stell)
    fp = open(fname, "r+t")
    fp.seek(stell)
    fp.write("# " + SIGX  + " " + hashx )
    fp.close

# ------------------------------------------------------------------------

if __name__ == '__main__':

    ret = 0
    checksum = False;    verbose = False
    myopts  = "vm";      argopts = "d:"

    try:
        opts, args = getopt.getopt(sys.argv[1:], myopts + argopts,
                        ["debug=", "help", "help", "verbose", "version", ])

    except getopt.GetoptError as err:
        print(_("Invalid option(s) on command line:"), err)
        sys.exit(1)

    for aa in opts:
        if aa[0] == "-d" or aa[0] == "--debug":
            pass
        if aa[0] == "-m":
            #print("adding checksum")
            checksum = True

        if aa[0] == "-v":
            #print("adding checksum")
            verbose = True

    if len(args) < 1:
        print("use: validate.py filename [filename ... ]")
        sys.exit(0)

    for aa in args:

        try:
            ohashx, hashx, stell = validate(aa)
            #print("ohashx:", ohashx, "hashx:", hashx, "stell:", stell)
        except Exception as  ioex:
            print("Cannot process", "'" + aa + "'", os.strerror(ioex.errno))
            continue

        if checksum:
            if ohashx != hashx:
                if verbose:
                    print("Adding hash:", hashx)
                addhash(aa, hashx, stell)
            else:
                if verbose:
                    print("Hash checks out at", hashx)

        else:
            if ohashx != hashx:
                ret |= 1
                ttt = "  "
            else:
                ttt = "Un"
            print ("%sModified file" % ttt, wsgi_str.strpad(aa), "Old hash:",
                                    wsgi_str.strpad(ohashx, 10), "New hash:",  hashx)
    sys.exit(ret)
# hashx signature 0x5ce23ee8
More stuff
New test