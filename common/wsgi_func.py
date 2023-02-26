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
import wsgi_parse, wsgi_data, wsgi_str

# ------------------------------------------------------------------------

def     parse_args(strx, context):

    '''
    Expand arguments, return arr of argument strings, including command
    The latest one filters delimiters

    Mon 14.Nov.2022 Added local table variable expansion.

    '''

    fff = wsgi_parse.parse_buffer(strx, "\[ .*? \]", context, context.local_table)[0]
    eee = ' '.join(fff)

    #if context.configx.pgdebug > 5:
    #    print("Args loc expanded:", eee)

    ssss = wsgi_parse.parse_buffer(eee, "\[ .*? \]", context, wsgi_global.gl_table.mytable)[0]

    if context.configx.pgdebug > 5:
        print("Args expanded:", ssss)

    ss = ""
    for aa in ssss:
        # Filter delimiters
            ss += aa

    if context.configx.pgdebug > 6:
        print("Args pre decoded:", ssss)

    sss = str.split(ss)

    if context.configx.pgdebug > 5:
        print("Args decoded:", sss)

    ddd = []
    for aa in sss:
        if aa != '[' and aa != ']' and aa != '{' and aa != '}':
            ddd.append(aa)
    #print("Args filtered:", ddd)
    return ddd

#def     deep_func(strx, context):
#    return "Deep from code"
#
#def     crap_func(strx, context):
#    return "<b>crap</b> from code"
#

def     app_one_func(strx, context):

    ''' Example app function '''

    content = '''<table width=100% border=0 bgcolor=#dddddd>
        <tr><td align=center bgcolor=#cccccc><b>APP ONE (Some Strings?)</b><br>
        <tr><td>
        <tr><td  align=center>code for app 1 comes here
        <tr><td  align=center>code for app 1 comes here
        <tr><td  align=center>code for app 1 comes here
        <tr><td  align=center>code for app 1 comes here
        <tr><td  align=center>code for app 1 comes here
        <tr><td>
        </table>
        '''
    return content

# ------------------------------------------------------------------------
# Faugh calendar

def     app_two_func(strx, context):

    '''
    Mock calendar. Does nothing but presents a calendar looking user interface
    '''

    #content = "App Two here"
    #return content

    try:
        content = '''<table width=100% border=0  bgcolor=#dddddd>
            <tr><td align=center bgcolor=#cccccc colspan=7><b>APP TWO (Calendar?)</b><br>
        '''
        #        <tr><td>code for app 2 comes here
        dt = datetime.datetime.now()

        dt2 = datetime.datetime.now()
        from calendar import monthrange
        rrr = monthrange(dt2.year, dt2.month)

        #anchor = dt.day % 7;
        mon = rrr[0]
        anchor =	 dt.weekday()

        "day", dt.weekday(), #print("dt", dt.day, "mon", mon, "anchor", anchor, "rrr", rrr)

        content += "<tr><td colspan=7>"
        cnt = 0; cnt2 = 0;
        wday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        content += "<tr>"
        for cc in range(7):
            content += "\n<td  align=center> <font size=-1>" + wday[cc]

        for aa in range(5):
            content += "<tr>"
            for bb in range(7):
                #prog = aa*7 + bb + 1
                #if cnt2 >= rrr[1]:
                #    break

                cnt += 1
                if cnt > mon and cnt2 < rrr[1]:
                    cnt2 += 1

                    if cnt2 == dt.day:
                        #print("today")
                        bgcolor="#eeeeee"
                        color = "#888888"
                    else:
                        bgcolor="#dddddd"
                        color = "#000000"

                    content += "<td align=center bgcolor=" + bgcolor + ">"
                    decor = 0
                    #if random.randint(0, 255) % 4 == 0:
                    #    decor = 1;

                    decor = cnt2 % 4 == 0
                    if decor:
                        content += "<a href=noting>"
                    else:
                        content += " &nbsp; "

                    content += "<font size=-1>" + str(cnt2)
                    content += "</font>"

                    if decor:
                        content += "*</a>"
                    else:
                        content += " &nbsp; "
                else:
                    content += "<td align=center> -"


        content += "</table>\n"

    except:
        wsgi_util.put_exception("Exception on app_two_func")

        # Note that we still complete the table, so the site keeps going
        content += "</table>\n"

    return content

