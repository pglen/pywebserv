#!/usr/bin/env python3

import os, getpass, sys, base64, time

# Influencers. Changes cypher text. Modify only if you need a custom
# encryption.

# Just a random str, edit only on special customization
seed = "309812347089lhjkhdfasbsvnm,sdkljd089d908asd089sdajasdl;jk28923"

# Starting vector for the feedback loop
vector = 0xe5

# Limit the rounds
MAXROUNDS = 4

# Rotate by this much
ROTATE = 3

# ------------------------------------------------------------------------
# Simple Encryption / Decryption. Only to get the protocol jump started.
# Make 1.) forward feedback pass, 2.) backward feedback pass, 3.) xor
# with constant seed.
#
# At the time of release, the following cyphertext was output from the
# reference input:
#
#org  ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
#enco ak8QjddpwaVT/77J41X2xhHb9+863YU8Zpu4KQURFKQUaxgV2+RNUrJrknkoMr7kGOnSQA==
#org3 ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz
#
# If your output is different, it will not decode old installation data
# correctly. If this is what you want, update both server and client.

# ------------------------------------------------------------------------
# Helpers
#
# _ror -- rotate byte right          _rol -- rotate byte left
# _rev -- reverse string             _rounds -- call N number of times

def _ror(xint, rotwith):
    return xint
    ret =  xint >> rotwith | xint << (8 - rotwith)
    return ret & 0xff

def _rol(xint, rotwith):
    return xint
    ret =  xint << rotwith | xint >> (8 - rotwith)
    return ret & 0xff

def _rev(xstr):
    ret = bytearray()
    for aa in range(len(xstr)-1, -1, -1):
        ret.append(xstr[aa])
    return ret

def _rounds(rounds, func, arg1, arg2):

    # Limit the rounds, so we have acceptable performance
    #rounds = min(rounds, MAXROUNDS)

    for aa in range(rounds):
        arg1 = func(arg1, arg2)
    return arg1

# ------------------------------------------------------------------------
# Main entry points. We use strlen() rounds to mix it up so one input bit
# change changes every output bit.

def xencrypt(xstr, xpass):
    return _rounds(MAXROUNDS, _xencrypt, xstr, xpass)
    #return _rounds(len(xstr), _xencrypt, xstr, xpass)
    #return _xencrypt(xstr, xpass)

def xdecrypt(xstr, xpass):
    return _rounds(MAXROUNDS, _xdecrypt, xstr, xpass)
    #return _rounds(len(xstr), _xdecrypt, xstr, xpass)
    #return _xdecrypt(xstr, xpass)

# ------------------------------------------------------------------------
# Actual encryption routines

def _xencrypt(xstr, xpass):

    #print("_xencrypt", type(xstr), type(xstr[0]), xstr[0] )

    # Forward
    yprog = 0; xprog = 0; xstr2 = bytearray();
    prop = vector
    for aa in range(len(xstr)):
        chh = xstr[aa] + ord(xpass[xprog]) + ord(seed[yprog]) + prop
        chh2 = _rol(chh & 0xff, ROTATE)
        xstr2.append(chh2 & 0xff)
        xprog += 1; yprog += 1
        if xprog >= len(xpass): xprog = 0
        if yprog >= len(seed):  yprog = 0
        prop = xstr[aa]

    #return xstr2

    # Omit middle pass
    #yprog = 0; xstr2a = ""
    #for aa in range(len(xstr)):
    #    chh = ord(xstr2[aa]) ^ ord(seed[yprog])
    #    yprog += 1
    #    if yprog >= len(seed): yprog = 0
    #    xstr2a += chr(chh)
    #xstr2 = xstr2a

    # Backward
    yprog = 0; xprog = 0; xstr3 = bytearray();
    prop = vector
    for aa in range(len(xstr)-1, -1, -1):
        chh = xstr2[aa] + ord(xpass[xprog]) + ord(seed[yprog]) + prop
        chh2 = _rol(chh & 0xff, ROTATE)
        xstr3.append(chh2 & 0xff)
        xprog += 1; yprog += 1
        if xprog >= len(xpass): xprog = 0
        if yprog >= len(seed):  yprog = 0
        prop = xstr2[aa]

    xstr3 = _rev(xstr3)     # Because we scanned backwards

    return xstr3

# ------------------------------------------------------------------------

def _xdecrypt(xstr, xpass):

    # Backward
    #print(type(xstr), type(xstr[0]), xstr[0] )

    yprog = 0; xprog = 0; xstr2 = bytearray()
    prop =  vector
    for aa in range(len(xstr)-1, -1, -1):
        chhh = _ror(xstr[aa], ROTATE)
        chh = (chhh - ord(xpass[xprog]) - ord(seed[yprog])) - prop
        xstr2.append(chh & 0xff)
        xprog += 1; yprog += 1
        if xprog >= len(xpass): xprog = 0
        if yprog >= len(seed):  yprog = 0
        prop = chh

    xstr2 = _rev(xstr2)     # Because we scanned backwards

    # Omit middle pass
    #yprog = 0; xstr2a = "";
    #for aa in range(len(xstr)):
    #    chh = ord(xstr2[aa]) ^  ord(seed[yprog])
    #    yprog += 1
    #    if yprog >= len(seed):  yprog = 0
    #    xstr2a += chr(chh)
    #xstr2 = xstr2a

    # Forward
    #xstr2 = xstr       # Skip

    yprog = 0; xprog = 0; xstr3 = bytearray();
    prop =  vector
    for aa in range(len(xstr)):
        #chhhh = xstr2[aa]
        chhhh = _ror(xstr2[aa], ROTATE)
        chh = (chhhh - ord(xpass[xprog]) - ord(seed[yprog])) - prop
        xstr3.append(chh & 0xff)

        xprog += 1; yprog += 1
        if xprog >= len(xpass): xprog = 0
        if yprog >= len(seed):  yprog = 0
        prop = chh

    return xstr3

# ------------------------------------------------------------------------
if __name__ == '__main__':

    xpass   = "1234"
    org  = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890"

    if len(sys.argv) > 2:
        org = sys.argv[1]
        xpass = sys.argv[2]
    elif len(sys.argv) > 1:
        org = sys.argv[1]

    org2    = xencrypt(org.encode(), xpass)

    #print("org2", org2)
    #sys.exit()

    enco        = base64.b64encode(org2)

    # Simulated transport goes here -------------->

    deco        = base64.b64decode(enco)
    time_mark   = time.perf_counter()
    org3    = xdecrypt(deco, xpass)
    print("tdelta", "%.4f" % ((time.perf_counter() - time_mark) * 1000), "ms")

    #print( "org3", org3)

    org4    = org3.decode()

    print( "org ",  org )
    print( "enco", enco)
    print( "org4", org4)

    #if deco != org2:
    #    print( "\nERROR! Faulty base 64")

    if org != org4:
        print( "\nERROR! Faulty xencrypt / xdecrypt")

# EOF