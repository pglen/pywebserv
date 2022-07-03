 #!/usr/bin/env python3

import os, sys, time

import wsgi_util, wsgi_func, wsgi_data, wsgi_global

''' Local macros and data. Register it after init or use the "_mac_ prefix to auto register
'''

_mac_tabhead = "#ccffcc"
_mac_misscol = "#eeeeee"

_mac_left = '''
<table width=100% border=0>
    <tr><td align=center bgcolor={ tabhead } colspan=2 height=36>
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

_mac_miss_state = '''
    <table width=100% cellpadding=3 border=0>
    { mission_statement }
    </table>
'''

_mac_mission_statement = '''
<tr><td bgcolor={ misscol }>
<font size=-1>Mission Statement:</font>
<font size=+0><br></font>
<font size=+2><center><b>World Wide Globalization Message.</b></center><p></font>
&nbsp; &nbsp; The pace of globalization has exceeded expectations. This institution is searching
for new ways of existance, and recommending solutions. Because true globalization, done right, can
end hunger, and can terminate all wars. May create a better existence for all, via connecting supply
and demand without bounds, and establish a new peaceful equilibrium.
 Globalization may create a happier human race with higher quality of life and more balance.
  For EVERYBODY. <p>
&nbsp; &nbsp; Please do not be misled by the term globalization. It is about global cooperation,
not control. We live in an inseparable global pool, our planet, Earth. This is the basis
for everything else. Please look around for ideas on the site, approve / disapprove as you feel, and help if
you so desire. And help you can. Every one of us makes an impact.<p>
'''

_mac_center = '''

    <td valign=top>
     <table width=100% border=0>
        <tr><td align=center>
        <font size=+2><b>{ header2 } </b></font>
        { miss_state }
        <table width=100% border=0>
            <tr valign=top>
            { article4 } { article } { article2 } { article3 }
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
            &nbsp <img src=siteicons/media-skip-backward.png title="Backward Front">
            &nbsp <img src=siteicons/media-seek-backward.png title=Backward>
            <td width=150px>
            &nbsp; Navigation &nbsp;
            <td align=left>
            &nbsp <img src=siteicons/media-seek-forward.png title=Forward>
            &nbsp <img src=siteicons/media-skip-forward.png title="Forward Front">
</table>
'''

_mac_right = '''

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
            <font size=+2><b>Welcome to UPP Editorxx, </a> </font> <br>
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
    for aa in vvv:
        if "_mac_" in aa[:5]:
            #wsgi_util.append_file("register: " + aa[5:] + "\n")
            wsgi_global.add_one_func(aa[5:],  vvv[aa])
            #wsgi_global.add_one_func(aa,  vvv[aa])
except:
    print("Exception on init vars", sys.exc_info())

# EOF


