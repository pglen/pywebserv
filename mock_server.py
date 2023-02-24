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
        return [util.FileWrapper(open(fn, "rb"))]
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

def _re_open():
    #th = subprocess.Popen(["firefox", "localhost:8000"], close_fds=True)
    #th = subprocess.Popen(["xvkbd", "-window", "Firefox", "-text", "\Cr"])
    th = subprocess.Popen(["./bringfocus.sh"], shell=True)
    #return th
    pass

def _re_serve():
    opt = ""
    th = subprocess.Popen(["/usr/bin/env", "python", "wsgi_main.py"] + sys.argv[1:])
    return th

def waitx():
    time.sleep(.1)

def append_filename(nnn):
    global fnamearr, statarr

    if os.path.isfile(nnn):
        fff = os.stat(nnn).st_mtime
        # Two synchronized arrays
        fnamearr.append(nnn)
        statarr.append(fff)

# ------------------------------------------------------------------------
# Scan all files in one deep directory

# Wed 22.Feb.2023 data files excempted

def isskip(aaa):
    ret = False
    # No need for these files
    if "__" == aaa[:2]:
        #print("Skipping __ files", aaa)
        ret = True
    if ".git" in aaa:
        #print("Skipping .git files", aaa)
        ret = True
    if "data/" in aaa:
        #print("Skipping data dir", aaa)
        ret = True
    if "test/" in aaa:
        #print("Skipping data dir", aaa)
        ret = True
    return ret

def  rescan():
    global fnamearr, statarr

    fnamearr = []; statarr = []
    fnamearr2a = os.listdir()
    #print("fnamearr2a", fnamearr2a)

    for aaa in fnamearr2a:
        if isskip(aaa):
            continue
        if os.path.isdir(aaa):
            _rescan(aaa)
        if os.path.isfile(aaa):
             append_filename(aaa)
    #print("fnamearr", fnamearr)

# ------------------------------------------------------------------------

def _rescan(dirx):

    fnamearr2 = os.listdir(dirx)
    for aa in range(len(fnamearr2)):
        nnn = dirx + os.sep + fnamearr2[aa]
        #print("nnn", nnn)
        if isskip(nnn):
            continue

        if os.path.isfile(nnn):
             append_filename(nnn)
        elif os.path.isdir(nnn):
            _rescan(nnn)
    return None

# ------------------------------------------------------------------------
# Entry point for the server

if __name__ == '__main__':

    #path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    #port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    print("start mock server")

    global fnamearr, statarr

    rescan()

    th = _re_serve();  waitx();  _re_open()

    while True:

        #print(th.returncode, th.pid)

        flag = False
        for aa in range(len(fnamearr)):

            # Make sure the log files do not trigger
            if fnamearr[aa][-4:] == ".log":
                continue
            # and python compile files do not trigger restart
            if fnamearr[aa][-4:] == ".pyc":
                continue

            # and sqlt files
            if fnamearr[aa][-5:] == ".sqlt":
                continue

            try:
                stat = os.stat(fnamearr[aa])
            except:
                pass
                continue;

            if statarr[aa] != stat.st_mtime:
                statarr[aa] = stat.st_mtime
                flag = True
                #print("would restart on", fnamearr[aa])

        if flag:
            time.sleep(.4)

            th.terminate(); waitx()
            th.kill();      waitx()
            rescan();       waitx()

            #print("Restarted server:", time.asctime())

            th = _re_serve() ; waitx();

            _re_open()
        time.sleep(.4)

# EOF
# hashx signature: 0x4a09199a
