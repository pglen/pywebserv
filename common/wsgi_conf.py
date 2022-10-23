#!/usr/bin/env python3

''' The simplest web server, utilities module. This is where we parse the
    incoming (loaded) files for macros. The substitution occures in steps
    recursively.
'''

#import builtins

# Config global; After testing some crap, this was the simplest

class Configx:

    '''
    Parameters are going around with this class
    '''

    def __init__(self):
        self.mypath      = ""
        self.datapath    = ""
        self.verbose     = 0
        self.pgdebug     = 0
        self.port        = 8000
        self.server      = None
        self.mainclass   = None

    def __str__(self):
        return "verb:"+ str(self.verbose) + " deb:" + str(self.pgdebug)

    # Return details of
    def getvals(self):
        sss = ""
        sss += "mypath: " +     self.mypath + "\n"
        sss += "datapath: " +   self.datapath + "\n"
        sss += "verbose: " +    str(self.verbose) + "\n"
        sss += "pgdebug: " +    str(self.pgdebug) + "\n"
        sss += "port: " +       str(self.port) + "\n"

        return sss

#builtins.Config = Configx

class CarryOn:

    '''
    Parameters are going around all the way to processing
    '''
    def __init__(self):

        self.environ = None
        self.mainclass = None

    def tostr(self):
        print("environ:", Carryon.environ, "mainclass:", Configx.pgdebug)

    def getvals(self):
        strx = ""
        strx += "self.carryon.url " + self.url + "\n"
        strx += "self.carryon.query " +   self.query + "\n"
        strx += "self.carryon.request " +  self.request + "\n"
        strx += "self.carryon.tmplate " + self.template + "\n"
        strx += "self.carryon.fname " +   self.fname + "\n"
        return strx

#def showvals():
#
#    return "Verb = " + str(Config.verbose),  "Deb = " + str(Config.pgdebug)
#

# EOF
