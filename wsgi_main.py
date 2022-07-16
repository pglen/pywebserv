#!/usr/bin/env python3

''' The simplest web server. This directory is at the root
of the web server, and sub directories may assume the following functions:

    data            for database related
    content         where the files live
        siteicons       icons for this site
        media           images, media
        static          files that may be presented as is
        proj*           python and html / css files that make up the site


  To create a <b>new project</b>, add a new directory that starts with "proj"
 (like "proj-000") and populate the files. At least one python file is needed.

    To create a <b>new page</b>, add a new python file, and call the
URL registration function(s) within. The server redirects the url
to the function you specify.

  add_one_url("/", got_index, "index.html")

 To create a new 'macro' use the add macro function with the macro name
and the name of the function that is executed by the macro. The macro
will be replaced by the return value of the function. The macro
is created by surrounding braces with a space. Like: { mymacro }
The macro regex is '{ .*? }' [the '?' is for non greedy wild card)

 add_one_func("mymacro", my_img_func)

 Builtin macros:

 { image nnn }          --  Put an image tag nnn in the output
 { image nnn www }      --  Put an image tag in the output, resize width to requested
 { image nnn www hhh }  --  Put an image tag in the output, resize to width / height

The first two forms of the { image } function will preserve the image's aspect ratio.

'''

import sys, os, mimetypes, time, datetime, getopt, traceback

def tracex(xstr):

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

#from urllib.parse import urlparse, unquote, parse_qs, parse_qsl

from wsgiref import simple_server, util

import gettext
gettext.bindtextdomain('pyedpro', './locale/')
gettext.textdomain('pyedpro')
_ = gettext.gettext

class myconf():
    verbose = 0;
    pgdebug = 0;
    show_keys  = 0
    port = 8000
# ------------------------------------------------------------------------

