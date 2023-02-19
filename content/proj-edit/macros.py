 #!/usr/bin/env python3

import  sys, os
import  wsgi_util, wsgi_func, wsgi_global, wsgi_data

'''
    Local macros and data. Register it after init or use the "_mac_ prefix to auto register
'''

from . import common

modname = __file__.split(os.sep)[-2]
#print("modname", "'" + modname + "'")


_mac_feedwidth = '800'
_mac_ShortCName = ''' United Planet Peace '''

# ------------------------------------------------------------------------

gl_arr = []

def fill_data(localdb, recnum):

    #print("data file", "data/%s_data.sqlt" % modname)
    #print("localdb", localdb)
    #print("recnum", recnum)
    #print("all", localdb.getall())

    global gl_arr
    res = localdb.getbyid(recnum)
    if res[0] not in gl_arr:
        gl_arr.append(res[0])
        return res

    print("skip:", recnum, wsgi_util.strupt(res[0]))
    return None

    ##print("res", res)
    #if not res:
    #    res = "Empty record"
    #return res

_mac_center_top = '''
 <table width=100% { sitecolor } border=0>
    <tr  height=36>
    <td align=center width=30%> &nbsp; &nbsp; <font size=+2>
    <a href=index.html> <b>{ ShortCName }</b> </a>
    </font>
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
        </table>
     </table>
'''

_mac_edit_center = '''
<td valign=top>

     <center>
     { center_top }
     { center_body }
'''

_mac_editrow = '''
<tr align=center><td> Edit
<td> Edit2
<td> Edit3
'''

#<font Page Main size=+2>Edit Rows</font>

def imgrow_data(strx, context):

    sss = wsgi_func.parse_args(strx, context)
    foot = "" #'''<td> <td>  '''
    #print("arg sss", sss)
    data = fill_data(context.localdb, int(sss[1]))

    # The fill data will filter duplicates for us
    if not data:
        return

    #print("data", data)
    if (context.rec_cnt % 2) == 0:
        trcolor = "#ddeedd"
    else:
        trcolor = "#cceecc"
    context.rec_cnt += 1

    strx = '''
    <form action=editor.html method=post>
    <tr style=\"background-color:%s\">''' %  trcolor

    for aa in data:
        aa = wsgi_util.strtrim(aa)
        strx += "<td> <font>%s</font> " % aa

    # add footer
    strx += '''
        <td width=10>
        <input type=submit id=idsub name=ed_%s  value="Edit" >
        <br>
        <input type=submit id=idsub name=del_%s value="  Del " >
        </form>
        ''' %  (sss[1], sss[1])

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
                  Image row text Image row text Image row text Image row text
                  Image row text Image row text Image row text Image row text
                  Image row text Image row text Image row text Image row text
                  Image row text Image row text Image row text Image row text
                  Image row text Image row text Image row text Image row text
                  Image row text Image row text Image row text Image row text
                  Image row text Image row text Image row text Image row text
                  Image row text Image row text Image row text Image row text
                  Image row text Image row text Image row text Image row text
                  Image row text Image row text Image row text Image row text
                  </div>
            </table>
       </table>
    '''

    desc = '''
    Image description Image description3
      Image description
    Image description Image description Image description Image description Image description
    '''

    strx += foot
    strx += desc

    return strx

def mid_rows(strx, context):

    print("mid_rows", strx, context)

    ret = '''
    <tr> <td colspan=7 align=center>
            <p><font size=+3>Data Review</font>
            <br>
    '''

    try:
        wsgi_data.soft_opendb(context, modname)
    except:
        print("Could not create local data for %s" % modname)
        wsgi_util.put_exception("opening SQL")
        return

    ret += "<table border=0 width=100%>"
    recs = context.localdb.getcount()
    print("got", recs, " records")

    global gl_arr
    gl_arr = []

    if not recs:
        ret += "<tr><td align=center>No Data"
    else:
        #for aa in range(recs):
        context.rec_cnt = 0
        # Starting at the end
        for aa in range(recs-1, -1, -1):
            ddd = "{ imgrow_data [ %d ] }" % (aa)
            ret +=  ddd

    ret += "</table>"
    #context.localdb.close()
    return ret

_mac_center_body = '''
    <table width=100% border=0>
        <tr><td align=center colspan=6>
        { mid_rows }
    </table>
'''

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

_mac_add_new = '''
    <form action=editor.html method=post>
    <input type=submit name='add_new' value='Add New'>
    </form>
'''

_mac_right = '''
    <td valign=top width=20%>
        <table width=100% cellpadding=3 border=1>
        <tr><td bgcolor={ tabhead } height=36 align=center>
            <font size=+1> <b>Misc</b>
        <tr><td>
        <tr><td align=center>
            &nbsp; &nbsp;
            <b>Last column, maybe ads</b><br>
            cogito ergo sum cogito ergo sum cogito ero sum
            cogito ero sum cogito ero sum cogito ero sum
            cogito ero sum cogito ero sum cogito ero sum
            { deep }<br>
            { app_one } <p>
            { app2 } <p>
            { app3 }
        </table>
'''

# Clear text box when the first char is space (empty)
_mac_clr = ''' if(this.value[0]==' ')this.value='' '''

_mac_header = '''
    <table width=100% bgcolor={ sitecolor } border=0>
        <form method=post>
            <tr><td>
            <a href=index.html>
            <font size=+2><center><b>Welcome to UPP Site Editor, </a> </font> <br>
            <!-- &nbsp; &nbsp; &nbsp;  -->
            the editing site for United Planet Peace<br>
            <font size=-1 color=red>Authorized users only</center></font>

            <!-- (under construction, check back later) --!>
             <td align=right width=40%>
                <!--
                <font size=-1>Quick feedback:</font>  &nbsp;
                <input type=text name="feedname" onfocus="{ clr }" value=" Your Name" size=10>
                <input type=text name="feedtit"  onfocus="{ clr }" value=" Feddback Title" size=10>
                <input type=text name="feedtxt"  onfocus="{ clr }" value=" Feedback Content" size=12>
                <input type=submit name='feedSUB' value='Submit'>
                 -->
            <td>

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
    wsgi_util.add_local_func("imgrow_data", imgrow_data, common.local_table)

except:
    #print("Exception on editor init vars", sys.exc_info())
    wsgi_util.put_exception("in Editor Index")
    raise

# EOF