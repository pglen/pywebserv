#!/usr/bin/env python3

''' The simplest web server '''

# These are the functions that get called from macro expansion
# add trailing '_func' to the name as a convention

import os, sys, random, datetime

try:
    from PIL import Image
except:
    print("Must install PIL");

import wsgi_util, wsgi_style, wsgi_res, wsgi_global

def     deep_func(strx, context):
    return "Deep from code"

def     crap_func(strx, context):
    return "<b>crap</b> from code"

def     app_one_func(strx, context):

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

# ------------------------------------------------------------------------
# Faugh calendar

def     app_two_func(strx, context):


    content = "App2 here"
    return content


    '''
    Mock calendar. Does nothing but presents a calendar looking user interface
    '''

    try:
        content = '''<table width=100% border=1>
            <tr><td align=center bgcolor=#cccccc colspan=7><b>APP TWO (Calendar?)</b><br>
        '''
        #        <tr><td>code for app 2 comes here
        dt = datetime.datetime.now()
        anchor = dt.day % 7;
        mon = anchor - dt.weekday()

        rrr = monthrange(dt2.year, dt2.month)
        print("dt", dt.weekday(), dt.day, mon, anchor, "rrr", rrr)

        content += "<tr><td colspan=5>"
        cnt = 0; cnt2 = 0;
        wday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        content += "<tr>"
        for cc in range(7):
            content += "<td> <font size=-1>" + wday[cc]
        for aa in range(5):
            content += "<tr>"
            for bb in range(7):
                #aa*7 + bb + 1
                if cnt > rrr:
                    break

                cnt += 1
                if cnt > mon:
                    content += "<td> <font size=-1>" + str(cnt2+1)
                    cnt2 += 1
                    if random.randint(0, 255) % 4 == 0:
                        content += "*"
                    else:
                        content += "&nbsp;"
                else:
                    content += "<td> <font size=-1>" + "&nbsp;"

        content += "</table>"

    except:
        print("Exception on app_two_func", sys.exc_info())
    return content

def     image_func(strx, context):

    '''
     { image nnn }          --  Put an image tag nnn in the output
     { image nnn www }      --  Put an image tag in the output, resize width to requested
     { image nnn www hhh }  --  Put an image tag in the output, resize to parm

    The first two forms of the { image } function will preserve the image's aspect ratio.

    '''

    # Expand arguments
    ssss = wsgi_util.recursive_parse(strx, context,  "\[ .*? \]")
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

# ------------------------------------------------------------------------
# I wish the http standard had this one command

def     include_func(arg, context):

    #print("include_function called", arg, os.getcwd(), context, __file__)

    # Expand arguments
    ssss = wsgi_util.recursive_parse(arg, context, "\[ .*? \]")
    sss = ssss.split()

    # Travel down the dependency list
    while True:
        fname = os.path.dirname(context) + os.sep + sss[2]
        if os.path.isfile(fname):
            break
        fname = os.path.dirname(os.getcwd()) + os.sep + "content/static" + os.sep + sss[2]
        if os.path.isfile(fname):
            break
        fname = os.path.dirname(os.getcwd()) + os.sep + "content/html" + os.sep + sss[2]
        if os.path.isfile(fname):
            break
        break

    #print("trying fname", fname)
    try:
        with open(fname, 'r') as fh:
            buff = fh.read()
        #print("buff", buff)
    except:
        return "Warn: include macro cannot read file '%s'" % sss[2]

    return buff


def     build_initial_table():

    ''' The initial table for the global items '''
    try:
        wsgi_global.add_one_func("app_one", app_one_func)
        wsgi_global.add_one_func("app2",   app_two_func)
        wsgi_global.add_one_func("image",   image_func)
        wsgi_global.add_one_func("include", include_func)

        wsgi_global.add_one_func("deep",    deep_func)
        #wsgi_global.add_one_func("crap",    crap_func)

    except:
        #print("Cannot build global table", sys.exc_info())
        wsgi_util.put_exception("Cannot build global table")

def     build_initial_rc():

    ''' The initial table for the global resource items '''
    try:
        wsgi_global.add_one_func("header",   wsgi_res.header)
        wsgi_global.add_one_func("footer",   wsgi_res.footer)
        wsgi_global.add_one_func("bigtext",  wsgi_res.bigtext)
        wsgi_global.add_one_func("imgrow",   wsgi_res.imgrow)
        wsgi_global.add_one_func("article",  wsgi_res.article)
        wsgi_global.add_one_func("article2", wsgi_res.article2)

        wsgi_global.add_one_func("mystyle",  wsgi_style.mystyle)

    except:
        #print("Cannot build global rc", sys.exc_info())
        wsgi_util.put_exception("Cannot build global resources")

# EOF
