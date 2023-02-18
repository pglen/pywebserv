#!/usr/bin/env python3

''' The simplest web server, utilities module. This is where we parse the
    incoming (loaded) files for macros. The substitution occures in steps
    recursively.
'''

#import builtins

import wsgi_util

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
        self.benchmark   = 0
        self.port        = 8000
        self.server      = None
        self.mainclass   = None

    def __str__(self):
        return "verb:"+ str(self.verbose) + " deb:" + str(self.pgdebug)

    def _fillarr(self, selfx):
        #def dummy(): pass
        arr = []
        for aa in dir(selfx):
            # Filter out all sys args and methods
            if aa[:2] == "__":
                continue
            #print(aa, type(getattr(self, aa)))
            if type(getattr(selfx, aa)) == \
                            type(getattr(self, "getvals")):
                continue
            #print(aa, getattr(self, 	aa))
            arr.append(aa)
        return arr

    # Return details of the config, filter all but vars
    def getvals(self):
        sss = ""
        arr = self._fillarr(self)
        for aa in arr:
            sss += wsgi_util.strpad(str(aa), 14) + "  " + \
                  str(getattr(self, aa)) + "\n"

        # Replaced this for automation
        #sss += "mypath: " +     self.mypath + "\n"
        #sss += "datapath: " +   self.datapath + "\n"
        #sss += "verbose: " +    str(self.verbose) + "\n"
        #sss += "pgdebug: " +    str(self.pgdebug) + "\n"
        #sss += "port: " +       str(self.port) + "\n"
        #sss += "benchmark: " +  str(self.benchmark) + "\n"

        return sss

    # Sync one class's extra methods to the other class
    #   (in essence copy config)

    def sync(self, syncto):
        arr = self._fillarr(syncto)
        for aa in arr:
            #print("aa", aa)
            setattr(self, aa, getattr(syncto, aa))

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
