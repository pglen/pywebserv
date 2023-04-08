 #!/usr/bin/env python3

import  sys, os
import  wsgi_util, wsgi_func, wsgi_global, wsgi_data, wsgi_str

'''
    Local macros and data. Register it after init or use the "_mac_ prefix to auto register
'''

from . import common

modname = __file__.split(os.sep)[-2]
#print("modname", "'" + modname + "'")

_mac_feedwidth = '800'
_mac_ShortCName = ''' United Planet Peace '''

# ------------------------------------------------------------------------

_mac_center_top = '''

 <table width=100% { sitecolor } border=0>
    <tr  height=36>
    <td align=center width=30%> &nbsp; &nbsp; <font size=+2>
    <a href=index.html> <b>{ ShortCName }</b> </a>
    </font>
        <td>
        <!--
        <table width=100% border=0>
            <tr align=center>
                <td>
                <td> <a href=index.html>
                     <img src=/siteicons/go-home.png class=image title="Back to home page"> </a>
                <td> <img src=/siteicons/emblem-default.png class=image title="Go forward">
                <td> <img src=/siteicons/emblem-unreadable.png class=image title="Blah Blah">
                <td> <img src=/siteicons/emblem-favorite.png class=image title="Favorite">
                <td>
        </table>\n
        -->
     </table>\n
'''

_mac_edit_center = '''

    <td valign=top bgcolor=#eeeeee>
     <table border=0 width=100%>
        <tr><td align=center>
        <table width=100% border=0>
            <tr><td align=center>
            { mid_rows }
        </table>

         { add_new }

     </table>

'''

_mac_editrow = '''
<tr align=center><td> Edit
<td> Edit2
<td> Edit3
'''

#<font Page Main size=+2>Edit Rows</font>

def row_data(strx, context):

    #sss = wsgi_func.parse_args(strx, context)
    #print("row_data", strx, context)

    foot = "" #''' <td> #'''<td>

    strx = '''<form action=editor.html method=post>'''

    res = getattr(context, context.mydb).res
    recs = len(res)

    if not  recs:
        print("No data in context",)
        strx += "No Data"
        strx += "</form>\n"
        return strx

    cnt = 0
    for onerec in res:

        #print("onerec", onerec)

        if (cnt % 2) == 0:
            trcolor = "#ddeedd"
        else:
            trcolor = "#cceecc"
        strx += '''\n\n<tr style=\"background-color:%s\">''' %  trcolor

        #for bb in onerec[1:]:
        for bb in onerec[1:]:
            bbb = wsgi_str.strtrim(bb)
            strx += "\n      <td>%s" % bbb
        cnt += 1

        # Buttons
        buttstr = '''
            <td width=10>
            <input type=submit id=idsub name=ed_%s  value="Edit" >
            <br>
            <input type=submit id=idsub name=del_%s value="  Del " >
            ''' %  (onerec[0], onerec[0])

        #print("buttstr", buttstr)
        strx += buttstr

    return strx

    strx = '''
    <tr> <td width=10>
    <td width=20>
    <div class=up-class> <font size=+2>Hello rotated text</font></div>
    <td width=10>
    <td align=center>
    <table width=100% border=0>
        <tr><td align=center>
        <font size=+2> Image row Header
    '''
    strx += str(sss[1])
    strx += '''
    <tr><td align=center>
    { image beach-hd.jpeg [ feedwidth ]  }

        <tr><td align=center>
         <a href=editor?like>
         &nbsp;
         <img src=/siteicons/like.png  class=plain title="Like">
         </a>
         &nbsp;
         <a href=editor?dislike>
         &nbsp;
         <img src=/siteicons/dislike.png   class=plain  title="DisLike">
         &nbsp;
         <a href=editor?love>
         &nbsp;
         <img src=/siteicons/emblem-favorite.png    class=plain  title="Love">
         &nbsp;
         <a href=editor?forward>
         &nbsp;
         <img src=/siteicons/mail-forward.png   class=plain  title="Forward">
         &nbsp;
         <a href=editor?share>
         &nbsp;
         <img src=/siteicons/network-transmit.png   class=plain title="Share">
         &nbsp;

        <tr><td align=center>
            <table border=0>
            <tr><td align=center>
                 <div class=textx>
                  <font size=+0>
                  Image row text Image row text Image row text Image row text
                  Image row text Image row text Image row text Image row text
                  </div>
            </table>\n
       </table>\n
    '''

    desc = '''
    Image description Image description
    '''

    strx += foot
    strx += desc

    return strx

