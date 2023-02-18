#!/usr/bin/env python3


'''!  \mainpage

 The simplest web server. This directory is at the root of the web server.

 The sub directories listed below contain the following functionality:

        common              the code for the server
        data                for database related
        content             where the content files live
            siteicons       icons for this site
            media           images, media
            static          files that may be presented as is
            proj-*          python and html / css files that make up the site
                index.py    included by default
                macros.py   macros included in project
                common.py   common to this project

&nbsp;To create a <b>new web project</b>, add a new directory that starts with "proj"
 (like "proj-index") and populate the files. At least one python file is needed,
 must be named 'index.py'

&nbsp;To create a <b>new web page</b>, add a new python file, and call the
URL registration function(s) within. The server redirects the url
to the function you specify.

            add_one_url("/index.html",  got_index,            "index.html")
            add_one_url("/",            got_index,            "index.html")
                         ^__URL         ^__function to call   ^__template to use

 To create a new 'macro' use the add macro function with the macro name
and the name of the function that is executed by the macro. The macro
will be replaced by the return value of the function. The macro
is created by surrounding braces with a space. Like: { mymacro }
The macro regex is '{ .*? }' [the '?' is for non greedy wild card)

  add_one_func("mymacro",  my_macro_func)

  Macro 'auto' files:

     The variables in the files start with "_mac_" will become local
    macros, that can be  referenced on this page.
    Variables start with "_glob_" will become global that can be
    referenced on the whole site. See: ./contents/Proj-xxx/macros.py
    The variables start with "_func_" will become local functions

     The project files are imported under a try: except clause, so ordinarily,
    a mistake (like syntax error) can down the site, only the particular
    page / project.

    However, some conditions (like missing site dependencies)
     CAN down the site.

 # The built in macros:   (see source for complete list)

 ### { image nnn [ www ] [ hhh ] }

Put an image html tag nnn in the output. The optional arguments create the following:

        image nnn www

Put an image tag in the output, resize width to requested. Preserve the
image's aspect ratio.

        image nnn www hhh

Put an image tag in the output, re-size to width / height. The re-sized image is
cached and presented on the next call.

The images are searched for in local / global / static ... directories;

 ### { include fname }

--  Include a file. Read and present file verbatim. Will search
for a file in local / global / static / css directories. Most useful
for common project headers / footers.

 ## Commenting out macros:

  Normally a macro is delimited by { macro }, so changing the delimiter will
make it a non macro. In the examples we use underscore like this: {_macro }
The parser will print the string as normal, so to hide it from the browser
we add the html comments around it. Like: <!-- {_macro } -->

 ## Space in macros arguments:

 The macro arguments are parsed by assuming the space character as the delimiter.
The work around is to use the HTML &nbsp; space symbol. Like: Hello&nbsp;World

 ## Unrecognized macros:

 The macros that are not recognized are printed verbatim into the HTML stream.
This is to signal the developer that the macro is not valid.


'''

import sys, os, mimetypes, time, datetime, getopt, traceback

def tracex(xstr):

    '''!  Trace current fault.
         This was crafted, so the apache run time can access it without any includes.
      '''

    cumm = xstr + " "
    a,b,c = sys.exc_info()
    #print(a,b,c)
    if a != None:
        cumm += str(a) + " " + str(b) + "\n"
        try:
            #cumm += str(traceback.format_tb(c, 10))
            ttt = traceback.extract_tb(c)
            for aa in ttt:
                #print( "trace stack item ", aa)
                cumm += " *** File: " + os.path.basename(aa[0]) + \
                        " Line: " + str(aa[1]) + "\n" +  \
                    "   Context: " + aa[2] + " -> " + aa[3] + "\n"
        except:
            print( "Could not print trace stack. ", sys.exc_info())
    print(cumm)

try:
    from urllib.parse import urlparse, unquote, parse_qs, parse_qsl
except ImportError:
     from urlparse import urlparse, unquote, parse_qs, parse_qsl

from wsgiref import simple_server, util

import gettext
gettext.bindtextdomain('pyedpro', './locale/')
gettext.textdomain('pyedpro')
_ = gettext.gettext

class comline():

    '''! Command line action defines '''

    CLEAR_CONFIG = False
    SHOW_CONFIG = False
    SHOW_TIMING = False
    USE_STDOUT = False     ##!< Variable values

