#!/usr/bin/env python3

'''
     This is a sample project macro file;
        Variables start with "_mac_" will become local macros, that can be
        referenced on this page.
        Variables start with "_func_" wil become functions that can be
        referenced on this page.

        Variables start with "_glob_" wil become global that can be
        referenced on the whole site.

      To see where things expand, and what they expand to, use the -s
    option on the command line.

     To see it in the rendered HTML, as comments use the -i option.
    Only function expansions will show, as comments inside tags are
    not allowed. (vars may appear inside tags)

     This file is imported under a try: except clause, so ordinarily,
    nothing in this file can down the site.

      This file can only down this page. (for example a syntax
      error) However, some conditions (like missing site dependencies)
      CAN down the site.

'''

import os, sys, time

import wsgi_util, wsgi_func, wsgi_data, wsgi_global

''' Local macros and data. Register it after init or use the _mac_ prefix to auto register
'''

from . import common

_glob_siteemail =  "admin@unitedplanetpeace.com"
_glob_tabhead   = "#ccffcc { tabhead }"
_glob_misscol   = "#eeeeee"

# String parsed before function
_glob_sitecolor = "#aaffbb"

#def _func_sitecolor(strx, context):
#    return "#aaffff"

_mac_CompanyName = '''UPP the United Planet Peace'''

_glob_sitestyle = '''

<style>

* {
  box-sizing: border-box;
}

   div {
    display: block;
}

body {
  font-family: Arial;
  padding: 10px;
  background: #f1f1f1;
}

/* Header/Blog Title */
.header {
  /*padding: 30px;*/
  text-align: center;
  background: white;
}

.header h1 {
  font-size: 50px;
}

/* Style the top navigation bar
.topnav {
  overflow: hidden;
  background-color: #333;
}
*/

/* Style the topnav links
.topnav a {
  float: left;
  display: block;
  color: #f2f2f2;
  text-align: center;
  padding: 14px 16px;
  text-decoration: none;
}
*/

/* Change color on hover
.topnav a:hover {
  background-color: #ddd;
  color: black;
}
*/

/* -------------------------------------------------------------------- */
/* Column container */

.row {
  display: flex;
  flex-direction: row;
  flex-wrap: nowrap;
}

/* Left column */
.leftcolumn {
  flex: 25%;
  background-color: #f1f1f1;
  padding-left: 20px;
  /*visibility: collapse;*/
  /*overflow: hidden;*/
}
/* Mid column */
.midcolumn {
  flex: 50%;
  background-color: #f1f1f1;
  padding-left: 20px;
}
/* Right column */
.rightcolumn {
  flex: 25%;
  background-color: #f1f1f1;
  padding-left: 20px;
}

/* -------------------------------------------------------------------- */

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
    background-color:  #aaffaa;
}
.textx {
    border-radius: 10px;
    background-color:  #cccccc;
    padding: 10px;
    max-width: 800px;
}

@media (max-width:600px) {

    .row {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
    }

    .midcolumn {
      flex: 100%;
      order: 1;
      background-color: white;
      padding: 20px;
    }
    .leftcolumn {
      flex: 100%;
      order: 2;
      background-color: #f1f1f1;
      padding: 20px;
    }
    .rightcolumn {
      order: 3;
      flex: 100%;
      background-color: white;
      padding: 20px;
    }
}

@media (min-width:600px) and (max-width:1000px) {

  .row {
      display: flex;
      flex-direction: row;
      flex-wrap: wrap;
    }

    .leftcolumn {
      background-color: #f1f1f1;
      padding: 20px;
      flex: 25%;
    }
    .midcolumn {
      background-color: white;
      padding: 20px;
      flex: 75%;
    }
    .rightcolumn {
      background-color: white;
      padding: 20px;
      flex: 100%;
    }
}

</style>

<script language="javascript">
function toggle(tt, dt) {
    var ele = document.getElementById(tt);
    var text = document.getElementById(dt);
    if(ele.style.display == "block") {
            ele.style.display = "none";
        text.innerHTML = "<font size=-1>show again ...</font>";
    }
    else {
        ele.style.display = "block";
        text.innerHTML = "<font size=-1>hide</font>";
    }
}
</script>

'''

