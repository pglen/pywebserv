 #!/usr/bin/env python3

'''
     This is a sample project macro file;
        Variables start with "_mac_" will become local macros, that can be
        referenced on this page.
        Variables start with "_glob_" wil become global that can be
        referenced on the whole site.

     This file is imported under a try: except clause, so ordinarily,
    nothing in this file can down the site, can only down this page.
    (for example a syntax error) However, some conditions (like missing
    site dependencies) CAN down the site.
'''

import os, sys, time
import wsgi_util, wsgi_func, wsgi_data, wsgi_global

''' Local macros and data. Register it after init or use the _mac_ prefix to auto register
'''

from . import common

_glob_tabhead = "#ccffcc"
_glob_misscol = "#eeeeee"

_mac_CompanyName = '''UPP the United Planet Peace'''

_glob_sitestyle = '''
<style>
.container {
  position: relative;
  width: 50%;
}
.plain {
    #border: 0;
    #background-color: #333333;
    border-radius: 0px;
}
.image {
  opacity: 1;
  display: inline;
  height: auto;
  transition: .5s ease;
  backface-visibility: hidden;
  //corner-radius: 15px;
}
img {
  opacity: 1;
  display: inline;
  height: auto;
  transition: .5s ease;
  backface-visibility: hidden;
  border-radius: 15px;
}
.container {
  position: relative;
  width: 50%;
}
.container:hover .image {
  opacity: 0.3;
}
.container:hover .middle {
  opacity: 1;
}
a:link, a:visited {
    //color: black;
    text-decoration: none;
    decoration: none;
}
.up-class {
    writing-mode: sideways-lr;
    text-orientation: mixed;
    //background-color:  #aaffaa;
}
.textx {
    border-radius: 10px;
    background-color:  #cccccc;
    padding: 10px;
    max-width: 800px;
}
</style>
'''

## Example bad type for glob
#_glob_site_bad = ("1", "2")
## Example bad type for mac
#_mac_site_bad = ("1", "2")

# Can add a function too
#def _glob_sitestyle_func(config, carry):
#    print(glob_sitestyle2)

_glob_site_left = '''
<table width=100% border=0>
    <tr><td bgcolor={ tabhead } align=center colspan=2 height=36>
    <font size=+1><b>Main Navigation</b>
    <tr><td height=6>
    <tr><td colspan=2 align=center><a href=/index.html>
        <img src="/media/united_planet_logo.png" title="Main Logo">
        </a>

    <tr><td height=6>
    <tr><td width=30%> &nbsp;
    <td>
        <li><font size=+1><a href=index.html>Home Page</a>
        <li><a href=log.html>Log Page</a>
        <li><a href=index.html>Blog Page</a>
        <li><a href=index.html>Personal Page</a>
        <li><a href=index.html>Tech Page</a>
        <li><a href=index.html>Another Page</a>
        <li><a href=more.html>More <br> &nbsp;  &nbsp; (test for broken link)</a>
    <tr><td height=12>
    <tr><td colspan=2 style="text-align:justify;">
    &nbsp;

    <!--&nbsp <img src=siteicons/media-skip-backward.png title="Backward Front">
    -->
    <tr><td height=8 align=center colspan=2>
    <!-- <img src="/media/upp_2_small.png" title="Logo"> -->
 </table>

'''

_mac_mission_statement = '''
    <table width=100% cellpadding=3 border=0>
    { mission_statement }
    </table>
'''

_mac_mission_statement = '''

<tr><td fgcolor=white style="bgcolor: { xmisscol }; color:black">
    <font size=-1>Mission Statement:</font>
    <font size=+0><br></font>
    <font size=+2><center><b>World Wide Globalization Message.</b></center><p></font>
    &nbsp; &nbsp; The pace of globalization has exceeded expectations. This institution is searching
    for new ways of existence, and recommending solutions. Because true globalization, done right, can
    end hunger, and can terminate all wars. May create a better existence for all, via connecting supply
    and demand without bounds. And it will establish a new, peaceful equilibrium.
     Globalization may create a happier human race with higher quality of life and more balance.
      For EVERYBODY. <p>
    &nbsp; &nbsp; The term globalization is used in the context of global cooperation.
    We live in an inseparable entity, our planet, Earth. This is the basis
    for our existence, and the basis for everything else. Please look around for ideas on
    the site, approve or disapprove as you feel, and please help if you so desire. And help
    you can. Every one of us makes an impact.<p>
'''

