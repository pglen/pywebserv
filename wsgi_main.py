#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time
import multiprocessing
from urllib.parse import urlparse, unquote, parse_qs
from wsgiref import simple_server, util

config = None

class NoLoggingWSGIRequestHandler(simple_server.WSGIRequestHandler):
    def log_message(self, format, *args):
        # Do just a little bit of logging
        if "siteicons" not in args[0] and "media" not in args[0]:
            print(args[0])
        pass

# ------------------------------------------------------------------------

class Config():
    def __init(self):
        self.mypath = ""
        self.server = None

# ------------------------------------------------------------------------
# Endow this class with all the info a page would need to complete

class xWebServer():

    def __init__(self, environ, respond):

        import wsgi_util, wsgi_content, wsgi_style, wsgi_global

        #wsgi_util.printenv(environ, True)

        self.mypath = os.path.dirname(os.path.realpath(__file__));
        sys.path.append(self.mypath)

        # Make sure we are landing here
        os.chdir(self.mypath)
        #print("Loaded in ", self.mypath)
        self.query = parse_qs(environ['QUERY_STRING'], keep_blank_values=True)

        if(self.query):
            print("Query", self.query)

        if "POST" in environ['REQUEST_METHOD']:
            try:
                content_length = int(environ['CONTENT_LENGTH']) # <--- Gets the size of data
                print("content_length", content_length) # <--- Gets the data itself
                #print(environ['wsgi.version'])
                self.request = environ['wsgi.input'].read(content_length)
                print("Request", self.request )
            except:
                print("No post data", sys.exc_info())
                pass

        self.url = environ['PATH_INFO']
        splitx = os.path.split(self.url)
        tmpname = self.assem_path(splitx)
        #print("tmpname", tmpname, "self.mypath", self.mypath)
        self.fn = self.mypath +  tmpname
        #print("self.fn", self.fn)
        self.mtype = mimetypes.guess_type(self.fn)[0]
        if not self.mtype:
            self.mtype = "text/plain"

        # Add default enties to table
        wsgi_global.add_one_url("/", wsgi_content.got_index)
        wsgi_global.add_one_url("/index.html", wsgi_content.got_index)
        self.urlmap = wsgi_global.urlmap

    def translate_url(self, config, url):
        #print("Looking up", url)
        par = urlparse(url)
        got = self.urlmap.lookup(par.path)
        return got

    def assem_path(self, splitx):
        ppp = ""
        for aa in range(len(splitx)):
            #print("re-assemble", splitx[aa])
            if aa == len(splitx)-1:
                # Empty last file name, index wanted
                if splitx[aa] == "":
                    ppp = os.path.join(ppp, "/index.html")
                else:
                    if splitx[aa] != os.sep:
                        ppp = os.path.join(ppp, splitx[aa])
            else:
                if splitx[aa] != os.sep:
                    ppp = os.path.join(ppp, splitx[aa])
        return ppp

# ------------------------------------------------------------------------
# WSGI main entry point

def application(environ, respond):

    import wsgi_util, wsgi_content, wsgi_style, wsgi_global

    config = Config()
    mainclass = xWebServer(environ, respond)

    config.mypath = mainclass.mypath
    config.mainclass = mainclass

    #print("translated: ",  mainclass.fn)

    #  Dynamic content - overrides static
    callme = mainclass.translate_url(config, mainclass.url)

    if(callme):
        content = ""
        try:
            print("Attemp callback",  mainclass.fn, mainclass.url)
            content = callme(config, mainclass.url, mainclass.query)
        except:
            print("exc from translate url", sys.exc_info())
            wsgi_util.put_exception("tr url")
            respond('500 Internal Server Error', [('Content-Type', "text/html" + ';charset=UTF-8')])

            fn5 = mainclass.mypath + os.sep + "500.html"
            if os.path.exists(fn5):
                content = wsgi_content.got_500(config, "500.html", mainclass.query)
            else:
                content = "Empty results from page assembly."
            return [bytes(content, "utf-8")]

        respond('200 OK', [('Content-Type', "text/html" + ';charset=UTF-8')])
        return [bytes(content, "utf-8")]

    # Static content
    elif os.path.exists(mainclass.fn):
        respond('200 OK', [('Content-Type', mainclass.mtype + ';charset=UTF-8')])
        fp = util.FileWrapper(open(mainclass.fn, "rb"))
        return fp
    # Error content
    else:
        respond('404 Not Found', [('Content-Type', 'text/html;charset=UTF-8')])
        fn4 = mainclass.mypath + os.sep + "404.html"
        if os.path.exists(fn4):
            content = wsgi_content.got_404(config, "404.html", mainclass.query)
            return [bytes(content, "utf-8")]
        else:
            return [b"URL not found and 404 file does not exist."]

# ------------------------------------------------------------------------

if __name__ == '__main__':

    #print("Args", sys.argv)

    mypath = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    httpd = simple_server.make_server('', port, application, handler_class=NoLoggingWSGIRequestHandler)

    print("Serving {} on port {}, control-C to stop".format(mypath, port))

    while True:
        try:
            httpd.handle_request()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()
            raise
            break
