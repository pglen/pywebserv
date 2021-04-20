#!/usr/bin/env python3

''' The simplest web server '''

# These are the functions that get called from macro expansion
# add trailing the '_func' as convention

import os, sys, random, datetime

from PIL import Image

import wsgi_util
import wsgi_style

def     deep_func(strx):
    return "Deep from code"

def     crap_func(strx):
    return "<b>crap</b> from code"

def     app_one_func(strx):

    content = '''<table width=100% border=0>
        <tr><td align=center bgcolor=#cccccc><b>APP ONE</b><br>
        <tr><td>
        <tr><td>code for app 1 comes here
        <tr><td>code for app 1 comes here
        <tr><td>code for app 1 comes here
        <tr><td>code for app 1 comes here
        <tr><td>code for app 1 comes here
        <tr><td>
        </table>
        '''
    return content

def     app_two_func(strx):

    content = '''<table width=100% border=1>
        <tr><td align=center bgcolor=#cccccc colspan=7><b>APP TWO (Calendar?)</b><br>
    '''
    #        <tr><td>code for app 2 comes here

    dt = datetime.datetime.now()
    anchor = dt.day // 7;
    print("dt", dt.weekday(), dt.day, anchor)
    content += "<tr><td colspan=5>"
    for aa in range(7):
        content += "<tr>"
        for bb in range(5):
            content += "<td> <font size=-1>" + str(aa*7 + bb + 1)
            if random.randint(0, 255) % 4 == 0:
                content += "*"
            else:
                content += "&nbsp;"


    content += "</table>"

    return content


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

