 #!/usr/bin/env python3

''' The simplest web server '''

header2 = '''
<form method=post>
    <table width=100% border=0>
        <tr><td>
        <font size=+2><b>Sub Header here.</b></font>
        <td align=right>
            <input type=text name=textx value="Submit Feedback">
            <input type=submit name='hello' value='Submit'>
        <td>
        </table>
</form>
'''

header = '''
    <table width=100% { mycolor } border=0>
    <tr  height=36>
    <td align=left width=22%> &nbsp; &nbsp; <font size=+2> <b>{ Company Name }</b> </font>
            <td>
                <table width=100% border=0>
                    <tr align=center>
                        <td>
                        <td> <a href=index.html>
                            <img src=siteicons/go-home.png class=image title="Back to home page"> </a>
                        <td> <img src=siteicons/emblem-default.png class=image title="Go forward">
                        <td> <img src=siteicons/emblem-unreadable.png class=image title="Blah Blah">
                        <td> <img src=siteicons/emblem-favorite.png class=image title="Favorite">
                        <td>
                </table>
                <td align=right width=18%>
                Search: &nbsp; <input type=text value="" size=12>
                <td align=right width=7% >
                <img src=siteicons/mail-forward.png class=image title="Mail / Contact Us">
                <img src=siteicons/application-exit.png title="Enter / Log In">
    </table>
'''

footer = '''
    <tr  height=48>
    <td align=left width=45%>
    &nbsp; &nbsp; <font size=+2> <b>Contact</b> </font><b>peterglen99@gmail.com</b>
            <td> Copyright (C) Open Source
            <td align=right>
                <img src=siteicons/system-log-out.png class=image title="Log Out / Leave">
                &nbsp; &nbsp;
'''

imgrow = '''
  <tr><td>
     { image beach-hd.jpeg [ thumbwidth ] [ thumbheight ] }
      <td width=10>
      <td> Image description Image description3
      Image description
      Image description Image description Image description Image description Image description
'''

article = '''
    <td>
        <table border=0 bgcolor=#dddddd>
            <tr><td>
            <table border=0 bgcolor=#eeeeee>
            <tr>
                <tr><td colspan=2>
                <font size=+2>Article header, longer one
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

article2 = '''
    <td>
        <table border=0 bgcolor=#dddddd>
            <tr><td>
            <table border=0 bgcolor=#f5f5f5>
            <tr>
                <tr><td colspan=2>
                <font size=+2>Article header, longer one
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

bigtext = '''
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { image beach-hd.jpeg 100 }   <p>
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.                `
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                hello
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                hello<br>
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                hello
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
                { var } substitution is { no problem } here.
'''

# EOF