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

_glob_siteemail =   "admin@unitedplanetpeace.com"
_glob_tabhead   =   "#ccffcc { tabhead }"
_glob_misscol   =   "#eeeeee"

# String parsed before function
_glob_sitecolor = "#aaffbb"

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

/* Header/Blog Titlefor(int aa = 0; aa < limx; aa++)
    {
    // Do stuff
    }
 */
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

.imgflex {
  opacity: 1;
  display: inline;
  height: auto;
  transition: .5s ease;
  backface-visibility: hidden;
  border-radius: 15px;
  width: 600px;
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
  backface-visibility: hidden;                                 
  corner-radius: 0px;
}

.img_round {
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

//.container:hover .image {
//  opacity: 0.3;
//}

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
    background-color:  #dddddd;
    padding: 10px;
    max-width: 800px;
    text-align: justify;
}

/* The Modal Dialog ------------------------------------------------- */

.Clicker {
  cursor: pointer;
}

.modal {
  //display: none; /* Hidden by default */
  position: fixed; /* Stay in place */
  z-index: 1; /* Sit on top */
  //right: 0;
  right: 0;
  bottom: 0;
  //width: 50%; /* Full width */
  //height: 10%;
  overflow: auto; /* Enable scroll if needed */
  background-color: rgba(255,255,255,0.8); /* Black w/ opacity */
}

/* Modal Content */
.modal-content {
  //bottom: 0;
  //background-color: #fefefe;
  //width: 90%;
  /* height: 100%; */

}

/* The Close Button */
.closebutt {
  color: black;
  float: right;
  font-size: 28px;
  font-weight: bold;
}

.closebutt:hover,
.closebutt:focus {
  color: #000;
  text-decoration: none;
  cursor: pointer;
}

.modal-header {
  padding: 2px 2px;
  //background-color: #eeeeee;
  //5cb85c;
  //color: black;
  //width = 100%

}

.modal-body {
    padding: 8px 8px;
    display:inline;
    float:left;
    font-size: 18px;
    }

.modal-footer {
  padding: 2px 8px;
  //background-color: #eeeeee
  //5cb85c;
  color: black;
}

 /* Popup container ---------------------------------------- */

.popup {
  position: relative;
  display: inline-block;
  cursor: pointer;
}

/* The actual popup (appears on top) */
.popup .popuptext {
  visibility: hidden;
  width: 160px;
  background-color: #555;
  color: #fff;
  text-align: center;
  border-radius: 6px;
  padding: 8px 0;
  position: absolute;
  z-index: 1;
  bottom: 125%;
  left: 50%;
  margin-left: -80px;
}

/* Popup arrow */
.popup .popuptext::after {
  content: "";
  position: absolute;
  top: 100%;
  left: 50%;
  margin-left: -5px;
  border-width: 5px;
  border-style: solid;
  border-color: #555 transparent transparent transparent;
}

/* Toggle this class when clicking on the popup container (hide and show the popup) */
.popup .show {
  visibility: visible;
  -webkit-animation: fadeIn 1s;
  animation: fadeIn 1s
}

/* Add animation (fade in the popup) */
@-webkit-keyframes fadeIn {
  from {opacity: 0;}
  to {opacity: 1;}
}

@keyframes fadeIn {
  from {opacity: 0;}
  to {opacity:1 ;}
}

/* Media ----------------------------------------------------------- */

@media (max-width:500px) {

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
    .imgflex {
      opacity: 1;
      display: inline;
      height: auto;
      transition: .5s ease;
      backface-visibility: hidden;
      width: 300px;
      //border-radius: 0px;
      }
}

