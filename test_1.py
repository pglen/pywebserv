 #!/usr/bin/env python3

import os, sys, time, copy

#_mac1 = '''
#Hello 1
#'''
#
#_mac2 = '''
#Hello 2
#'''

#test_1.py

vvv = locals().copy()

#print("vvv", vvv)

for aa in vvv:
    if "_mac" in aa:
        print(aa, "=", vvv[aa])

