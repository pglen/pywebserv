#!/usr/bin/env python3

''' The simplest web server. This directory is at the root
of the web server, and sub directories may assume the following functions:

    data            for database related
    siteicons       icond for this site
    media           images, media
    static          files that may be presented as is
    projects        python files that make up the site

  To create a <b>new page</b>, add a new python file, and call the
URL registration function and macro registration function.

  add_one_url("/", got_index, "index.html")

 To create a new 'macro' use the add function with the macro name
and the name of the function that is executed by the macro. The macro
will be replaced by the return value of the function. The macro syntax
is created by surrounding braces wit a space. Like: { macro }

 add_one_func("mymacro", my_img_func)

 Builtin macros:

 { image }          --  Put an image tag in the output
 { image www }      --  Put an image tag in the output, resize width to requested
 { image www hhh }  --  Put an image tag in the output, resize to parm

The first two forms of the { image } function will preserve the image's aspect ratio.

'''

import sys, os, mimetypes, time, sqlite3
import multiprocessing
from urllib.parse import urlparse, unquote, parse_qs
from wsgiref import simple_server, util

# ------------------------------------------------------------------------

class Config():

    '''
    Parameters are going around with this class
    '''

    def __init(self):
        self.mypath = ""
        self.server = None
        self.mainclass = None


class xWebServer():
    '''
     This class has all the info a page would need. Add
     urls and functions to complete the reply.
    '''
    def __init__(self, environ, respond):

        ''' Deocrate the class instance with data from the environment '''

        # import here so apache wsgi interface gets the files
        import wsgi_global, wsgi_content, wsgi_util, wsgi_data

        self.respond = respond
        self.environ = environ
        self.config = Config()
        self.config.mainclass = self
        self.config.mypath = os.path.dirname(os.path.realpath(__file__));
        self.config.verbose = 0
        self.sql = wsgi_data.wsgiSql("data/wsgi_main.sqlt")

        #wsgi_util.printenv(environ, True)
        #print(environ['wsgi.version'])
        #print("Loaded in ", self.mypath)

        self.request = ""
        self.query = parse_qs(environ['QUERY_STRING'], keep_blank_values=True)
        #print("Query", self.query)

        self.method = environ['REQUEST_METHOD']
        #print("REQUEST_METHOD", self.method)

        if "POST" in self.method:
            try:
                content_length = int(environ['CONTENT_LENGTH']) # <--- Gets the size of data
                #print("content_length", content_length) # <--- Gets the data itself
                self.request_org = environ['wsgi.input'].read(content_length)
                #print("Request", self.request_org)
                self.request = parse_qs(self.request_org, keep_blank_values=True)
                print("Request", self.request)
            except:
                print("No post data", sys.exc_info())
                pass

        self.url = environ['PATH_INFO']
        splitx = os.path.split(self.url)
        tmpname = self._assem_path(splitx)
        self.fn = self.config.mypath +  tmpname
        #print("self.fn", self.fn)
        self.mtype = mimetypes.guess_type(self.fn)[0]
        if not self.mtype:
            self.mtype = "text/plain"
        self.urlmap = wsgi_global.urlmap

    def _translate_url(self, config, url):
        #print("Looking up", url)
        par = urlparse(url)
        got, tmpl = self.urlmap.lookup(par.path)
        return got, tmpl

    # --------------------------------------------------------------------
    #  Dynamic content - overrides static

    def process_req(self):

        ''' This executes the request, after the initilizer parsed everything '''

        import wsgi_content, wsgi_util

        #print("serving", self.url, self.fn)
        callme, tmpl = self._translate_url(self.config, self.url)
        if(callme):
            content = ""
            try:
                #print("Callback",  self.fn, self.url)
                content = callme(self.config, self.url, self.query, tmpl)
            except:
                wsgi_util.put_exception("translate url")
                self.respond('500 Internal Server Error', [('Content-Type', "text/html" + ';charset=UTF-8')])

                fn5 = self.config.mypath + os.sep + "html/500.html"
                if os.path.exists(fn5):
                    content = wsgi_content.got_500(self.config, "html/500.html", self.query)
                else:
                    content = "Empty results from page assembly."
                return [bytes(content, "utf-8")]

            self.respond('200 OK', [('Content-Type', "text/html" + ';charset=UTF-8')])
            return [bytes(content, "utf-8")]

        # Static content
        else:
            found_file = ""
            if os.path.exists(self.fn):
                found_file = self.fn
            else:
                fn2 = self._pad_path(self.fn, "/html")
                #print("fn2", fn2)
                if os.path.exists(fn2):
                    found_file = fn2

            if found_file:
                self.respond('200 OK', [('Content-Type', self.mtype + ';charset=UTF-8')])
                fp = util.FileWrapper(open(self.fn, "rb"))
                return fp
            else:       # Error content
                self.respond('404 Not Found', [('Content-Type', 'text/html;charset=UTF-8')])
                fn4 = self.config.mypath + os.sep + "html/404.html"
                if os.path.exists(fn4):
                    content = wsgi_content.got_404(self.config, "html/404.html", self.query)
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

    def _pad_path(self, splitx, padname):
        #print("splitx", splitx)
        ppp = ""
        for aa in range(len(splitx)):
            #print("re-assemble", splitx[aa])
            if aa == len(splitx)-1:
                ppp = os.path.join(ppp, padname)
            ppp = os.path.join(ppp, splitx[aa])

        #print("ppp", ppp)
        return ppp

# ------------------------------------------------------------------------
# WSGI main entry point

def application(environ, respond):

    '''
    WSGI main entry point. The web server (like apache)
    will call this.
    '''
    # Make sure we are landing here
    mypath = os.path.dirname(os.path.realpath(__file__));
    os.chdir(mypath); sys.path.append(mypath)

    import wsgi_util, wsgi_content, wsgi_global

    mainclass = xWebServer(environ, respond)
    err = wsgi_global.getprojects()
    return mainclass.process_req()

# ------------------------------------------------------------------------


if __name__ == '__main__':

    class NoLoggingWSGIRequestHandler(simple_server.WSGIRequestHandler):

        ''' Override parent's logging '''

        def log_message(self, format, *args):
            # Do just a little bit of logging
            if "siteicons" not in args[0] and "media" not in args[0]:
                print(args[0])
            pass
        #print("Args", sys.argv)

    mypath = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000
    httpd = simple_server.make_server('', port, application, handler_class=NoLoggingWSGIRequestHandler)
    print("HTTPD {} on port {}, control-C to stop".format(mypath, port))

    while True:
        try:
            httpd.handle_request()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()
            raise
            break