_mac_main_center = '''

    <td valign=top>
     <table width=100% border=0>
        <tr><td align=center>
        <font size=+2><b>{ header2 } </b></font>
        { mission_statement }
        { fill_data xx }
        <!-- len={ xxDataLen }<br> -->

        <table width=100% border=0>
            <tr valign=top>
            <td valign=middle bgcolor=#cccccc> &nbsp; << &nbsp;
            { article 0 } { article 1 } { article 2 } { article 3 }
            <td valign=middle bgcolor=#cccccc> &nbsp; >>  &nbsp;
         </table>

        <!-- <video width="800" height="600" controls>
          <source src="/media/henryProject_1.mp4" type="video/mp4">
          Your browser does not support the video tag.
            </video>   -->

       <!-- { feed_data } -->

        <table width=100% border=0>
            <tr valign=top>
            { imgrow } { imgrow } { imgrow }
         </table>
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

_glob_site_right = '''
<td width=20% valign=top>
  <table border=0 width=100% cellpadding=3>
    <tr><td bgcolor={ tabhead } height=36 align=center>
        <font size=+1> <b>Misc</b>
    <tr><td>
    <tr><td>
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

#{ xxData0-0 } <br>
#{ xxData0-1 } <br>
#{ xxData0-2 } <br>
#{ xxData0-3 } <br>

def article(strx, context):

    ddd = wsgi_func.parse_args(strx, context)

    sss = '''
    <td>
        <table border=0 bgcolor=#dddddd>
            <tr><td>
            <table border=0 bgcolor=#f5f5f5>
            <tr>
                <tr><td colspan=2>
                <font size=+2> { getData xx %s 1 }
                <tr>
                <td>
                { image beach-hd.jpeg [ thumbwidth ] [ thumbheight ] }
                <td>
                    { getData xx %s 2 }
                <tr><td colspan=2>
                    { getData xx %s 3 }
                <tr><td colspan=2 style="text-alignment:justify">
                    { getData xx %s 4 }<br>
                    { getData xx %s 5 }<br>
                    <!-- { getData xx %s 6 }<br> -->
            </table>
        </table>
    ''' % (ddd[1], ddd[1], ddd[1], ddd[1], ddd[1], ddd[1], )
    return sss

_mac_article2 = '''
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

# Clear text box when the first char is space (empty)
_mac_clr = ''' if(this.value[0]==' ')this.value='' '''

_mac_header2 = '''
    <table width=100% border=0>
        <form method=post>
            <tr><td>
            <a href=index.html>
            <font size=+2><b>Welcome to UPP, </a> </font> <br>
            &nbsp; &nbsp; &nbsp; the site for United Planet Peace
            <!-- (under construction, check back later) --!>

            <td align=right>
                 <font size=-1>Quick feedback:</font>  &nbsp;
                <input type=text name="feedname" onfocus="{ clr }" value=" Your Name" size=10>
                <input type=text name="feedtit"  onfocus="{ clr }" value=" Feddback Title" size=10>
                <input type=text name="feedtxt"  onfocus="{ clr }" value=" Feedback Content" size=12>
                <input type=submit name='feedSUB' value='Submit'>
            <td>
        </form>
    </table>
'''

# ------------------------------------------------------------------------
# Override main macros

_mac_header = '''

    <table width=100% { sitecolor } border=0>
    <tr  height=36>
    <td align=left width=30%> &nbsp; &nbsp; <font size=+2>
     <a href=index.html> <b>{ CompanyName }</b> </a>
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
                <td align=right width=18%>
                Search site: &nbsp; <input type=text value="" size=12>
                <td align=right width=7% >
                <img src=/siteicons/mail-forward.png class=image title="Mail / Contact Us">
                <a href=index.html> <img src=/siteicons/application-exit.png title="Enter / Log In"></a>
    </table>
'''

_glob_site_footer = '''
    <table width=100% { sitecolor }>
        <tr  height=48>
        <td align=left width=45%>
        &nbsp; &nbsp; <font size=+2> <b>Contact Site Admin</b> </font><b>peterglen99@gmail.com</b>
                <td> Copyright (C) Peter Glen; Released to Open Source
                <td align=right>
                    <img src=/siteicons/system-log-out.png class=image title="Log Out / Leave">
                    &nbsp; &nbsp;
    </table>
'''


_mac_imgrow = '''
  <tr>  <td width=10>
  <td width=20>
  <div class=up-class> <font size=+2>Hello rotated text</font></div>

  <td width=10>
     <td align=center>
      <table border=0><tr><td align=center width=400>
       <font size=+2> Image row Header
      { image beach-hd.jpeg [ feedwidth ] [ feedheight ]  }<p>

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

# This adds local the variables pre - marked for a purpose
wsgi_util.add_local_vars( locals().copy(), common.local_table)

# This adds global the variables pre - marked for a purpose
wsgi_util.add_global_vars( locals().copy(), common.local_table)

wsgi_global.add_one_func("article", article)

# EOF
