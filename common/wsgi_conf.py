#!/usr/bin/env python3

''' The simplest web server, utilities module. This is where we parse the
    incoming (loaded) files for macros. The substitution occures in steps
    recursively.
'''

import builtins

# Config global; After testing some crap, this was the simplest

class Configx:

    '''
    Parameters are going around with this class
    '''
    mypath      = ""
    datapath    = ""
    server      = None
    mainclass   = None
    #debug       = 0
    verbose     = 0
    pgdebug     = 0
    port        = 8000

builtins.Config = Configx

#def showvals():
#
#    return "Verb = " + str(Config.verbose),  "Deb = " + str(Config.pgdebug)
#

# EOF
