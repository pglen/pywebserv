 #!/usr/bin/env python3

import sys

''' Local macros and data. Register it after init or use the "_mac_ prefix to auto register
'''

local_table = []

# ------------------------------------------------------------------------
# Add a new project function;

def     add_local_func(mname, mfunc, mpage = None, fname=None):

    global local_table

    #print("local_func:", mname)

    '''
         Add a macro function or string here. The macro is substituted
        by the output of the function.
    '''
    try:
        #see if there is an entry already
        for aa in local_table:
            if aa[0] == mname:
                print("Duplicate macro", mname)
                return True
        local_table.append([mname, mfunc])
    except:
        print("Cannot add local table item", sys.exc_info())
    return False


_mac_tabhead = "#ccffcc"
_mac_misscol = "#eeeeee"

_mac_miss_state = '''
    <table width=100% cellpadding=3 border=0>
    { mission_statement }
    </table>
'''
_mac_ShortCName = '''
    United Planet Peace
    '''

_mac_header_edit = '''
header here
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

_mac_center_body = '''

    <table width=100% border=1>
        <tr><td align=center colspan=3>
        Edit main rows
        { imgrow }
    </table>

'''

_mac_mission_statement2 = '''
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
                #print("Added:", aa[5:]) #, vvv[aa][:12])
                pass
            add_local_func(aa[5:], vvv[aa])

    #print("Local table len", len(local_table))
    #
    #print ("local table")
    #for aa in local_table:
    #    print(" '" + aa[0] + "'", end = " ")
    #print ("\ntable end")

except:
    #print("Exception on editor init vars", sys.exc_info())
    print_exception("Editor")
    raise

# EOF











