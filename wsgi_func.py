#!/usr/bin/env python3

''' The simplest web server '''

import os, sys
from PIL import Image

# These are the functions that cgt called from macro expansion
# add trailing _func as convention

import wsgi_util

def     deep_func(strx):
    return "Deep from code"

def     crap_func(strx):
    return "<b>crap</b> from code"

def     image_func(strx):

    # Expand arguments
    ssss = wsgi_util.recursive_parse(strx,  "\[ .*? \]")
    sss = ssss.split()
    #print("Image func:", sss)

    iname = "media/" + sss[2]
    if len(sss) == 4:
        return "<img src=media/" + iname + ">"

    elif len(sss) == 5:
        basewidth =  int(sss[3])
        nnn = "media/res_" + sss[3] + "_" + str(sss[2])
        # Note: If resized is older, we generate
        if not os.path.exists(nnn) or os.stat(nnn).st_mtime < os.stat(iname).st_mtime:
            try:
                img = Image.open(iname)
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                #print("new name", nnn)
                img.save(nnn)
            except:
                print("Image process", sys.exc_info())
        else:
            #print("Using cached version", nnn)
            pass
        return "<img src=" + nnn + " >"

    elif len(sss) == 6:
        basewidth  =  int(sss[3])
        baseheight =  int(sss[4])
        nnn = "media/res_" + sss[3] + "x" + sss[4] + "_" + str(sss[2])
        # Note: If resized is older, we generate
        try:
            if not os.path.exists(nnn) or os.stat(nnn).st_mtime < os.stat(iname).st_mtime:
                img = Image.open(iname)
                img = img.resize((basewidth, baseheight), Image.ANTIALIAS)
                #print("new name", nnn)
                img.save(nnn)
        except:
            print("Image process", sss[2], sys.exc_info()[1])
        else:
            #print("Using cached version", nnn)
            pass
        #return "<img src=" + sss[2] + " height=" + sss[3] + " width= " + sss[4] + " >"
        return "<img src=" + nnn + " >"

    return "<img src=media/broken.png>"

