#!/usr/bin/env python3

''' The simplest web server, utilities module. This is where we parse the
    incoming (loaded) files for macros. The substitution occures in steps
    recursively.
'''

def strpad(strx, pad = 18):

    ''' pad string '''

    if len(strx) < pad:
        dd =  pad - len(strx)
        stry = strx + " " * dd
    else:
        stry = strx

    return stry

# ------------------------------------------------------------------------

def strtrim(strx, trim = 18):

    ''' trim string ; adapt to bytes type '''

    if type(strx) == str:
        padd = " ... "
    else:
        padd = b" ... "

    if len(strx) > trim - 3:
        hhh = trim // 2
        stry = strx[:hhh] + padd + strx[-hhh:]
    else:
        stry = strx
    return stry

def strupt(strx, trim = 24):

    ''' Unescape, pad and trim string '''

    strx2 = strunesc(strx)
    strx2 = strtrim(strx2, trim)
    return strx2

def strunesc(strx):
    ''' expand new lines etc ... to \\n '''
    ret = "'"
    for aa in strx:
        if aa == "\r":
            ret += "\\r"
        elif aa == "\n":
            ret += "\\n"
        else:
            ret += aa
    ret += "'"
    return ret

# EOF
