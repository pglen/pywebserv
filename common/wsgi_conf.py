#!/usr/bin/env python3

''' The simplest web server, utilities module. This is where we parse the
    incoming (loaded) files for macros. The substitution occures in steps
    recursively.
'''

import wsgi_util, wsgi_str

def fillxarr(selfx):
    arr = []
    for aa in dir(selfx):
        # Filter out all sys args and methods
        if aa[:2] == "__":
            continue
        #print(aa, type(getattr(self, aa)))
        if type(getattr(selfx, aa)) == \
                        type(getattr(selfx, "__init__")):
            continue
        #print(aa, getattr(self, 	aa))
        arr.append(aa)
    return arr


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
            sss += wsgi_str.strpad(str(aa), 14) + "  " + \
                  str(getattr(self, aa)) + "\n"
        return sss

    # Sync one class's extra methods to the other class
    #   (in essence copy config)

    def sync(self, syncto):
        arr = self._fillarr(syncto)
        for aa in arr:
            #print("aa", aa)
            setattr(self, aa, getattr(syncto, aa))

class CarryOn:

    '''
    Parameters are going around all the way to processing
    '''
    def __init__(self):
        self.environ = None
        self.mainclass = None

    def getvals(self):
        strx = ""
        arr = fillxarr(self)
        #print("arr", arr)
        for aa in arr:
            bb = str(getattr(self, aa))
            bb  = wsgi_str.strtrim(bb, 36)
            strx += wsgi_str.strpad(str(aa)) + \
                         " = " + bb + "\n"
        return strx

# EOF