class xWebServer():

    '''
     This class has all the info we would need for page generation. Add urls and functions
     to complete the reply. The return value of the process_rq function is the
     output to the client.
    '''

    def __init__(self, environ, respond):

        ''' Decorate the class instance with data from the environment '''

        # import here so apache wsgi interface gets the files
        import wsgi_global, wsgi_content, wsgi_util
        import wsgi_data, wsgi_func, wsgi_parse
        # wsgi_conf

        #self.mark = time.perf_counter()
        self.respond = respond
        self.environ = environ

        Config.mainclass = self
        Config.mypath = os.path.dirname(os.path.realpath(__file__)) + os.sep
        Config.datapath = Config.mypath + "content" + os.sep

        #if self.config.pgdebug > 6:
        #    print("self.config.mypath", self.config.mypath, "self.config.datapath", self.config.datapath)

        self.stime = datetime.datetime.now()
        try:
            self.sql = wsgi_data.wsgiSql(Config.datapath + "data/wsgi_main.sqlt")
        except:
            print("Warn: Cannot create database", sys.exc_info())

        logf = Config.datapath + "data/wsgi_main.log"
        try:
            self.logfp = open(logf, "a+")
        except:
            import getpass
            print(getpass.getuser())
            print("Cannot open log %s %s" % (getpass.getuser(), logf), sys.exc_info())
            self.logfp = None

        if self.logfp:
            # Print less stuff
            if not "siteicons" in environ['PATH_INFO']:
                sss = [environ['REQUEST_METHOD'], environ['PATH_INFO']]
                print( str(self.stime), *sss, file=self.logfp, flush=True)

            #print( str(self.stime), environ, file=self.logfp, flush=True)

        #if self.config.pgdebug > 8:
        #    wsgi_util.printenv(environ, True)

        #print(environ['wsgi.version'])
        #print("Loaded in ", self.mypath)
        #wsgi_util.print_httpenv(environ)

        wsgi_func.build_initial_table()
        wsgi_func.build_initial_rc()

        self.query = ""
        if 'QUERY_STRING' in environ:
            self.query = parse_qs(environ['QUERY_STRING'], keep_blank_values=True)
            #if self.config.pgdebug > 4:
            #    print("QUERY_STRING", self.query)

        self.cookie = ""
        if 'HTTP_COOKIE' in environ:
            self.cookie = environ['HTTP_COOKIE'].split("=")
            #if self.config.pgdebug > 4:
            #    print("HTTP_COOKIE", self.cookie)

        self.method = ""
        if 'REQUEST_METHOD' in environ:
            self.method = environ['REQUEST_METHOD']
            #if self.config.pgdebug > 4:
            #    print("REQUEST_METHOD", self.method)

        self.request_org = ""
        self.request = {}
        if 'CONTENT_LENGTH' in environ:
            if self.method == 'POST':
                try:
                    content_length = int(environ['CONTENT_LENGTH']) # <--- Gets the size of data
                    #print("content_length", content_length) # <--- Gets the data itself
                    self.request_org = environ['wsgi.input'].read(content_length).decode()
                    #print("Request_org", self.request_org)
                    self.request = parse_qsl(str(self.request_org), keep_blank_values=True)
                    #if self.config.pgdebug > 5:
                    #    print("Request", self.request)
                except:
                    print("No post data", sys.exc_info())
                    pass

        self.url = ""
        if 'PATH_INFO' in environ:
            self.url = environ['PATH_INFO']

        splitx = os.path.split(self.url)
        tmpname = self._assem_path(splitx)
        self.fn = Config.datapath +  tmpname
        #print("self.fn", self.fn)
        self.mtype = mimetypes.guess_type(self.fn)[0]
        if not self.mtype:
            self.mtype = "text/plain"
        self.urlmap = wsgi_global.urlmap

    def _translate_url(self, config, url):
        ''' return details for a url '''
        #print("Looking up", url)
        par = urlparse(url)
        got, tmpl, filen = self.urlmap.lookup(par.path)
        #print("Got ", got, tmpl, filen)
        return got, tmpl, filen

    # --------------------------------------------------------------------
    #  Dynamic content - overrides static

    def process_req(self):

        ''' This executes the request, after the initialize-r parsed everything '''

        import wsgi_content, wsgi_util

        #print("serving", self.url, self.fn)

        try:
            callme, tmpl, filen = self._translate_url(Config, self.url)
        except:
            wsgi_util.put_exception("call proj entry")

        if(callme):
            content = ""
            try:
                #print("Callback",  self.fn, self.url)
                content = callme(Config, self.url, self.query, self.request, tmpl, filen)
            except:
                wsgi_util.put_exception("At process_req " + str(filen))
                self.respond('500 Internal Server Error', [('Content-Type', "text/html" + ';charset=UTF-8')])

                fn5 = Config.datapath + os.sep + "html/500.html"
                if os.path.exists(fn5):
                    content = wsgi_content.got_500(Config, fn5, self.query)
                else:
                    content = "Empty results from page assembly."
                return [bytes(content, "utf-8")]

            self.respond('200 OK', [('Content-Type', "text/html" + ';charset=UTF-8')])
            return [bytes(content, "utf-8")]

        # Static content
        else:
            found_file = ""
            while 1:
                if os.path.exists(self.fn):
                    found_file = self.fn
                    break
                fn2 = self._pad_path(self.fn, "static")
                if os.path.exists(fn2):
                    found_file = fn2
                    break
                fn2 = self._pad_path(self.fn, "html")
                if os.path.exists(fn2):
                    found_file = fn2
                    break
                break

            #print("found_file", found_file)
            if found_file:
                self.mtype = mimetypes.guess_type(found_file)[0]
                if not self.mtype:
                    self.mtype = "text/plain"
                self.respond('200 OK', [('Content-Type', self.mtype + ';charset=UTF-8')])
                fp = util.FileWrapper(open(found_file, "rb"))
                return fp

            else:       # Error content
                self.respond('404 Not Found', [('Content-Type', 'text/html;charset=UTF-8')])
                fn4 = Config.datapath + os.sep + "html/404.html"
                if os.path.exists(fn4):
                    content = wsgi_content.got_404(Config, fn4, self.query)
                    return [bytes(content, "utf-8")]
                else:
                    return [b"URL not found. (and 404 file does not exist)."]

    def _assem_path(self, splitx):
        #print("splitx", splitx)
        ppp = ""
        for aa in range(len(splitx)):
            #print("re-assemble", splitx[aa])
            if aa == len(splitx)-1:
                # Empty last file name, index wanted
                if splitx[aa] == "":
                    ppp = os.path.join(ppp, "/index.html")
                else:
                    ppp = os.path.join(ppp, splitx[aa])
            else:
                ppp = os.path.join(ppp, splitx[aa])
        #print("ppp", ppp)
        return ppp

    def _pad_path(self, fnorg, padname):
        ''' inject last dirname '''
        splitx = os.path.split(fnorg)
        #print("splitx", splitx)
        ppp = ""
        for aa in range(len(splitx)):
            #print("re-assemble", splitx[aa])
            if aa == len(splitx)-1:
                ppp = os.path.join(ppp, padname)
            ppp = os.path.join(ppp, splitx[aa])
        #print("ppp", ppp)
        return ppp