def _glob_headurl(strx, context):

    # Expand arguments
    sss = wsgi_func.parse_args(strx, context)
    #print("args spaced:", sss)

    rrr = '''
        <tr>
        <td width=50%%> &nbsp;
        <td valign=center>
                <a href=%s>
                <img src=/siteicons/dot.png />
                </a>
        <td> &nbsp;
        <td align=left>
        <font size=+1>
        <a href=%s> %s </a><br>
        <td width=50%%> &nbsp;
    ''' % (sss[1], sss[1], sss[2])

    return rrr

_glob_site_left = '''

    <table border=0 align=center width=100%>
        <tr><td bgcolor={ tabhead } align=center colspan=3 height=36>
            <font size=+1><b>Main Navigation</b>
        <tr>
            <td height=6>
        <tr>
            <td width=50%> &nbsp;
            <td align=center>
                <img src="/media/upp.png" title="Main">
            <td width=50%> &nbsp;
        <tr>
            <td> &nbsp;
            <td>
                <a href=/index.html>
                <img src="/media/united_planet_logo_300.png" title="Main Logo">
                </a>
            <td> &nbsp
    </table>

    <table border=0 align=center width=100%>
        <tr>
        { headurl index.html Home&nbsp;Page }
        { headurl log.html Log&nbsp;Page }
        { headurl index.html Blog&nbsp;Page }
        { headurl index.html Personal&nbsp;Page }
        { headurl index.html Tech&nbsp;Page }
        { headurl index.html Another&nbsp;Page }
        { headurl broken.html Broken&nbsp;Page }

        <tr><td height=12>
    </table>

'''

_mac_mission_statement = '''


    <font size=-1>Mission Statement:</font>
    <a id="displayText" href="javascript:toggle('toggleText', 'displayText');">
        <font size=-1>show</font></a>

    <div id="toggleText" style="display: none">
        <font size=+1><center><b>World Wide Globalization Message.</b></center><p></font>
        <div style="text-align: justify;">
        &nbsp; &nbsp; The pace of globalization has exceeded expectations. This institution is searching
        for new ways of co-existence, and recommending solutions. Because true globalization, done right, can
        end hunger, and can terminate all wars. May create a better existence for all, via connecting supply
        and demand without bounds. And it will establish a new, peaceful equilibrium.
         Globalization may create a happier human race with higher quality of life and more balance.
          For EVERYBODY. <p>
        &nbsp; &nbsp; The term globalization is used in the context of global cooperation.
        We live in an inseparable entity, our planet, Earth. This is the basis
        for our existence, and the basis for everything else. Please look around for ideas on
        the site, approve or disapprove as you feel, and please help if you so desire. And help
        you can. Every one of us makes an impact.<p>
        </div>
    </div>

'''

#<tr><td fgcolor=white style="bgcolor: { xmisscol }; color:black">

_mac_founding_statement = '''

    <font size=-1>Founding Statement:</font>
    <a id="displayText2" href="javascript:toggle('toggleText2', 'displayText2');">
        <font size=-1>show</font></a>
    <div id="toggleText2" style="display: none">
        <font size=+1><center><b>The Founding Father's and Founding Mother's era.</b></center><p></font>
        <div style="text-align: justify;">
        &nbsp; &nbsp; Many countries have gone through their democratic \"Founding\" era. An era
        in which a system of justice is established. An equitable order of distributing
        power and resources is created, which assures fair and equal representation for all.
        &nbsp; &nbsp; However, some countries have not gone through this 'Founding' era. The UPP is set out to bring
        this Founding Father's and Founding Mother's era to the whole planet.<br>
        </div>
    </div>
'''