def     image_func(strx, context):

    '''
     { image nnn }          --  Put an image tag nnn in the output
     { image nnn www }      --  Put an image tag in the output, resize width to requested
     { image nnn www hhh }  --  Put an image tag in the output, resize to parm
    The first two forms of the { image } function will preserve the image's aspect ratio.
    '''
    #print("image_func", strx)

    sss = parse_args(strx, context)
    #print("Image args:", len(sss), sss)

    iname = "/media/" + sss[1]
    if len(sss) == 2:
        return "<img src=" + iname + ">"

    elif len(sss) == 3:
        try:
            basewidth =  int(sss[2])
        except:
            print("Invalid parameters to image function (3)", sss)
            return "<img src=" + iname + ">"

        nnn = "/tmp/res_" + sss[2] + "_" + str(sss[1])
        cwd = os.getcwd();
        nnn2 = cwd + nnn
        iname2 = cwd + iname

        # Note: If resized is older, we generate
        if not os.path.exists(nnn2) or os.stat(nnn2).st_mtime < os.stat(iname2).st_mtime:
            #print("Resizing", nnn2)
            try:
                img = Image.open("." + iname)
                wpercent = (basewidth / float(img.size[0]))
                hsize = int((float(img.size[1]) * float(wpercent)))
                img = img.resize((basewidth, hsize), Image.ANTIALIAS)
                img.save(nnn2)
            except:
                print("Exc Image proc.five:", nnn, sys.exc_info())
        else:
            #print("Using cached version", nnn2)
            pass
        return "<img src=" + nnn + " >"

    elif len(sss) == 4:
        try:
            basewidth  =  int(sss[2])
            baseheight =  int(sss[3])
        except:
            print("Invalid parameters to image function (4)", sss)
            return "<img src=" + iname + ">"

        cwd = os.getcwd();
        nnn = "/tmp/res_" + sss[2] + "x" + sss[3] + "_" + str(sss[1])
        nnn2 = cwd + nnn
        iname2 = cwd + iname
        #print("nnn", nnn2)
        #print("iname2", iname2)
        try:
            #print("Resizing", nnn2)
            # Note: If resized is older, we generate
            if not os.path.exists(nnn2) or os.stat(nnn2).st_mtime < os.stat(iname2).st_mtime:
                img = Image.open(iname2)
                img = img.resize((basewidth, baseheight), Image.ANTIALIAS)
                img.save(nnn2)
        except:
            print("Exc image proc.six:", iname2, sys.exc_info()[1])
        else:
            #print("Using cached version", nnn2)
            pass
        #return "<img src=" + sss[2] + " height=" + sss[3] + " width= " + sss[4] + " >"
        return "<img src=" + nnn + " >"

    return "<img src=/media/broken.png>"

def     load_data_func(strx, context):

    '''
    # ------------------------------------------------------------------------
     Get a row's data; pre load database table as macros.

       Arguments:
           arg[0]      command name
           arg[1]      name of module to get the data from

     Example:
               { loadData proj-edit }

    '''

    print("load_data_func", context)

    ddd = parse_args(strx, context)

    if context.configx.pgdebug > 3:
        print("load_data_func() ddd", ddd)

    # Get data from the editor project;
    # Careful, passing the wrong filename, it will be created
    try:
        fff = "./data/%s.pydb" % ddd[1]
        localdb = wsgi_data.wsgipydb(fff)

    except Exception as e:
        print("Could not create / open local data for '%s'" % fff, e)
        wsgi_util.put_exception("open / get data")
        return ""

    context.prog = 0
    # The data is added to the top of the context object
    context.res = localdb.getall()

    # Dump it
    if context.configx.pgdebug > 2:
        for aa in context.res:
            print("res", wsgi_str.strpad(wsgi_str.strupt(str(aa[0]))),
                        wsgi_str.strupt(str(aa[1:])))

    # Sat 25.Feb.2023 deactivted -- data is now in context variable
    # The data is returned as macros, the page can reference
    #wsgi_global.gl_table.add_one_func(prefix + "DLen", str(len(res)))
    #wsgi_global.gl_table.add_one_func(prefix + "Data", res )

    #localdb.close()

    return ""

