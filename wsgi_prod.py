#!/usr/bin/env python3

# Test in production environment

import sys
import os
import mimetypes
import time
import multiprocessing
from wsgiref import simple_server, util


def application(environ, respond):

    print("arg", sys.argv)
    path = os.path.dirname(os.path.realpath(__file__));
    print("mypath", path)
    #printenv(environ)

    #print("path", environ['PATH_INFO'])
    #print("qqq", environ['QUERY_STRING'])

    print("pwd", os.getcwd());
    os.chdir(path)
    print("pwd", os.getcwd());

        #fn = os.path.join(path, environ['PATH_INFO'][1:])
    fn = environ['PATH_INFO'][1:]
    print("Request:",  fn)

    # Empty file name, index wanted
    if(fn.split(os.path.sep)[-1] == ""):
        fn = os.path.join(fn, 'index.html')

    print("Calc Request:",  fn)


    type = mimetypes.guess_type(fn)[0]
    if not type:
        type = "text/plain"

    if os.path.exists(fn):
        respond('200 OK', [('Content-Type', type + ';charset=UTF-8')])
        #respond('200 OK', [('Content-Type', type)])
        fp = util.FileWrapper(open(fn, "rb"))
        return fp
    else:
        #print("Not found",  fn)
        respond('404 Not Found', [('Content-Type', 'text/plain')])
        #respond('200 Hello world', [('Content-Type', 'text/plain')])
        return [b'not found']
        #return "Hello World"

def hello(aa, bb):
    print(aa, bb)

if __name__ == '__main__':

    env = dict(os.environ)
    env.update ( {"PATH_INFO" : "/"})
    env.update ( {"QUERY_STRING" : ""})
    application(env, hello)

# EOF