#<tr><td fgcolor=white style="bgcolor: { xmisscol }; color:black">

_mac_target_statement = '''


    <font size=-1>Target Statement:</font>
    <a id="displayText3" href="javascript:toggle('toggleText3', 'displayText3');">
    <font size=-1>show</font></a>
    <div id="toggleText3" style="display: none">
        <font size=+1><center><b>Uniform Global Standards for Governance</b></center></font>
        <div style="text-align: justify;"><br>
        &nbsp; &nbsp; There are plenty of organizations to help each other in
        cooperating internationally; mostly aiding / controlling inter-governmental
        affairs. And there are plenty of enforcement instruments.
        However, the most important instrument is missing: Containment of the
        Leadership. In the twenty first century, there should be standards of
        leadership, standards of govenance and especally, standards for justice.
        Term limits for every position. High standards for democracy, accountability and equality.
        UPP is set out to create a framework where these shortcomings are addressed.
        Globally. The whole planet.<p>
        </div>
    </div>
'''

def _func_calcwrap(strx, context):

    dbsize = len(context.res)

    if context.prog >= dbsize - 3:
        cont = "&nbsp; &nbsp; -- &nbsp; &nbsp;"
    else:
        cont = "&nbsp; << &nbsp;"
    return cont

def _func_calcwrap2(strx, context):

    if context.prog <= 0:
        cont = "&nbsp;&nbsp; -- &nbsp;&nbsp;"
    else:
        cont = "&nbsp; >> &nbsp;"
    return cont


_mac_main_center = '''

     <table border=0>
        <tr><td align=center>
        <font size=+2><b>{ header2 } </b></font>
        <table border=0 width=100%>
            <tr><td>
            Read our Mission / Founding / Target statments
            <a id="displayText4" href="javascript:toggle('toggleText4', 'displayText4');">
            <font size=-1>show ...</font></a>

            <tr><td>
                <div id="toggleText4" style="display: none">
                    <div>
                    <table border=0 width=100%>
                        <tr><td>&nbsp; &nbsp; { mission_statement }
                        <tr><td>&nbsp; &nbsp; { founding_statement }
                        <tr><td>&nbsp; &nbsp; { target_statement }
                     </table>
                    </div>
                </div>
            </table>
        </table>

        <table border=0>
            <tr valign=top>
             <td nowrap=nowrap valign=middle bgcolor=#cccccc
                style="cursor:pointer"
                    onclick="location.href='index.html?step={ calcstep 1 }'">
                { calcwrap }

            { article 0 }
            <td valign=middle bgcolor=#cccccc>
            { article 1 }
            <td valign=middle bgcolor=#cccccc>
            { article 2 }

             <td  nowrap=nowrap valign=middle bgcolor=#cccccc
                style="cursor:pointer"
                    onclick="location.href='index.html?step={ calcstep -1 }'">
                { calcwrap2 }

         </table>

       <!-- { feed_data } -->

        <table border=0>
            <tr valign=top>
            { imgrow } { imgrow } { imgrow }
         </table>
    </table>


'''

_mac_nav = '''
<table border=0>
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

# This one is made global

_glob_site_right = '''

  <!-- <td width=20% valign=top> -->

  <table border=0 width=100% cellpadding=3>
    <tr><td bgcolor={ tabhead } height=36 align=center>
        <font size=+1> <b>Misc</b>
    <tr><td>
    <tr><td align=center>
        &nbsp; &nbsp;
        <b>Last column, maybe ads</b><p>
        cogito ergo sum cogito ergo sum cogito ergo sum
        cogito ergo sum cogito ergo sum cogito ergo sum
        cogito ergo sum cogito ergo sum cogito ergo sum
        <br>
        { app_one } <p>
        { app_two } <p>
