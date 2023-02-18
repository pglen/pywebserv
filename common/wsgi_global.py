#!/usr/bin/env python3

''' These tags / funtions / tables are global to the site '''

import sys, time, importlib

# Get strings and functions

from wsgi_style import *
from wsgi_res   import *
from wsgi_func  import *
import wsgi_util

# A list of variables and strings. Making an error here will down the site.
# The newly defined local macro can override the global one. Make sure you do not expect
# nested override, as the macro is expanded with locals first, globals second;
# The local macro will not override the macro that is uncovered by global
# macro expansion;

global_table_init = [
    ["spacer",          "<table><tr><td></table>"],
    ["linespacer",      "<tr><td height=8>"],
    ["sitecolor",       "bgcolor=#aaffbb"],
    ["feedwidth",       "400"],
    ["feedheight",      "300"],
    ["thumbwidth",      "120"],
    ["thumbheight",     "80"],
    ["nullcolor",       "#cccccc"],
  ]

# ------------------------------------------------------------------------
# URL to function mapping

class UrlMap():

    ''' This class stores the URL to function mapping '''

    def __init__(self):
        self.urls = []

    def dump(self):
        def ph(): pass
        ret = ""
        for aa in self.urls:
            if type(aa[1]) ==  type(ph):
                #print("url F", wsgi_util.strpad(aa[0]),  \
                #    wsgi_util.strpad(aa[1].__name__), aa[2])
                bb = aa[1].__name__
            else:
                bb = aa[1]

            ret += wsgi_util.strpad(str(aa[0])) + \
                       wsgi_util.strpad(str(bb)) + str(aa[2]) + "\n"
        return ret

    def add(self, url, func, page, fname):
        # Got one already?
        #for aa in self.urls:
        #    if aa[0] == url:
        #        return
        self.urls.append((url, func, page, fname))

    def lookup(self, url):

        #print("Looking up url", url)

        for aa in self.urls:
            #print("src url", aa[0], aa[1])
            if aa[0] == url:
                return aa[1], aa[2], aa[3]

        # Not found ...
        return None, None, None

    # Find first level of URL
    def revlookup(self, rev):
        rrr = rev.split(os.sep)
        for aa in self.urls:
            sss = aa[0].split(os.sep)
            #print("rev url", sss[1], "aa 1", aa[1], aa[2])
            try:
                #print(rrr, sss);
                if rrr[1] == sss[1]:
                    return os.path.split(aa[3])
            except:
                pass
        return ""

    # ------------------------------------------------------------------------
    # Add functions to URL map
    # One may override any file; in that case the values are filled in

    # We build it dynamically, so error is flagged

    def     add_one_url(self, url, mfunc, mpage = None, fname = ""):

        '''
        Add a url and a function here. Also, an optional template. The template is assumed
        to be in the same directory as the script. If no template is added, the following
        places will be searched: the project "./" directory,  the /static/ directory.
        If the template cannot be found, the return value of the function output is delivered as
        it was generated without template substitution.
        '''

        if not mpage:
            mpage = "index.html"

        try:
            self.add(url, mfunc, mpage, fname)
        except:
            print("Cannot add url map", sys.exc_info())

    # ------------------------------------------------------------------------
# URL to function table, global

urlmap =  UrlMap()

# ------------------------------------------------------------------------
# Add a new project function;

class Table():

    def __init__(self):

        self.mytable = []
        for aa in global_table_init:
            self.mytable.append(aa)

    def add_one_func(self, mname, mfunc, mpage = None, fname=None):
        '''
             Add a macro function or string here. The macro is substituted
            by the output of the function. Macro syntax is words surrounded by
            '{ ' and ' }' as in { macro }
            if macro is a string, substitution is made in line.

              It is also permissible to add a python variable as the value for
            substitution. It is substituted recursively, so variables in
            variables are permitted. The max nesting depth is 10.
              The arguments to a macro are expanded when enclosed in  '[ arg ']'
            like: { mymacro [ arg_one ] two three }
            The macro (after substation) receives the argument string verbatim.
        '''

        #print("adding mname", mname)

        #global global_table
        try:
            #see if there is an entry already
            for aa in self.mytable:
                if aa[0] == mname:
                    #print("Duplicate macro:", mname)
                    return 1
            self.mytable.append([mname, mfunc])
        except:
            print("Cannot add global table item", sys.exc_info())
        return 0

    def lookup_item(self, item):
        for aa in self.mytable:
            if aa[0] == item:
                return aa[1:]
        return ""

    def dump_table(self):
        for aa in self.mytable:
            nnn = wsgi_util.strpad("'" + str(aa[0]) + "'")
            print(nnn, " = ", end = " ")
            #print("type", type(aa[1]))

            if type(aa[1]) == type(""):
                print("'" + aa[1][:24].replace("\n", "\\n") + "'")
            elif type(aa[1]) == type([]):
                print("ARR ", aa[1][0])
            else:
                print("'" + aa[1].__name__ + "()" +"'")

gl_table = Table()


# ------------------------------------------------------------------------

def  _load_project(pdir, mainclass):

    ret = []
    try:
        sys.path.append(pdir)
        files = os.listdir(pdir)
        for aa in files:
            if aa[-3:] == ".py":
            #if aa[-8:] == "index.py":
                fname = pdir + os.sep + aa
                if os.path.exists(fname):
                    mname =  pdir + "." + aa[:-3]
                    #print("mname", mname);
                    #print("modules", sys.modules.keys())
                    if mname in sys.modules.keys():
                        #print("imported already", mname)
                        continue
                    try:
                        fp = open(fname)
                        fff = fp.read().split()
                        mod = importlib.__import__(mname, globals(), locals(), fff, 0)
                    except:
                        wsgi_util.put_exception("Cannot import module: '%s'" % (fname, ))
                        msg = "Module %s failed to load" % aa
                        #print("msg", msg)
                        ret = [msg.encode("utf-8"),]
                        # Keep loading
                        continue

                    ''' did not work
                    try:
                        cmd = mod.__name__ + ".initialize()"
                        print("init", cmd)
                        xx = compile(cmd, "<string>", 'exec')
                        exec(xx)
                    except:
                        wsgi_util.put_exception("Cannot initialize module: '%s' " % aa)
                        msg = "Module %s failed to init" % aa
                        ret = [msg.encode("utf-8"),]
                        return ret
                    '''
    except:
        #print("Cannot import guest project", sys.exc_info())
        wsgi_util.put_exception("Cannot import:")
        ret = [b"Some modules failed to load"]

    return ret

# ------------------------------------------------------------------------
# Load all projects from dirs starting with "proj"

def     getprojects(mainclass):

    '''
        Add (import) projects in directories starting with 'proj'
        for automatic inclusion into the site.
        The initial proj-ect dir was called 'projects'
    '''

    pdir = "proj"
    dirs = os.listdir(".")
    for aa in dirs:
        if os.path.isdir(aa):
            if aa[:4] == pdir:
                _load_project(aa, mainclass)

    #print("pl delta", "%.4f" % ( (time.perf_counter() - mainclass.mark) * 1000), "ms")

    # Print all URLS
    cnt = 0
    for aa in urlmap.urls:
        # Check for duplicate
        ddd = 0; url = ""; xcnt = 0
        for bb in urlmap.urls:
            if aa[0] == bb[0]:
                ddd += 1
                url = bb[0]
                xcnt = cnt
        cnt += 1
        if ddd > 1:
            print("   ** Warn: Duplicate URL", xcnt, url)

# EOF