usr_cnt = 0
mainclass = None

# ------------------------------------------------------------------------
# WSGI main entry point

def application(environ, respond):

    '''
    WSGI main entry point. The web server (like apache) will call this.
    '''

    #print("Started:", environ['PATH_INFO'])

    try:
        # Make sure we are landing here
        mypath = os.path.dirname(os.path.realpath(__file__));
        sys.path.append(mypath)
        sys.path.append(mypath + os.sep + "common")
        os.chdir(mypath + os.sep + "content");
        sys.path.append(mypath + os.sep + "content")

        import wsgi_util, wsgi_content, wsgi_global, wsgi_conf

        #wsgi_util.append_file("Started Server Page\n")

        global myconf
        Config.pgdebug = myconf.pgdebug
        Config.verbose = myconf.verbose
        global usr_cnt, mainclass


        usr_cnt += 1
        #print("Query arrived", os.getpid(), usr_cnt)
        # if not mainclass:
        try:
            mainclass = xWebServer(environ, respond)
        except:
            wsgi_util.put_exception("Creating Server OBJ")

        # Only do it one time (not for dev deployment)
        if True: #usr_cnt == 1:
            try:
                wsgi_global.getprojects(mainclass)
            except:
                wsgi_util.put_exception("Loading Projects")

        wdata = mainclass.process_req()
        #print("tdelta", "%.4f" % ( (time.perf_counter() - mainclass.mark) * 1000), "ms")
        return wdata

    except:
        #print("Exception in main:", sys.exc_info())
        tracex("Exception in main:")
        content = "Script error"
        return [bytes(content, "utf-8"),]

def xversion():
    print("Version 1.0")
    #sys.exit(0)

def xhelp():
    print("Helping 1.0")
    #sys.exit(0)

# ------------------------------------------------------------------------

if __name__ == '__main__':

    opts = []; args = []

    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h?vV:fxctoktp:",
                        ["debug=", "help", "help", "verbose", "version", ])

    except getopt.GetoptError as err:
        print(_("Invalid option(s) on command line:"), err)
        sys.exit(1)

    # Outdated parsing ... for now, leave it as is
    for aa in opts:
        #print("opt", "'" + aa[0] + "'", aa[1])
        if aa[0] == "-d" or aa[0] == "--debug":
            try:
                myconf.pgdebug = int(aa[1])
                #print( _("Running at debug level:"),  Config.pgdebug)
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
            myconf.verbose = 1
        if aa[0] == "-f":
            myconf.full_screen = True
        if aa[0] == "-x":
            CLEAR_CONFIG = True
        if aa[0] == "-c":
            SHOW_CONFIG = True
        if aa[0] == "-t":
            SHOW_TIMING = True
        if aa[0] == "-o":
            USE_STDOUT = True
        if aa[0] == "-k":
            myconf.show_keys = True
        if aa[0] == "-t":
            print("Tracing ON")
            sys.settrace(tracer)

    print("\n===== Starting HTTPD on port {}, control-C to stop".format(myconf.port))

    class NoLoggingWSGIRequestHandler(simple_server.WSGIRequestHandler):

        ''' Override parent's logging '''

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