</table>
'''

# Get new value of the step for

def _func_calcstep(strx, context):

    ddd = wsgi_func.parse_args(strx, context)
    #print("ddd", ddd)

    if hasattr(context, "prog"):
        newval =  context.prog + int(ddd[1])
        dbsize = len(context.res)
        #print("dbsize", dbsize)
        if newval > dbsize - 3:
            newval = dbsize-3
        if newval < 0:
            newval = 0
        return str(newval)
    else:
        return "0"

def _func_article(strx, context):

    ddd = wsgi_func.parse_args(strx, context)

    #print("ddd", ddd)
    #print("article res", context.res)
    #print("_func_article", context)

    if not hasattr(context, "prog"):
        context.prog = 0

    idx = context.prog + int(ddd[1])
    res = context.res

    #print("res[0]", res[0])

    sss = '''
    <td>
        <table border=0 bgcolor=#dddddd>
            <tr><td>
            <table border=0 bgcolor=#f5f5f5>
            <tr>
                <tr><td colspan=2>
                <font size=+2> %s
                <tr>
                <td>
                { image beach-hd.jpeg [ thumbwidth ] [ thumbheight ] }
                <td>
                    %s
                <tr><td colspan=2>
                <tr><td colspan=2 style="text-alignment:justify">
                    %s<br>
                    %s<br>
            </table>
        </table>
    ''' % ( res[idx][2], res[idx][3], res[idx][4], res[idx][5])

    return sss

_mac_article5 = '''Hello'''

_mac_art_header = '''Header here'''

# Clear text box when the first char is space (empty)
_mac_clr = ''' if(this.value[0]==' ')this.value='' '''

_mac_header2 = '''
    <table width=100% border=0>
        <form method=post>
            <tr><td>
            <a href=index.html>
            <font size=+2><center><b>Welcome to UPP, </a> </center></font> <br>

            <!-- &nbsp; &nbsp; &nbsp; the site for United Planet Peace -->
            <!-- (under construction, check back later) --!>

            <td align=right>
                 <font size=-1>Quick feedback:</font>  &nbsp;
                <input type=text name="feedname" onfocus="{ clr }" value=" Your Name" size=10>
                <input type=text name="feedtit"  onfocus="{ clr }" value=" Feddback Title" size=10> <br>
                <input type=text name="feedtxt"  onfocus="{ clr }" value=" Feedback Content" size=12>
                <input type=submit name='feedSUB' value='Submit'>
            <td>
        </form>
    </table>
'''

# ------------------------------------------------------------------------
# Override main macros

_glob_header = '''

    <table width=99% bgcolor={ sitecolor } border=0>
    <td align=center width=30%> &nbsp; &nbsp;
    <font size=+2>
        <a href=index.html><b>{ CompanyName }</b></a>
    </font><br>
     <font color=red>
         Please Note, that Site is Under Construction
     </font>
            <td align=center>
                <table width=100%  border=0>
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

#_glob_site_footer = '''
_glob_footer = '''
    <table width=100%  border=0>
        <tr><td width=100% colspan=3>
        <img src=/media/city_scape_xsmall.png width=100%>
        <tr><td>
        <table  width=100% bgcolor={ sitecolor }>
            <tr>
            <td align=center width=30%>
                    &nbsp; &nbsp; <font size=+2>
                    <b>Contact Site Admin</b></font><br>
                    <b>{ siteemail }</b>

            <td align=center >
                Copyright (C) Peter Glen; <br>Site Source Released under Open Source
            <td align=right>
                <img src=/siteicons/system-log-out.png class=image title="Log Out / Leave">
                &nbsp; &nbsp;
        </table>
    </table>
'''

_mac_feed_data = ''' FD '''

_mac_imgrow = '''
  <tr>  <td width=10>
  <td width=20>
  <!-- <div class=up-class> <font size=+2>Hello rotated text</font></div> -->

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

wsgi_util.add_all_vars(locals().copy(), common.local_table)

#wsgi_util.dump_global_table()
#wsgi_util.dump_local_table(common.local_table)

# EOF
