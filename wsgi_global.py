#!/usr/bin/env python3

# These tags are global to the site

import os, sys
from PIL import Image

import wsgi_res

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

global_table = \
  [
    ["header2", " <font size=+2>Sub Header here</font>"],
    ["header", wsgi_res.header],
    ["footer", wsgi_res.footer],
    ["var", "<font size=+1>variable { deep } </font>"],
    ["no problem", "no even a <b>little</b> problem? "],
    ["bigtext", wsgi_res.bigtext],
    ["deep", deep_func],
    ["crap", crap_func],
    ["image", image_func],
    ["mystyle", wsgi_res.mystyle],
    ["spacer", "<table><tr><td></table>"],
    ["mycolor", "bgcolor=#aaffbb"],
    ["thumbwidth", "120"],
    ["thumbheight", "80"],
    ["imgrow", wsgi_res.imgrow],
  ]

def global_items(item):

    #print("item", "'" + item + "'")
    for aa in global_table:
        if item[2:-2] == aa[0]:
            if type(aa[1]) == str:
                return aa[1]
            if type(aa[1]) == type(global_items):
                return aa[1](item)

    # "??" #return str(item[2:-2]) + "??"
    return item

# Parameterized last

def global_para_items(item):

    #print("item", "'" + item + "'")

    # rescan for parameterized
    for aa in global_table:
        if item[2:-2].split()[0] == aa[0]:
            if type(aa[1]) == type(global_items):
                return aa[1](item)

    return "!!" + str(item[2:-2]) + "!!"
