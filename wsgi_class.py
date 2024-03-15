#!/usr/bin/env python3

'''

    Main server class. This is executed from both the command line and
    the apache run time. The imports are scattered a little, because the
    apache run time does not know where the modules are. So when we include a
    module in a later stage, the module has been told where it is at.
    (like the 'common' subdir)

'''

import sys, os, mimetypes, time, datetime, getopt, traceback, uuid

try:
    from urllib.parse import urlparse, unquote, parse_qs, parse_qsl
except ImportError:
     from urlparse import urlparse, unquote, parse_qs, parse_qsl

from wsgiref import simple_server, util

#from common import wsgi_util


class xWebServer():

    '''!
     This class has all the info we would need for page generation. Add urls and functions
     to complete the reply. The return value of the process_request function is the
     output to the client.
    '''

    def __init__(self, environ, respond):

        '''! Decorate the class instance with data from the environment '''

        # import here so apache wsgi interface gets the files
        import wsgi_global, wsgi_content, wsgi_util
        import wsgi_data, wsgi_func, wsgi_parse, wsgi_conf

        self.server_time_mark = time.perf_counter()
        #wsgi_util.printenv(environ)

        self.start_time = datetime.datetime.now()

        # Create initial
        self.configx = wsgi_conf.Configx()
        self.configx.mypath = os.path.dirname(os.path.realpath(__file__)) + os.sep
        self.configx.datapath =  self.configx.mypath + "content" + os.sep

        if self.configx.pgdebug > 1:
            print("self.configx.mypath", self.configx.mypath)
            print("self.configx.datapath", self.configx.datapath)

        if self.configx.pgdebug > 2:
           print(self.configx.getvals())

        logd = self.configx.datapath + "data"
        if not os.access(logd, os.X_OK):
            os.mkdir(logd)
        logf = self.configx.datapath + "data/wsgi_main.log"
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
                print(str(self.start_time), *sss, file=self.logfp, flush=True)

            #print( str(self.start_time), environ, file=self.logfp, flush=True)

        #print("env ver", environ['wsgi.version'] )

        #print("Loaded in ", self.mypath)
        #wsgi_util.print_httpenv(environ)
        #wsgi_util.printenv(environ)

        wsgi_func.build_initial_table()
        wsgi_func.build_initial_rc()

        self.good_cookies = {}
        self.wanted_cookies = []    # This will be sent to the server

    def parse_instance(self, environ, respond):

        import wsgi_util
        #wsgi_util.printenv(environ)

        self.query = ""
        if 'QUERY_STRING' in environ:
            self.query = parse_qs(environ['QUERY_STRING'], keep_blank_values=True)
            if self.configx.pgdebug > 2:
                if self.query:
                    print("QUERY_STRING", self.query)

        self.cookie = ""
        self.remote = ""

        if 'REMOTE_HOST' in environ:
            self.remote = environ['REMOTE_HOST']

        if 'HTTP_COOKIE' in environ:
            self.cookie = environ['HTTP_COOKIE']
            if self.configx.pgdebug > 4:
                if environ['PATH_INFO'][-1:] == "/":
                    print("HTTP_COOKIE:", self.cookie)
                    #self.cookie += "a"

            for aa in self.cookie.split(";"):
                #print("cookie:", aa)
                bb = aa.split("=", 1)
                # This is where we decode the encrypted cookie
                import wsgi_util
                rrr = wsgi_util.decode_cookie_header(bb[0], bb[1])
                #print("decoded cookie", rrr[0], rrr[1])
                if "-Damaged" in rrr[0] :
                    self.good_cookies.update( ((bb[0], bb[1]),) )
                else:
                    self.good_cookies.update( ((rrr[0], rrr[1]),) )

            if self.configx.verbose > 1:
                if environ['PATH_INFO'][-1:] == "/":
                    print("good cookies", self.good_cookies)
            if self.configx.verbose > 2:
                    print("good cookies", self.good_cookies)

        self.method = ""
        if 'REQUEST_METHOD' in environ:
            self.method = environ['REQUEST_METHOD']
            if self.configx.pgdebug > 4:
                print("REQUEST_METHOD", self.method)

        self.request_org = ""
        self.request = []
        if 'CONTENT_LENGTH' in environ:
            if self.method == 'POST':
                import wsgi_cgi
                self.request = wsgi_cgi.parse_cgi(environ, self.configx)

        self.url = ""
        if 'PATH_INFO' in environ:
            self.url = environ['PATH_INFO']

        if self.configx.verbose:
            print("self.url", self.url)

        splitx = os.path.split(self.url)
        #splitx = self.url.split(os.sep)

        tmpname = self._assem_path(splitx)
        self.fn = self.configx.datapath +  tmpname
        self.fn = os.path.normpath(self.fn)

        #print("self.fn", self.fn)
        self.mtype = mimetypes.guess_type(self.fn)[0]
        if not self.mtype:
            self.mtype = "text/plain"

    def _translate_url(self, config, url):

        '''! return details for a url '''

        import wsgi_global
        #import wsgi_content, wsgi_util

        #print("Looking up", url)
        par = urlparse(url)

        if self.configx.verbose > 2:
            print("Translate_url from:", par.path)

        got, tmpl, filen = wsgi_global.urlmap.lookup(par.path)

        if self.configx.verbose > 2:
            print( "Got:", got, tmpl, filen)

        # Patch for dir if no extension
        #print("splitext", os.path.splitext(url)[1])
        # if it does not end in '/'
        #if not os.path.splitext(url)[1] and url[len(url)-1] != '/':
        #    url += '/'
        #    print("Looking up url second pass", url)
        #    for aa in self.urls:
        #        #print("src url", aa[0], aa[1])
        #        if aa[0] == url:
        #            return aa[1] + '/', aa[2], aa[3]


        return got, tmpl, filen

    def make_headers(self, mtype, minutes):

        dt = datetime.datetime.utcnow() + datetime.timedelta(minutes=minutes)
        fdt = dt.strftime('%a, %d %b %Y %H:%M:%S GMT')

        headers =  [
                    ('Content-Type', mtype + ';charset=UTF-8'),
                    ('Expires', '%s' % fdt),
                    ]

        #print("Headers", headers)

        for aa in self.wanted_cookies:
            #print("setting cookie", aa)
            import wsgi_util
            ccc = wsgi_util.set_cookie_header(aa[0], aa[1], aa[2])
            headers.append(ccc)
        #print("headers", headers)

        self.wanted_cookies = []
        return headers

    # --------------------------------------------------------------------
    #  Dynamic content - overrides static

    def process_request(self, request, respond):

        '''!
            This executes the request, after the main initializer
            parsed everything
        '''

        import wsgi_global, wsgi_content, wsgi_util

        #respond('200 OK', [('Content-Type', "text/html" + ';charset=UTF-8')])
        #return [bytes("Cannot do shit", 'utf-8')]


        if self.configx.verbose > 2:
            print("process_request", self.url, self.fn)

        if self.configx.verbose > 3:
            print("url map:\n%s\n" % wsgi_global.urlmap.dump())

        try:
            callme, template, fname = self._translate_url(self.configx, self.url)
        except:
            wsgi_util.put_exception("When calling proj entry")
            return

        import wsgi_conf
        self.carrydef = wsgi_conf.CarryOn(self)
        self.carrydef.template = template
        self.carrydef.fname = fname
        self.carrydef.url = self.url
        self.carrydef.query = self.query
        self.carrydef.request = self.request
        self.carrydef.template = template
        self.carrydef.fname = fname

        #got_session = 0
        #for aa in self.good_cookies:
        #    if "Session" in aa:
        #        #print("found good", aa)
        #        got_session = 1
        #
        #if not got_session:
        #    sess = str(uuid.uuid4())
        #    print("New Session:", sess)
        #    self.wanted_cookies.append(("Session", sess, 1))
        #    # Also create a matching data

        if "Session" not in self.good_cookies:
            import wsgi_data
            sess = str(uuid.uuid4())
            print("New Session:", sess, self.remote)
            # 5 minutes
            self.wanted_cookies.append(("Session", sess, 300))

        if self.configx.verbose > 2:
            print("process_request2", callme, template)

        if(callme):
            #import wsgi_conf
            content = ""
            # Per request carryon; carried around with object as a reference
            try:
                self.carryon = wsgi_conf.CarryOn(self)
                self.carryon.mypath = os.path.dirname(os.path.realpath(__file__)) + os.sep
                self.carryon.url = self.url
                self.carryon.query = self.query
                self.carryon.request = self.request
                self.carryon.template = template
                self.carryon.fname = fname

                if self.configx.pgdebug > 2:
                    print(self.carryon.getvals())

                #print("Callback",  self.fn, self.url)
                try:
                    content = callme(self.configx, self.carryon)
                    #raise
                except:
                    print("Error on callme")
                    wsgi_util.put_exception("render content")

                try:
                    pass
                    # See if residual anything
                    #if hasattr(self.carryon, "localdb"):
                    #    #print("exiting", self.carryon.localdb)
                    #    self.carryon.localdb.close()
                except:
                    print("Error on exit cleanup")

            except:
                wsgi_util.put_exception("At process_request" + str(fname))

                fn5 = self.configx.datapath + "html/500.html"
                if os.path.isfile(fn5):

                    content = wsgi_content.got_500(self.carrydef, fn5, self.query)
                    #print("got 500", content)
                else:
                    content = "Empty results from page assembly."

                respond('500 Internal Server Error', [('Content-Type', "text/html" + ';charset=UTF-8')])
                return [bytes(content, "utf-8")]

            if self.configx.verbose > 3:
                print("process_request4", callme, template)

            respond('200 OK', self.make_headers("text/html", 1))

            return [bytes(content, "utf-8")]

        else:
            # Iterate for other content
            if self.configx.verbose > 2:
                print("Looking for file", self.fn)

            found_file = ""
            while True:
                if os.path.isfile(self.fn):
                    found_file = self.fn
                    break

                rev = wsgi_global.urlmap.revlookup(self.url)
                popped = self._pop_path(self.url)
                #print("rev:", rev, "got popped:", popped,)
                if rev:
                    fn2 = rev[0] + popped
                    if os.path.isfile(fn2):
                        found_file = fn2
                        break

                fn2 = self._pad_path(self.fn, "static")
                if os.path.isfile(fn2):
                    found_file = fn2
                    break

                fn2 = self._pad_path(self.fn, "html")
                if os.path.isfile(fn2):
                    found_file = fn2
                    break

                fn2 = self.configx.datapath + os.sep + "css" + os.sep \
                                        + os.path.basename(self.url)
                if os.path.isfile(fn2):
                    found_file = fn2
                    break

                # No more items ..
                break

            if found_file:
                if self.configx.verbose > 2:
                    print("found_file", "'" + found_file + "'")

                self.mtype = mimetypes.guess_type(found_file)[0]
                if not self.mtype:
                    self.mtype = "text/plain"

                if os.path.isfile(found_file):
                    #print("responding with file")
                    respond('200 OK', self.make_headers(self.mtype, 1))

                    from wsgiref import util
                    fp = util.FileWrapper(open(found_file, "rb"))
                    return fp
                else:
                    #print("responding with data", found_file)
                    respond('500 Internal Server Error', [('Content-Type', "text/html" + ';charset=UTF-8')])
                    wsgi_util.put_exception("On opening file %s" % found_file)

                    return [bytes("Error on opening file", 'utf-8')]

            else:
                # Error content
                print("Cannot find file:",  "'" + os.path.basename(self.fn) + "'")
                print("Request was:",  "'" + self.url + "'")

                #if self.configx.verbose:
                #    print("No such file", "'" + self.fn + "'")
                respond('404 Not Found', [('Content-Type', 'text/html;charset=UTF-8')])
                #print("error select", self.url, fname)

                # Search for 404 file, allow project 404 to override
                errfile = ""
                while True:
                    fn4 =  os.path.dirname(self.fn) + os.sep + "404.html"
                    if os.path.isfile(fn4):
                        errfile = fn4
                        break
                    fn4 = self.configx.datapath +  "html/404.html"
                    if os.path.isfile(fn4):
                        errfile = fn4
                        break
                    break

                if errfile:
                    import wsgi_conf
                    content  = wsgi_content.got_404(self.carrydef, errfile, self.query, self.fn)
                    return [bytes(content, "utf-8")]
                else:
                    return [b"URL not found. (and 404 file does not exist)."]

    # Parse and re-assemble pats
    def _assem_path(self, splitx):
        #print("assem_path: splitx", splitx)
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

    # Pad path with an injected name
    def _pad_path(self, fnorg, padname):
        '''! inject last dirname '''
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

    # Pop the top off the path
    def _pop_path(self, pname):
        '''! pop path head '''
        splitx = pname.split(os.sep)
        #print("splitx", splitx)
        ppp = ""
        for aa in range(len(splitx)):
            #print("re-assemble", splitx[aa])
            if aa == 1:
                pass
            else:
                ppp += splitx[aa]
                if  aa != len(splitx)-1:
                    ppp+= os.sep

        #print("pop_path: pname", pname, "ppp", ppp)
        return ppp

# hashx signature: 0xc0be5309

