''' The simplest web server '''

# These strin resources are the macro bodies

mystyle = '''
<style>
.container {
  position: relative;
  width: 50%;
}

.image {
  opacity: 1;
  display: inline;
  height: auto;
  transition: .5s ease;
  backface-visibility: hidden;
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

</style>
'''

header = '''
    <table width=100% { mycolor } border=0>
    <tr  height=36>
    <td align=left width=22%> &nbsp; &nbsp; <font size=+2> <b>Company Name</b> </font>
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
                <img src=siteicons/application-exit.png title="Exit /  Log Out">
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