@media (min-width:500px) and (max-width:1000px) {

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
    .imgflex {
      opacity: 1;
      display: inline;
      height: auto;
      transition: .5s ease;
      backface-visibility: hidden;
      border-radius: 15px;
      width: 500px;
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

function toggle3(pp, tt, dt) {
    var pre = document.getElementById(pp);
    var ele = document.getElementById(tt);
    var textx = document.getElementById(dt);
    if(ele.style.display == "block") {
        ele.style.display = "none";
        pre.style.display = "block";
        textx.innerHTML = "<font size=-1>Show More ...</font>";
    }
    else {
        ele.style.display = "block";
        pre.style.display = "none";
        textx.innerHTML = "<font size=-1>Show Less ...</font>";
    }
}

// When the user clicks on <div>, open the popup
function myFunction() {
  var popup = document.getElementById("myPopup");
  popup.classList.toggle("show");
}

function setCookie(c_name, value, exdays) {
    var exdate = new Date();
    exdate.setDate(exdate.getDate() + exdays);
    var c_value = escape(value) + ((exdays == null) ? "" : \
            "; expires=" + exdate.toUTCString() + ";SameSite=Strict");
    document.cookie = c_name + "=" + c_value;
    console.log(document.cookie)
}

// Declare modal globals
var mymodal_0, mymodal_1, mymodal_2

window.onload = function  myLoad() {

    mymodal_0 = document.getElementById("myModal_0")
    mymodal_1 = document.getElementById("myModal_1")
    mymodal_2 = document.getElementById("myModal_2")

    //var elements = document.getElementsByClassName("closebutt");
    var element = document.getElementById("cbx");
    //console.log("elem " + element)

    var myFunction = function() {
        // close it
        var ddd = document.getElementById("modx");
        console.log("ddd " + ddd)
        ddd.style.display = "none"
        //ddd.z-index = 1;
        //alert(this);
        setCookie("WasAck",  "OK", 1);

    };
    element.addEventListener('click', myFunction, false);

    /* console.log("myLoad") */

    // Take care of closing
    ccc = document.getElementById("myContent_0")
    // When the user clicks on body of popup, close the modal
    ccc.addEventListener("keydown", function(event)
        {
        /* console.log("key event listener" + event) */
        mymodal_0.style.display = "none";
        event.stopPropagation()
        })
    // The close triggers for click
    ccc.addEventListener("click", function(event)
        {
        mymodal_0.style.display = "none";
        event.stopPropagation()
        })

    ccc = document.getElementById("myContent_1")
    // When the user clicks on body of popup, close the modal
    ccc.addEventListener("keydown", function(event)
        {
        /* console.log("key event listener" + event) */
        mymodal_1.style.display = "none";
        event.stopPropagation()
        })
    // The close triggers for click
    ccc.addEventListener("click", function(event)
        {
        mymodal_1.style.display = "none";
        event.stopPropagation()
        })
    ccc = document.getElementById("myContent_2")
    // When the user clicks on body of popup, close the modal
    ccc.addEventListener("keydown", function(event)
        {
        /* console.log("key event listener" + event) */
        mymodal_2.style.display = "none";
        event.stopPropagation()
        })
    // The close triggers for click
    ccc.addEventListener("click", function(event)
        {
        mymodal_2.style.display = "none";
        event.stopPropagation()
        })

    // Take care of openining
    ooo = document.getElementById("clicker_0")
    ooo.addEventListener("click", function(event)
        {
        mymodal_0.style.display = "block";
        fff = document.getElementById("txt_0");
        fff.focus()
        event.stopPropagation()
        });
    ooo = document.getElementById("clicker_1")
    ooo.addEventListener("click", function(event)
        {
        mymodal_1.style.display = "block";
        fff = document.getElementById("txt_1");
        fff.focus()
        event.stopPropagation()
        });
    ooo = document.getElementById("clicker_2")
    ooo.addEventListener("click", function(event)
        {
        mymodal_2.style.display = "block";
        fff = document.getElementById("txt_2");
        fff.focus()
        event.stopPropagation()
        });
    }

//console.log("Loading page")

// When the user clicks anywhere outside of the modal, close it
window.onclick = function(event) {
  if (event.target == mymodal_0) {
    mymodal_0.style.display = "none";
    }
  if (event.target == mymodal_1) {
    mymodal_1.style.display = "none";
    }
  if (event.target == mymodal_2) {
    mymodal_2.style.display = "none";
  }
}

// Clear text box when the first char is space (empty)
function clr(zz) {

    if(zz.value[0]==' ') zz.value=''
}

</script>

'''
# Clear text box when the first char is space (empty)
_mac_clr = ''' if(this.value[0]==' ') this.value='' '''

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
        { headurl /index.html Home&nbsp;Page }
        { headurl /docs/ Documents&nbsp;Page }
        { headurl /misc/ Misc&nbsp;Page }
        { headurl /donate/ Donation&nbsp;Page }
        { headurl /about/ About&nbsp;Page }
        <!--
        {headurl index.html Personal&nbsp;Page }
        {headurl log.html Log&nbsp;Page }
        {headurl index.html Tech&nbsp;Page }
        {headurl index.html Another&nbsp;Page }
        {headurl broken.html Broken&nbsp;Page }
        -->

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
        end hunger, end violence and can terminate all wars. May create a better existence for all, via connecting supply
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
        &nbsp; &nbsp; There are plenty of organizations to help in
        cooperating internationally; aiding / controlling inter-governmental
        affairs. And there are plenty of enforcement instruments.
        However, the most important instrument is missing: Containment of the
        Leadership. In the twenty first century, there should be standards of
        leadership, standards of govenance and especally, standards for justice.
        Term limits for every position. High standards for democracy, accountability and equality.
        UPP is set out to create a framework where these shortcomings are addressed.
        Globally. For the whole planet.<p>
        </div>
    </div>
'''

_mac_center_body = '''

    <td>
     <table width=100% border=0>
        <tr><td align=center colspan=2>
        { linemessage }
        { subheader }
        <table border=0 width=100%>
            <tr><td>
            Read our Mission Statement  / Founding Statement
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
                { add_popup }
                { nav }
                { imgrow 0 }
                { imgrow 1 }
                { imgrow 2 }
                { imgrow 3 }
                { imgrow 4 }
                { nav }
         </table>

    </table>


'''

def _func_nav(strx, context):

    res = getattr(context, "proj-rows").res
    dbsize = len(res)
    bbb = max(0, context.prog -1)
    eee = min(dbsize-1, context.prog +1)
    strx = '''
<table border=0 width=100%%>
    <tr align=center>
        <td align=right>
            <a href=index.html?seek=%d>
            &nbsp <img src=/siteicons/media-skip-backward.png title="Back to start">
            </a>
            <a href=index.html?seek=%d>
            &nbsp <img src=/siteicons/media-seek-backward.png title=Backward>
            </a>
            <td width=150px>
            &nbsp; Navigation &nbsp;
            <td align=left>
            <a href=index.html?seek=%d>
            &nbsp <img src=/siteicons/media-seek-forward.png title=Forward>
            </a>
            <a href=index.html?seek=%d>
            &nbsp <img src=/siteicons/media-skip-forward.png title="Forward to end">
            </a>
</table>
''' % (0, bbb, eee, dbsize -1)
    return strx

# This one is made global

_glob_site_right = '''

  <!-- <td width=20% valign=top> -->

  <table border=0 width=100% cellpadding=3>
    <tr><td bgcolor={ tabhead } height=36 align=center>
        <font size=+1> <b>Misc</b>
    <tr><td>
    <tr><td align=center>
        { app_fortune } <p>
        { app_one } <p>
        { calendar } <p>
</table>
'''

def calcstep(ddd, context):

    if not hasattr(context, "prog"):
        context.prog = 0

    res = getattr(context, "proj-rows").res

    newval =  context.prog + int(ddd)
    dbsize = len(res)
    print("dbsize", dbsize)

    if newval > dbsize - 1:
        newval = dbsize - 1
    if newval < 0:
        newval = 0

    context.prog = newval

# Get new value of the step for

def _func_calcstep(strx, context):

    ddd = wsgi_func.parse_args(strx, context)
    #print("ddd", ddd)
    calcstep(ddd[1], context)

#<!-- The Modal dialog -->

def add_modal(img, num = 0):

    #print("control", num)

    sss = '''
    <div id="myModal_%d" class="modal">
      <!-- Modal content -->
      <div id=myContent_%d class="modal-content">
            <div class="modal-header">
            <span class="closebutt">&times;</span>
            <h2><center>Image preview. Click to close.</h2>
            </div>
        <div class="modal-body">
          <center>
          { image %s 1000 }

          <div style="width=0; overflow:hidden; opacity: 0">
            <!-- hidden for focus -->
            <input type=button id=txt_%d value="Close">
          </div>
        </div>
        <!-- <div class="modal-footer"> -->
        <!--     <h2>&nbsp;</h2> -->
        <!-- </div> -->
      </div>
    </div>
    <div class=Clicker id=clicker_%d><font size=-2>Show Image</font>
    </div>
    ''' % (num, num, img, num, num)
    #print("sss", sss)
    return sss

def _func_add_popup(strx, context):

    #print("cooki seen", context.mainclass.good_cookies)

    if  " WasAck" in context.mainclass.good_cookies:
        #print("cooki seen")
        return ""

    sss = '''
       <div class="modal" id="modx">
          <!-- Modal content -->
          <div id=myContent_%d class="modal-content">
                <div class="modal-body">
                This site contains minimal, limited number of cookies.
                Click to close. &nbsp;
                 <span class="closebutt" id=cbx >&times;</span>
                </div>
            <div>
        </div>
    </table>
    ''' # % ("hello", "hello")
    return sss

_mac_subheader = '''
    <table width=100% border=0>
        <!-- <form method=post> -->
            <tr><td align=center>
            <font size=+3><b>Welcome to UPP</b></font>
            <tr><td align=center>
            <font size=+2>The site for Planetary Peace and Justice.</font>

            <!-- (under construction, check back later) --!>
            <!--
            <td align=right>
                <font size=-1>Quick feedback:</font>  &nbsp;
                <input type=text name="feedname" onfocus="clr(this)" value=" Your Name" size=10>
                <input type=text name="feedtit"  onfocus="{ clr }" value=" Feedback Title" size=10> <br>
                <input type=text name="feedtxt"  onfocus="{ clr }" value=" Feedback Content" size=12>
                <input type=submit name='submit' value='Submit'>
            <td>
            -->
        <!-- </form> -->
        <td height=12>

    </table>
'''


def     _glob_calendar(strx, context):

    '''
    Mock calendar. Does nothing but presents a calendar looking user interface,
    and links the message on no cal
    '''
    import datetime
    try:
        content = '''<table width=100% border=0  bgcolor=#dddddd>
            <tr><td align=center bgcolor=#cccccc colspan=7><b>Event Calendar</b><br>
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

                    content += "<td align=center nowrap=nowrap bgcolor=" + bgcolor + ">"
                    decor = 0
                    #if random.randint(0, 255) % 4 == 0:
                    #    decor = 1;

                    decor = cnt2 % 4 == 0
                    content += "<font size=-1>"
                    if decor:
                        content += "<a href=/index.html?message=No%20Calendar%20Events>"
                    else:
                        content += " &nbsp; "

                    content += "%2d" % cnt2

                    if decor:
                        content += "*</a>"
                    else:
                        content += " &nbsp; "

                else:
                    content += "<td align=center> "

        content += "<tr><td colspan=7 align=center><font size=-2>"
        content += "** Calendar events are subject to change"

        content += "</table>\n"

    except:
        wsgi_util.put_exception("Exception on app_two_func")

        # Note that we still complete the table, so the site keeps going
        content += "</table>\n"

    return content

# ------------------------------------------------------------------------
# Override main macros

_glob_header = '''

    <table width=99% bgcolor={ sitecolor } border=0>
    <td align=center width=30%> &nbsp; &nbsp;
    <font size=+2>
        <a href=/index.html><b>{ CompanyName }</b></a>
    </font><br>
     <!--<font color=red>
         Please Note, that Site is Under Construction
     </font>   -->
            <td align=center>
                <table width=100%  border=0>
                    <tr align=center>
                        <td>
                        <td> <a href=/index.html>
                            <img src=/siteicons/go-home.png class=image title="Back to home page">
                            </a>
                        <td>
                        <a href=/donate/index.html?main>
                        <img src=/siteicons/emblem-default.png class=image title="Donate">
                        </a>
                        <td>
                        <a href=/about/index.html?subscribe>
                        <img src=/siteicons/emblem-unreadable.png class=image title="About">
                        </a>
                        <td>  <a href=/index.html?favorite>
                        <img src=/siteicons/emblem-favorite.png class=image title="Favorite">
                            </a>
                        <td>
                </table>
                <!--
                <td align=right width=22%>
                <form method=submit>
                Search site: &nbsp; <input name=search type=text value="" size=12>
                <input type=submit  value=Go></form>
                -->
                <td align=right width=7% >
                <a href=mailto:admin@unitedplanepeace.com>
                <img src=/siteicons/mail-forward.png class=image title="Mail / Contact Us">
                </a>
                <a href=index.html?exit> <img src=/siteicons/application-exit.png title="Enter / Exit"></a>
    </table>
    '''

_glob_site_footer = '''
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

def _func_imgrow(strx, context):

    ddd = wsgi_func.parse_args(strx, context)

    if not hasattr(context, "prog"):
        context.prog = 0

    idx = context.prog + int(ddd[1])
    res  = getattr(context, "proj-rows").res

    #print("ddd", ddd, context.prog)

    if not res:
        # Patch in something
                # ID Key  D1        Side Main                Under             Image
        res = [
                ["", "", "No Data", "No description", "Database is empty", "System Message: Under development", "X"],
                ["", "", "No Data", "No description", "Database is empty", "System Message", "X"],
                ["", "", "No Data", "No description", "Database is empty", "System Message", "X"],
              ]
    #print("res", res)

    if not res[idx][6] or res[idx][6] == 'none':
        imn =   "beach-hd.jpeg"
    else:
        imn = res[idx][6]

    sss =  '''
    <tr> <td width=10>
    <td width=20>
    <td width=10>
     <td align=center>
      <table border=0 width=100%%>
          <tr><td align=center colspan=1>
           <font size=+2> %s
            </font>
           <tr><td align=center>
           <div>
           <a href=/media/%s>
           { image %s [ 600 ] }
           </a>
           <br> <center> %s </center>
           </div>
           <tr>
           <td align=center>
          <!--Image description Image description -->
            %s
          <tr><td colspan=1>
             <div class=textx>
              <!-- Image row text Image row text Image row text Image row textx -->
             %s
              </div>
              <p>
        </table>
        ''' % (res[idx][2], imn, imn,
                        res[idx][5], res[idx][3], res[idx][4])

    #print("img", res[idx][6] )

    return sss

messagex = "none"

def _func_linemessage(strx, context):
    #print("messagexx", messagex)
    return messagex

def     _glob_app_one(strx, context):

    ''' Advert app function '''

    content = '''<table width=100% border=0 bgcolor=#dddddd>
        <tr><td align=center bgcolor=#cccccc><b>Sponsored</b><br>
        <tr><td>
        <tr><td  align=center>No Sponsors currently. Please become a sponsor, so
                    you can tell future generations what you helped with.
        <tr><td>
        <tr><td align=center><font size=-2>
            Contact admin for Advertising in this Space.

        </table>

        '''
    return content

wsgi_util.add_all_vars(locals().copy(), common.local_table)

#wsgi_util.dump_global_table()
#wsgi_util.dump_local_table(common.local_table)

# EOF