class Myconf():

    '''! Simplified config for propagating command line to runtime '''

    def __init__(self):

        # The sync routine will re-create it all
        self.verbose = 0;
        self.pgdebug = 0;
        self.benchmark = 0;
        self.show_keys  = 0
        self.port = 8000
        pass

# ------------------------------------------------------------------------

mainclass = None

# ------------------------------------------------------------------------
# WSGI main entry point

def application(environ, respond):

    '''!
    WSGI main entry point. The web server (like apache) will call this.
    '''

    global myconf, mainclass

    # Scan for command from wsgi
    #for kk in environ.keys():
    #    if 'WSGI_PARAMS' == kk:
    #        #print(kk, environ[kk])
    #        wsgi_comm = environ[kk]

    wsgi_comm  = environ.get('WSGI_PARAMS')
    if not wsgi_comm: wsgi_comm = ""
    else: print("wsgi_comm", wsgi_comm)

    #if myconf.verbose > 1:
    #try:
    #    #print("Started:")
    #    print(environ['WSGI_PARAMS'])
    #except:
    #    pass

    time_mark = time.perf_counter()

    try:
        # Make sure we are landing here
        mypath = os.path.dirname(os.path.realpath(__file__));
        sys.path.append(mypath)
        sys.path.append(mypath + os.sep + "common")
        os.chdir(mypath + os.sep + "content");
        sys.path.append(mypath + os.sep + "content")

        import wsgi_util, wsgi_content, wsgi_global, wsgi_conf, wsgi_class

        #wsgi_util.append_file("Started Server Page\n")

        #global usr_cnt
        #usr_cnt += 1

        # Only do it one time (not for dev deployment)
        #print("Query arrived", os.getpid(), usr_cnt)
        #if ".html" in environ['PATH_INFO']:
        #    print("tdelta0", environ['PATH_INFO'], "%.4f" %
        #                ( (time.perf_counter() - time_mark) * 1000), "ms")

        # this config comes from the command line ...
        #    ... we patch env into it from wsgi
        try:
            if not myconf:
                myconf =  Myconf()   ##!< Myconf in WSGI
        except:
            myconf =  Myconf()   ##!< Myconf in WSGI

        if "-b" in wsgi_comm:
            myconf.benchmark = 1

        if "-v" in wsgi_comm:
            myconf.verbose = 1

        if not mainclass:
            try:
                mainclass = wsgi_class.xWebServer(environ, respond)

                if mainclass.configx.pgdebug > 1:
                    print("Created instance")

            except:
                wsgi_util.put_exception("Creating Server OBJ")
                respond('500 Internal Server Error', [('Content-Type', "text/html" + ';charset=UTF-8')])
                msg = b"The server cannot create an instance of its main class."
                return [msg,]

        # re - decorate (sync command line config)
        mainclass.configx.sync(myconf)
        if myconf.verbose > 2:
            print(mainclass.configx.getvals())

        #wsgi_util.dump_global_table()

        if mainclass.configx.pgdebug > 1:
            wsgi_util.printenv(environ, False)

        if mainclass.configx.benchmark:
            print("tdelta0", environ['PATH_INFO'], "%.4f" %
                ( (time.perf_counter() - time_mark) * 1000), "ms")

        # Optimize this to load the current project only
        #print("Curr proj", environ['PATH_INFO'])

        try:
            wsgi_global.getprojects(mainclass)
        except:
            wsgi_util.put_exception("Loading Projects")

        #print("Main object inited", mainclass)

        if mainclass.configx.benchmark:
            print("tdelta1", environ['PATH_INFO'], "%.4f" %
                ( (time.perf_counter() - time_mark) * 1000), "ms")

        mainclass.parse_instance(environ, respond)

        if mainclass.configx.benchmark:
            print("tdelta2", environ['PATH_INFO'], "%.4f" %
                               ( (time.perf_counter() - time_mark) * 1000), "ms")

        wdata = ""
        try:
            wdata = mainclass.process_request(environ, respond)
        except:
            print("Exception in process request", sys.exc_info())
            #tracex("Exception in process_request:")
            # We hadle it with the caller, after printing some stuff
            raise

        if mainclass.configx.benchmark:
            print("tdelta3", environ['PATH_INFO'], "%.4f" %
                               ( (time.perf_counter() - time_mark) * 1000), "ms")
        # All went OK
        return wdata

    except:
        #print("Exception in main:", sys.exc_info())
        tracex("Exception in main, trace:")
        content = "Script error; on requesting URL: '" + environ['PATH_INFO'] + "'"

        if myconf.verbose:
            print("Error in main", sys.exc_info())

        # Search for 500 file
        errfile = ""
        while True:
            fn4 = mainclass.configx.datapath +  "html/500.html"
            if os.path.isfile(fn4):
                errfile = fn4
                break
            break

        if errfile:
            #print("found error file", errfile)
            content = wsgi_content.got_500(mainclass.configx, errfile, "")
        else:
            content = "Error on presenting the '500' file. Please contact the admin."

        respond('500 Internal Server Error', [('Content-Type', "text/html" + ';charset=UTF-8')])
        return [bytes(content, "utf-8"),]

