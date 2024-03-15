#!/usr/bin/env python3

import os, sys, time, uuid, string, random, signal, getopt

sys.path.append("common")
import wsgi_pass

allpass  =    string.ascii_lowercase
maxiter = 100000

# Return a random string based upon length

def randpass(lenx):

    strx = ""
    for aa in range(lenx):
        ridx = random.randint(0, len(allpass)-1)
        rr = allpass[ridx]
        strx += str(rr)
    return strx

def passgen(uname, xlen = 6):

    rrr = ""
    for aa in range(maxiter):
        sss = randpass(xlen)
        if wsgi_pass.passcheck(uname, sss, wsgi_pass.modulus):
            rrr = sss
            break
        #print("sss", sss)
    return aa, rrr

maxx = 0

def terminate(arg, arg2):
    print("\n", maxx)
    sys.exit(0)

def help():
    print("Usage: passgen.py [options] [arg_key arg_data]")
    print(" Options:    -h         help (this screen)")
    print("             -l         pass length")
    print("             -u         user name")
    print("             -v         verbose")

if __name__ == '__main__':

    xlen = 8
    uname = "user"
    verb = 0

    signal.signal(signal.SIGINT, terminate)

    opts = []; args = []
    opts_args = "l:hu:v"
    try:
        opts, args = getopt.getopt(sys.argv[1:], opts_args)
    except getopt.GetoptError as err:
        print(_("Invalid option(s) on command line:"), err)
        sys.exit(1)

    for aa in opts:
        if aa[0] == "-h" or aa[0] == "-?":
            help(); exit(1)
        if aa[0] == "-l":
            try:
                xlen = int(aa[1])
            except:
                xlen = 6
        if aa[0] == "-u":
            uname = aa[1]
        if aa[0] == "-v":
            verb = 1

    if verb:
        print("mod", wsgi_pass.modulus, "user", uname)

    while 1:
        ppp = passgen(uname, xlen)
        print(uname, ppp)

        ret = wsgi_pass.passcheck(uname, ppp[1], wsgi_pass.modulus)
        if verb:
            print("check", ret)

        if ppp[1] == "":
            break
        if maxx < ppp[0]:
            maxx = ppp[0]
        break

# EOF