def mid_rows(strx, carryon):

    #print("mid_rows", strx, carryon)

    ret = "<table border=0 width=100%>"

    ret += '''
    <tr> <td colspan=7 align=center>
            <p><font size=+3>Data Review (%s)</font>
            <br>
    ''' % (carryon.mydb)

    res = getattr(carryon, carryon.mydb).res
    recs = len(res)

    if not recs:
        ret += "<tr><td align=center>No Data / Empty Database"
    else:
        #carryon.xdata = carryon.localdb.getall(checker)
        # Render it
        ret +=  "{ row_data }"

    ret += "</table>\n"

    return ret

_mac_nav = '''
    <table width=100% border=0>
        <tr align=center>
            <td align=right>
                &nbsp <img src=/siteicons/media-skip-backward.png title="Backward Front">
                &nbsp <img src=/siteicons/media-seek-backward.png title=Backward>
                <td width=150px>
                &nbsp; Navigation &nbsp;
                <td align=left>
                &nbsp <img src=/siteicons/media-seek-forward.png title=Forward>
                &nbsp <img src=/siteicons/media-skip-forward.png title="Forward Front">
    </table>
'''

def add_new(strx, carry):

    strx = '''
    <table width=80%%>
        <tr><td align=center>
        <form action=editor.html method=post>
        <input type=submit name='add_new' value='Add New'>
        <input type=hidden name='db' value='%s'>
        <hr>
        <input type=submit name='exp' value='Export'>
        <input type=submit name='imp' value='Import'>
        </form>
    </table>
    ''' % (carry.mydb)
    return strx

_mac_right = '''
    <td valign=top width=20%>
        <table width=100% cellpadding=1 border=0>
            <tr><td bgcolor={ tabhead } height=36 align=center>
                <font size=+1> <b>Misc</b>
            <tr><td>
            <tr><td align=center>
                &nbsp; &nbsp;
                <b>Last column, maybe ads</b><br>
                cogito ergo sum cogito ergo sum cogito ero sum
                cogito ero sum cogito ero sum cogito ero sum
                cogito ero sum cogito ero sum cogito ero sum
        </table>
'''

# Clear text box when the first char is space (empty)
_mac_clr = ''' if(this.value[0]==' ')this.value='' '''

_mac_edit_header = '''
    <table width=100% bgcolor={ sitecolor } border=0>
        <form method=post>
            <tr><td>
            <a href=index.html>
            <font size=+2><center><b>Welcome to UPP Site Editor, </a> </font> <br>
            <!-- &nbsp; &nbsp; &nbsp;  -->
            the editing site for United Planet Peace<br>
            <font size=-1 color=red>Authorized users only</center></font>
            <td>

        <table width=100% border=0>
            <tr align=center>
                <td>
                <td> <a href=index.html>
                     <img src=/siteicons/go-home.png class=image title="Back to home page"> </a>
                <td> <img src=/siteicons/emblem-default.png class=image title="Go forward">
                <td> <img src=/siteicons/emblem-unreadable.png class=image title="Blah Blah">
                <td> <img src=/siteicons/emblem-favorite.png class=image title="Favorite">
                <td>
        </table>\n

        </form>
            <td align=right width=18%>
                Search site: &nbsp; <input type=text value="" size=12>
                <td align=right>
                <img src=/siteicons/mail-forward.png class=image title="Mail / Contact Us">
                <a href=index.html> <img src=/siteicons/application-exit.png title="Enter / Log In"></a>
    </table>
'''

try:
    wsgi_util.add_locals(locals().copy(), common.local_table)
    wsgi_util.add_local_func("mid_rows", mid_rows, common.local_table)
    wsgi_util.add_local_func("row_data", row_data, common.local_table)
    wsgi_util.add_local_func("add_new", add_new, common.local_table)

except:
    #print("Exception on editor init vars", sys.exc_info())
    wsgi_util.put_exception("in Editor Index")
    raise

# EOF