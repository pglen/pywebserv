#!/usr/bin/env python3

# This default for non production
modulus = 1234

try:
    from modulus import *
except:
    pass

def passcheck(user, sss, modx):

    sumx = 1
    for bb in user:
        sumx += ord(bb)
    for aa in sss:
        #print(ord(aa), end= " ")
        sumx *= ord(aa)
        sumx += ord(aa)
    #print("sumx", sumx)
    return sumx % modx == 0 and sumx % 7 == 0 and sumx % 8 == 0

# EOF


