#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time
import multiprocessing
from urllib.parse import urlparse, unquote, parse_qs
from wsgiref import simple_server, util

#mypath = ""
urlmap = None

def     translate_url(url):

    global mypath

    par = urlparse(url)
    #print(par)
    #url2 =  par.path[len(mypath):]
    #print("Looking up", url)
    return urlmap.lookup(url)

# ------------------------------------------------------------------------
# WSGI main entry point

def application(environ, respond):

    global urlmap, mypath, query, config

    # Make sure we are landing here
    mypath = os.path.dirname(os.path.realpath(__file__));
    sys.path.append(mypath)
    os.chdir(mypath)

    import wsgi_util, wsgi_content

    config = Config()
    config.mypath = mypath

    # URL to function table
    urlmap =  wsgi_util.UrlMap()
    wsgi_content.reg_all(urlmap)

    #print("pwd", os.getcwd());
    #print("Starting in pwd", os.getcwd())
    #print("mypath", mypath)
    #printenv(environ)

    print("-----------------------------------------------")
    #print("query_string", environ['QUERY_STRING'])
    #print("path_info", environ['PATH_INFO'])

    query = parse_qs(environ['QUERY_STRING'], keep_blank_values=True)
    #print("query", query)

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

    #print("table", urlmap.urls)

    fn2 = mypath + os.sep + fn
    type = mimetypes.guess_type(fn2)[0]
    if not type:
        type = "text/plain"

    #  Dynamic content - overrides static
    callme = translate_url(fn)
    if(callme):
        respond('200 OK', [('Content-Type', "text/html" + ';charset=UTF-8')])
        content = callme(config, fn, query)
        if not content:
            content = "Empty results from page assembly."
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

    httpd = simple_server.make_server('', port, application)
    print("Serving {} on port {}, control-C to stop".format(mypath, port))

    while True:
        try:
            httpd.handle_request()
        except KeyboardInterrupt:
            print("Shutting down.")
            httpd.server_close()
            raise
            break