def xversion():
    print("Version 1.0")
    #sys.exit(0)

def xhelp():
    print("wsgi_main.py: web server command line and WSGI driver")
    print("Use: wsgi_main [options] ")
    print(" Where options may be:")
    print("    -d level     --  set debug level [0-10]")
    print("    -h           --  help (this screen) alias: ?")
    print("    -v           --  increase verbosity 0 = none 1 = some 2 = more ...")
    print("    -V:          --  Show version")
    print("    -p port      --  Set port to listen on")
    print("    -b           --  print benchmark timing info")
    print("    -x           --  Reserved ")
    print("    -c           --  Reserved ")
    print("    -o           --  Reserved ")
    print("    -t           --  Reserved ")

    sys.exit(0)

# ------------------------------------------------------------------------



if __name__ == '__main__':

    global myconf
    myconf =  Myconf()      ##!< Myconf global

    opts = []; args = []

    myopts = "d:h?vV:xcotp:b"
    try:
        opts, args = getopt.getopt(sys.argv[1:], myopts,
                        ["debug=", "help", "help", "verbose", "version", ])

    except getopt.GetoptError as err:
        print(_("Invalid option(s) on command line:"), err)
        sys.exit(1)

    # Outdated parsing ... for now, leave it as is (has good points to it)
    for aa in opts:
        #print("opt", "'" + aa[0] + "'", aa[1])
        if aa[0] == "-d" or aa[0] == "--debug":
            try:
                myconf.pgdebug = int(aa[1])
                #print( _("Running at debug level:"),  self.configx.pgdebug)
            except:
                myconf.pgdebug = 0
                print(_("Exception on setting debug level"), sys.exc_info())

        if aa[0] == "-p" or aa[0] == "--port":
            try:
                myconf.port = int(aa[1])
            except:
                myconf.port = 0
                print(_("Exception on setting port"), sys.exc_info())

        # Most of these are placeholders
        if aa[0] == "-h" or  aa[0] == "--help" or aa[0] == "-?":
            xhelp()
        if aa[0] == "-V" or aa[0] == "--version":
            xversion()
        if aa[0] == "-v" or aa[0] == "--verbose":
            #print("Setting verbose")
            myconf.verbose += 1
        if aa[0] == "-x":
            comline.CLEAR_CONFIG = True
        if aa[0] == "-c":
            comline.SHOW_CONFIG = True
        if aa[0] == "-t":
            comline.SHOW_TIMING = True
        if aa[0] == "-o":
            comline.USE_STDOUT = True
        if aa[0] == "-t":
            print("Tracing ON")
            sys.settrace(tracer)
        if aa[0] == "-b":
            myconf.benchmark = 1
            #print("Benchmark ON")

    print("\n===== Starting HTTPD on port {}, control-C to stop".format(myconf.port))

    #print("comline", );
    #for aa in dir(comline):
    #    if "__" not in aa:
    #        try:
    #            print(aa, "=", comline.__getattribute__(comline, aa))
    #        except:
    #            pass
    #            print(sys.exc_info())

    class NoLoggingWSGIRequestHandler(simple_server.WSGIRequestHandler):

        '''! Override parent's logging '''

        def log_message(self, format, *args):
            # Do just a little bit of logging on stdout
            if "siteicons" not in args[0] and "media" not in args[0]:
                print(args[0])
            pass
        #print("Args", sys.argv)

    #mypath = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    #port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    httpd = simple_server.make_server('', myconf.port, application,
                                                handler_class=NoLoggingWSGIRequestHandler)

    #print("Begin main args", sys.argv)

    while True:
        try:
            httpd.handle_request()
        except KeyboardInterrupt:
            print("\nShutting down web server.\n")
            httpd.server_close()
            raise
            break

# EOF