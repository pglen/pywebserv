#!/usr/bin/env python3

'''

    Small wsgiref based web server. Takes a path to serve from and an
    optional port number (defaults to 8000), then tries to serve files.

    Mime types are guessed from the file names, 404 errors are raised
    if the file is not found. Used for the make serve target in Doc.

    Restarts if any of the files in current dir changed and project dir
    changed; calls the bringfocus batch job to refresh browser

'''

import sys, os, time
import mimetypes, subprocess

from wsgiref import simple_server, util

def app(environ, respond):

    fn = os.path.join(path, environ['PATH_INFO'][1:])
    if '.' not in fn.split(os.path.sep)[-1]:
        fn = os.path.join(fn, 'index.html')
    type = mimetypes.guess_type(fn)[0]

    if os.path.exists(fn):
        respond('200 OK', [('Content-Type', type)])
        return util.FileWrapper(open(fn, "rb"))
    else:
        respond('404 Not Found', [('Content-Type', 'text/plain')])
        #respond('200 Hello world', [('Content-Type', 'text/plain')])
        return [b'not found']
        #return "Hello World"

def serve():
        httpd = simple_server.make_server('', port, app)
        print("Serving {} on port {}, control-C to stop".format(path, port))
        while True:
            try:
                httpd.handle_request()
            except KeyboardInterrupt:
                print("Shutting down.")
                httpd.server_close()
                raise
                break

def re_open():
    #th = subprocess.Popen(["firefox", "localhost:8000"], close_fds=True)
    #th = subprocess.Popen(["xvkbd", "-window", "Firefox", "-text", "\Cr"])
    th = subprocess.Popen(["./bringfocus.sh"], shell=True)
    #return th
    pass

def re_serve():
    th = subprocess.Popen(["/usr/bin/env", "python", "wsgi_main.py"] + sys.argv[1:])
    return th

def waitx():
    time.sleep(.1)

def append_file(nnn):
    global fnamearr, statarr

    if os.path.isfile(nnn):
        fff = os.stat(nnn).st_mtime
        fnamearr.append(nnn)
        statarr.append(fff)

# ------------------------------------------------------------------------
# Scan all files in one deep directory

def  rescan():
    global fnamearr, statarr

    fnamearr = []; statarr = []
    fnamearr2a = os.listdir()
    #print("fnamearr2a", fnamearr2a)

    for aaa in fnamearr2a:
        if os.path.isdir(aaa):
            # No need for these files
            if "__" in aaa:
                continue
            if ".git" in aaa:
                continue
            if "data" in aaa:
                continue
            _rescan(aaa)
        if os.path.isfile(aaa):
             append_file(aaa)
    #print("fnamearr", fnamearr)

def _rescan(dirx):
    fnamearr2 = os.listdir(dirx)
    for aa in range(len(fnamearr2)):
        nnn = dirx + os.sep + fnamearr2[aa]
        #print("nnn", nnn)
        if os.path.isfile(nnn):
             append_file(nnn)

if __name__ == '__main__':

    #path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    #port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    global fnamearr, statarr

    rescan()

    th = re_serve();  waitx();  re_open()

    while True:
        flag = False
        for aa in range(len(fnamearr)):
            stat = os.stat(fnamearr[aa])
            if statarr[aa] != stat.st_mtime:
                statarr[aa] = stat.st_mtime
                flag = True

        if flag:
            th.terminate(); waitx()
            th.kill();      waitx()
            rescan()
            print("Restarted server:")
            th = re_serve() ; waitx();
            re_open()
        time.sleep(.2)

# EOF