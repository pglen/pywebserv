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

def     translate_url(config, url, urlmap):
    #print("Looking up", url)
    par = urlparse(url)
    got = urlmap.lookup(par.path)
    return got

# ------------------------------------------------------------------------
# WSGI main entry point

def application(environ, respond):

    global mypath, query, config

    # Make sure we are landing here
    mypath = os.path.dirname(os.path.realpath(__file__));
    sys.path.append(mypath)
    os.chdir(mypath)

    import wsgi_util, wsgi_content, wsgi_style, wsgi_global

    wsgi_global.add_one_url("/index.html", wsgi_content.got_index)

    config = Config()
    config.mypath = mypath

    #print("pwd", os.getcwd());
    #print("Starting in pwd", os.getcwd())

    #'''print("mypath", mypath)

    #print("-----------------------------------------------")
    #print("query_string", environ['QUERY_STRING'])
    #print("path_info", environ['PATH_INFO'])

    query = parse_qs(environ['QUERY_STRING'], keep_blank_values=True)
    if(query):
        print("query", query)

    if "POST" in environ['REQUEST_METHOD']:
        try:
            content_length = int(environ['CONTENT_LENGTH']) # <--- Gets the size of data
            print("content_length", content_length)
            print(environ['wsgi.version'])
            sub = environ['wsgi.input'].read(content_length)
            print("sub", sub)

            #post_data = environ[sys.stdin.read(10) # <--- Gets the data itself
            #print("post_data", post_data)
            #wsgi_util.printenv(environ)

        except:
            print("No post data", sys.exc_info())
            pass

    splitx = os.path.split(environ['PATH_INFO'])
    fn = ""
    for aa in range(len(splitx)):
        #print("re-assemble", splitx[aa])
        if aa == len(splitx)-1:
            # Empty file name, index wanted
            if splitx[aa] == "":
                fn += os.sep + "index.html"
            else:
                if splitx[aa] != os.sep:
                    fn += os.sep + splitx[aa]
        else:
            if splitx[aa] != os.sep:
                fn += os.sep + splitx[aa]

    fn2 = mypath + os.sep + fn
    type = mimetypes.guess_type(fn2)[0]
    if not type:
        type = "text/plain"

    #print(fn2)

    #  Dynamic content - overrides static
    callme = translate_url(config, fn, wsgi_global.urlmap)
    if(callme):
        content = ""
        try:
            content = callme(config, fn, query)
        except:
            print("exc from translate url", sys.exc_info())
            respond('500 Internal Server Error', [('Content-Type', "text/html" + ';charset=UTF-8')])

            fn5 = mypath + os.sep + "500.html"
            if os.path.exists(fn5):
                content = wsgi_content.got_500(config, "500.html", query)
            else:
                content = "Empty results from page assembly."
            return [bytes(content, "utf-8")]

        respond('200 OK', [('Content-Type', "text/html" + ';charset=UTF-8')])
        return [bytes(content, "utf-8")]

    # Static content
    elif os.path.exists(fn2):
        respond('200 OK', [('Content-Type', type + ';charset=UTF-8')])
        fp = util.FileWrapper(open(fn2, "rb"))
        return fp
    # Error content
    else:
        respond('404 Not Found', [('Content-Type', 'text/html;charset=UTF-8')])
        fn4 = mypath + os.sep + "404.html"
        if os.path.exists(fn4):
            content = wsgi_content.got_404(config, "404.html", query)
            return [bytes(content, "utf-8")]
        else:
            return [b"URL not found and 404 file does not exist."]

class Config():
    def __init(self):
        self.mypath = ""

# ------------------------------------------------------------------------

if __name__ == '__main__':

    #print("Args", sys.argv)
    global mypath

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
