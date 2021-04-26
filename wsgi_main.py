#!/usr/bin/env python3

''' The simplest web server '''

import sys, os, mimetypes, time, sqlite3
import multiprocessing
from urllib.parse import urlparse, unquote, parse_qs
from wsgiref import simple_server, util

class wsgiSql():

    def __init__(self, file, table = "initial"):

        self.table = table

        try:
            self.conn = sqlite3.connect(file)
        except:
            print("Cannot open/create db:", file, sys.exc_info())
            return
        try:
            self.c = self.conn.cursor()
            # Create table
            self.c.execute("create table if not exists " + self.table + "\
             (pri INTEGER PRIMARY KEY, key text, val text, val2 text, val3 text, val4 text)")
            self.c.execute("create index if not exists iconfig on " + self.table + " (key)")
            self.c.execute("create index if not exists pconfig on " + self.table + " (pri)")
            self.c.execute("PRAGMA synchronous=OFF")
            # Save (commit) the changes
            self.conn.commit()
        except:
            print("Cannot insert sql data", sys.exc_info())

        finally:
            # We close the cursor, we are done with it
            #c.close()
            pass

    # --------------------------------------------------------------------
    # Return None if no data

    def   get(self, kkk):
        try:
            if os.name == "nt":
                self.c.execute("select * from " + self.table + " where key = ?", (kkk,))
            else:
                self.c.execute("select * from " + self.table + " indexed by iconfig where key = ?", (kkk,))
            rr = self.c.fetchone()
        except:
            print("Cannot get sql data", sys.exc_info())
            rr = None
        finally:
            pass
        if rr:
            return rr[1:]
        else:
            return None

    # --------------------------------------------------------------------
    # Return False if cannot put data

    def   put(self, key, val, val2, val3, val4):

        #got_clock = time.clock()

        ret = True
        try:
            if os.name == "nt":
                self.c.execute("select * from " + self.table + " where key == ?", (key,))
            else:
                self.c.execute("select * from " + self.table + " indexed by iconfig where key == ?", (key,))
            rr = self.c.fetchall()
            if rr == []:
                #print( "inserting")
                self.c.execute("insert into " + self.table + " (key, val, val2, val3, val4) values (?, ?, ?, ?, ?)", (key, val, val2, val3, val4))
            else:

                #print ("updating")
                if os.name == "nt":
                    self.c.execute("update " + self.table + " set val = ?, val2 = ?, val3 = ?, val4 = ? where key = ?",\
                                     (val, val2, val3, val4, key))
                else:
                    self.c.execute("update " + self.table + " indexed by iconfig set val = ?, val2 = ?, val3 = ?, val4 = ? where key = ?",\
                                     (val, val2, val3, val4, key))
            self.conn.commit()
        except:
            print("Cannot put sql data", sys.exc_info())
            ret = False
        finally:
            #c.close
            pass

        #self.take += time.clock() - got_clock

        return ret

    # --------------------------------------------------------------------
    # Get All

    def   getall(self):
        try:
            self.c.execute("select * from " + self.table + "")
            rr = self.c.fetchall()
        except:
            print("Cannot get sql data", sys.exc_info())
        finally:
            #c.close
            pass
        return rr

    # --------------------------------------------------------------------
    # Return None if no data

    def   rmall(self):
        print("removing all")
        try:
            self.c.execute("delete from " + self.table + "")
            rr = self.c.fetchone()
        except:
            print("Cannot delete sql data", sys.exc_info())
        finally:
            pass
        if rr:
            return rr[1]
        else:
            return None

# ------------------------------------------------------------------------
# Parameters are going around with this one

class Config():
    def __init(self):
        self.mypath = ""
        self.server = None
        self.mainclass = None

# ------------------------------------------------------------------------
# Endow this class with all the info a page would need to complete

class xWebServer():


    def __init__(self, environ, respond):

        import wsgi_global, wsgi_content, wsgi_util

        self.respond = respond
        self.environ = environ
        self.config = Config()
        self.config.mainclass = self
        self.config.mypath = os.path.dirname(os.path.realpath(__file__));
        self.config.verbose = 0
        self.sql = wsgiSql("data/wsgi_main.sqlt")

        #self.sql.put("kkk", "aa", "bb", "cc", "dd")
        #print(self.sql.get("kkk"))

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
                print("content_length", content_length) # <--- Gets the data itself
                self.request = environ['wsgi.input'].read(content_length)
                print("Request", self.request )
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

        # Add default enties to table
        wsgi_global.add_one_url("/", wsgi_content.got_index)
        wsgi_global.add_one_url("/index.html", wsgi_content.got_index)
        self.urlmap = wsgi_global.urlmap

    def _translate_url(self, config, url):
        #print("Looking up", url)
        par = urlparse(url)
        got = self.urlmap.lookup(par.path)
        return got

    # --------------------------------------------------------------------
    #  Dynamic content - overrides static

    def process_req(self):

        import wsgi_content, wsgi_util

        #print("serving", self.url, self.fn)
        callme = self._translate_url(self.config, self.url)
        if(callme):
            content = ""
            try:
                #print("Callback",  self.fn, self.url)
                content = callme(self.config, self.url, self.query)
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

    # Make sure we are landing here
    mypath = os.path.dirname(os.path.realpath(__file__));
    os.chdir(mypath); sys.path.append(mypath)

    import wsgi_util, wsgi_content, wsgi_global

    mainclass = xWebServer(environ, respond)
    err = wsgi_global.getprojects()
    return mainclass.process_req()

# ------------------------------------------------------------------------

class NoLoggingWSGIRequestHandler(simple_server.WSGIRequestHandler):
    def log_message(self, format, *args):
        # Do just a little bit of logging
        if "siteicons" not in args[0] and "media" not in args[0]:
            print(args[0])
        pass

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
