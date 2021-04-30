#!/usr/bin/env python3

'''
    Small wsgiref based web server. Takes a path to serve from and an
    optional port number (defaults to 8000), then tries to serve files.

    Mime types are guessed from the file names, 404 errors are raised
    if the file is not found. Used for the make serve target in Doc.

    Restarts if any of the files in current dir changed

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

    #["wsgi_main.py", "wsgi_content.py", "wsgi_util.py", "wsgi_global.py", "index.html"]

def re_open():
    #th = subprocess.Popen(["firefox", "localhost:8000"], close_fds=True)
    #th = subprocess.Popen(["xvkbd", "-window", "Firefox", "-text", "\Cr"])
    th = subprocess.Popen(["./bringfocus.sh"], shell=True)
    return th

def re_serve():
    th = subprocess.Popen(["/usr/bin/env", "python", "wsgi_main.py"] + sys.argv[1:])
    return th

def  rescan():

    global fnamearr, statarr
    fnamearr = []; statarr = []
    fnamearr2 = os.listdir()
    #print("fnamearr2", fnamearr2)
    # Build reference
    for aa in range(len(fnamearr2)):
        if os.path.isfile(fnamearr2[aa]):
            fff = os.stat(fnamearr2[aa]).st_mtime
            fnamearr.append(fnamearr2[aa])
            statarr.append(fff)
    ddd = "projects"
    fnamearr3 = os.listdir(ddd)
    #print("fnamearr3", fnamearr3)
    for aa in range(len(fnamearr3)):
        aaa = ddd + os.sep + fnamearr3[aa]
        if os.path.isfile(aaa):
            fff = os.stat(aaa).st_mtime
            fnamearr.append(aaa)
            statarr.append(fff)
    #print("fnamearr", fnamearr)

if __name__ == '__main__':

    #path = sys.argv[1] if len(sys.argv) > 1 else os.getcwd()
    #port = int(sys.argv[2]) if len(sys.argv) > 2 else 8000

    global fnamearr, statarr
    rescan()

    th = re_serve();  time.sleep(.1);  re_open()

    while True:
        flag = False
        for aa in range(len(fnamearr)):
            stat = os.stat(fnamearr[aa])
            if statarr[aa] != stat.st_mtime:
                statarr[aa] = stat.st_mtime
                flag = True

        if flag:
            th.terminate()
            time.sleep(.5)
            th.kill()
            time.sleep(.5)
            rescan()
            print("Restarted server:")
            th = re_serve() ; time.sleep(.2);  re_open()

        time.sleep(.5)

# EOF