#!/usr/bin/python3

import sys

def validate(fname):

    fp = open(fname)
    hashx = int(0);
    old_hash = str("None")

    while True:
        line = fp.readline()
        if not line:
            break

        line = line.strip()
        if not line:
            continue
        if line[0] == '#':
            if "hashx signature" in line:
                hhh = str.split(line)
                for aa in hhh:
                    if len(aa) > 2:
                        if aa[:2] == "0x":
                            #print("Hash:", aa)
                            old_hash = aa
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

    return old_hash, hex(hashx)

def strpad(strx, pad = 18):

    ''' pad string '''

    if len(strx) < pad:
        dd =  pad - len(strx)
        stry = strx + " " * dd
    else:
        stry = strx

    return stry

if __name__ == '__main__':
    ret = 0
    for aa in sys.argv[1:]:
        ohashx, hashx = validate(aa)
        #print("hashx", hashx)

        if ohashx != hashx:
            ret |= 1
            ttt = "  "
        else:
            ttt = "Un"
        print ("%sModified file" % ttt, strpad(aa), "Old hash:",
                                strpad(ohashx, 10), "New hash:",  hashx)
    sys.exit(ret)
