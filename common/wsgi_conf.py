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

    def tostr():
        print("verb:", Configx.verbose, "deb:", Configx.pgdebug)

builtins.Config = Configx

class CarryOn:

    '''
    Parameters are going around all the way to processing
    '''
    def __init__(self):

        self.environ = None
        self.mainclass = None

    def tostr(self):
        print("environ:", Carryon.environ, "mainclass:", Configx.pgdebug)

    def print(self):
        print("self.carryon.url",     self.url)
        print("self.carryon.query",   self.query)
        print("self.carryon.request", self.request)
        print("self.carryon.tmplate", self.template)
        print("self.carryon.fname",   self.fname)

#def showvals():
#
#    return "Verb = " + str(Config.verbose),  "Deb = " + str(Config.pgdebug)
#

# EOF
