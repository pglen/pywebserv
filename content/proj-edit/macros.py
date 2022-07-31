 #!/usr/bin/env python3

import sys
import  wsgi_util, wsgi_func, wsgi_global

'''
    Local macros and data. Register it after init or use the "_mac_ prefix to auto register
'''

local_table = []

_mac_ShortCName = '''
 United Planet Peace
'''

_mac_edit_center = '''
<td valign=top>
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
     <center>{ center_body }
'''

_mac_editrow = '''
<tr align=center><td> Edit
<td> Edit2
<td> Edit3
'''

_mac_feedwidth2 = '800'

_mac_imgrow_ed = '''
  <tr>  <td width=10>
  <td width=20>
  <div class=up-class> <font size=+2>Hello rotated text</font></div>

  <td width=10>
     <td align=center>
      <table border=0><tr><td align=center width=400>
       <font size=+2> Image row Header
      { image beach-hd.jpeg [ feedwidth ]  }<p>

         <div class=textx>
          <font size=+0>
          Image row text Image row text Image row text Image row text
          Image row text Image row text Image row text Image row text
          </div>
       </table>

      <td width=10>
      <td> Image description Image description3
      Image description
      Image description Image description Image description Image description Image description
'''

def imgrow_data(strx, context):

    sss = wsgi_func.parse_args(strx, context)
    #print("strx", strx)

    strx = '''
    <tr>  <td width=10>
    <td width=20>
    <div class=up-class> <font size=+2>Hello rotated text</font></div>

    <td width=10>
     <td align=center>
      <table border=0 width=100%>
      <tr><td align=center>
       <font size=+2> Image row Header
      <tr><td align=center>
      { image beach-hd.jpeg [ feedwidth2 ]  }
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
          </div>
       </table>
    '''


    desc = '''
    Image description Image description3
      Image description
    Image description Image description Image description Image description Image description
    '''

    foot = '''<td width=10> <td>  '''
    strx += foot
    strx += desc

    return strx

def one_row(strx, context):

    #print(strx, context)

    ret = ""
    for aa in range(5):
        #print("One row")
        ret +=   " { imgrow_data [ %d ] }" % aa
    return ret

_mac_center_body = '''
    <table width=100% border=0>
        <tr><td align=center colspan=6>
        <font Page Main size=+2>Edit Rows</font>

        { one_row }

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

_mac_right = '''
<td width=20% valign=top>
  <table border=0 width=100% cellpadding=3>
    <tr><td bgcolor={ tabhead } height=36 align=center>
        <font size=+1> <b>Misc</b>
    <tr><td>
    <tr><td align=center>
        &nbsp; &nbsp;
        <b>Last column, maybe ads</b><br>
        cogito ero sum cogito ero sum cogito ero sum
        cogito ero sum cogito ero sum cogito ero sum
        cogito ero sum cogito ero sum cogito ero sum
        { deep }<br>
        { app_one } <p>
        { app2 } <p>
        { app3 }
</table>
'''

_mac_article3 = '''
    <td>
        <table border=0 bgcolor=#dddddd>
            <tr><td>
            <table border=0 bgcolor=#f5f5f5>
            <tr>
                <tr><td colspan=2>
                <font size=+2>Article header, number three
                <tr>
                <td>
                { image beach-hd.jpeg [ thumbwidth ] [ thumbheight ] }
                <td>
                Image description
                <tr><td colspan=2> Article Title
                <tr><td colspan=2 style="text-alignment:justify"> Image description3
                Article / Image description detail <br>
                Article / Image description detail
                Article / Image description detail
            </table>
        </table>
'''

_mac_article4 = '''
    <td>
        <table border=0 bgcolor=#dddddd>
            <tr><td>
            <table border=0 bgcolor=#eeeeee>
            <tr>
                <tr><td colspan=2>
                <font size=+2>"{ art_header } four"
                <tr>
                <td>
                { image beach-hd.jpeg [ thumbwidth ] [ thumbheight ] }
                <td>
                Image description
                <tr><td colspan=2> Article Title
                <tr><td colspan=2 style="text-alignment:justify"> Image description3
                Article / Image description detail <br>
                Article / Image description detail
                Article / Image description detail
            </table>
        </table>
'''

_mac_article5 = '''Hello'''

_mac_art_header = '''Header here'''

_mac_header2 = '''
    <table width=100% border=0>
        <form method=post>
            <tr><td>
            <a href=index.html>
            <font size=+2><b>Welcome to UPP Site Editor, </a> </font> <br>
            &nbsp; &nbsp; &nbsp; the site for United Planet Peace
            <!-- (under construction, check back later) --!>

            <td align=right>
                 <font size=-1>Quick feedback:</font>  &nbsp;
                <input type=text name="feedname" value="Name" size=10>
                <input type=text name="feedtit"  value="Title" size=10>
                <input type=text name="feedtxt"  value="Feedback Content" size=12>
                <input type=submit name='feedSUB' value='Submit'>
            <td>
        </form>

    </table>
'''

try:
    vvv = locals().copy()
    #print("vvv", vvv)
    for aa in vvv:
        if "_mac_" in aa[:5]:
            if Config.verbose:
                print("Added:", aa[5:]) #, vvv[aa][:12])
            wsgi_util.add_local_func(aa[5:], vvv[aa], local_table)

    #print("Local table: len=%d", len(local_table))
    #for aa in local_table:
    #    print(" '" + aa[0] + "'", end = " ")
    #print ("\ntable end")

    wsgi_util.add_local_func("one_row", one_row, local_table)
    wsgi_util.add_local_func("imgrow_data", imgrow_data, local_table)
    #wsgi_global.add_one_func("feedwidth2", _mac_feedwidth2)

except:
    #print("Exception on editor init vars", sys.exc_info())
    wsgi_util.put_exception("Editor")
    raise

# EOF