def     get_data_func(strx, context):

    '''!
     ----------------------------------------------------------------
     Retrieve from pre loaded table

       Arguments:
           arg[0]      command name
           arg[1]      index of row

     Example:
               { getData 1 }

    '''

    ddd = parse_args(strx, context)
    print("ddd", ddd)
    print("context.prog", context.prog)

    try:
        item = wsgi_global.gl_table.lookup_item(\
                        ddd[1] + "Data")[0][int(ddd[1])][int(ddd[2])]
        #print("item", item)
    except IndexError:
        #wsgi_util.put_exception("get data")
        item = "No data at %s:%s" % (ddd[1], ddd[2])
    except:
        wsgi_util.put_exception("get data")
        item = "Error"
    return item

# ------------------------------------------------------------------------
# I wish the http standard had this one command

def     include_func(strx, context):

    '''! Include a file and present it verbatim '''

    #print("include_func()", strx, dir(context.mainclass))
    #print("include_func()", strx, context.fname)

    # Expand arguments
    ssss = wsgi_parse.parse_buffer(strx, "\[ .*? \]", context, wsgi_global.gl_table.mytable)[0]
    ss = ""
    for aa in ssss:
        ss += aa
    sss = str.split(ss)

    #print("args spaced:", sss)

    fname = ""
    try:
        # Travel down the dependency list, start at the same dir as the caller file
        while True:
            fname = os.path.dirname(context.fname) + os.sep + sss[2]
            if os.path.isfile(fname):
                break
            fname = os.path.dirname(os.getcwd()) + os.sep + "content/static" + os.sep + sss[2]
            if os.path.isfile(fname):
                break
            fname = os.path.dirname(os.getcwd()) + os.sep + "content/html" + os.sep + sss[2]
            if os.path.isfile(fname):
                break
            break

    except:
            #print(sys.exc_info())
            wsgi_util.put_exception("find parsed file name")

    if context.configx.pgdebug > 2:
        print("include fname", fname)

    try:
        with open(fname, 'r') as fh:
            buff = fh.read()
        #print("buff", buff)
    except:
        return "Warn: include macro cannot read file '%s'" % sss[2]

    return buff


def     build_initial_table():

    ''' The initial table for the global items
        User may override this
    '''
    #print("build_initial_table()")

    try:
        # Built ins
        wsgi_global.gl_table.add_one_func("image",    image_func)
        #wsgi_global.gl_table.add_one_func("getData",  get_data_func)
        wsgi_global.gl_table.add_one_func("load_data", load_data_func)
        wsgi_global.gl_table.add_one_func("include",  include_func)
        #wsgi_global.gl_table.add_one_func("deep",     deep_func)

        # Examples
        wsgi_global.gl_table.add_one_func("app_one",    app_one_func)
        wsgi_global.gl_table.add_one_func("app_two",    app_two_func)

    except:
        #print("Cannot build global table", sys.exc_info())
        wsgi_util.put_exception("Cannot build global initital table")

init_rc =  [   \

    #("header",          wsgi_res.header),
    #("footer",          wsgi_res.footer),
    #("bigtext",         wsgi_res.bigtext),
    #("var",             wsgi_res.var),
    #("imgrow",          wsgi_res.imgrow),
    #("mystyle",         wsgi_style.mystyle),
    #("xarticle",        wsgi_res.article),
    #("xarticle2",       wsgi_res.article2),
    #("recursive",       wsgi_res.recursive),     # Do not add this, just for testing
    #("nullcolor",       "#cccccc"),
    #("sitecolor",       "#aaffbb"),

    # This junk (above) added to parse time  2+ msec ... de activated it

    ("spacer",          "<table><tr><td></table>"),
    ("linespacer",      "<tr><td height=8>"),
    ("feedwidth",       "400"),
    ("feedheight",      "300"),
    ("thumbwidth",      "120"),
    ("thumbheight",     "80"),
    ]

def     build_initial_rc():

    '''
        The initial table for the global resource items
        The user resources may override any of this
    '''
    try:
        for aa in init_rc:
            wsgi_global.gl_table.add_one_func(aa[0], aa[1])

    except:
        #print("Cannot build global rc", sys.exc_info())
        wsgi_util.put_exception("Cannot build global resources")

# EOF
