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
    <tr  height=36>
    <td Align=left> &nbsp; &nbsp; <font size=+2> <b>Company name</b> </font>
            <td> &nbsp Icon Here<td align=right>
                <img src=icons/mail-forward.png class=image title="Mail / Contacr us">
                <img src=icons/address-book-new.png class=image title="Address book">
                <img src=icons/application-exit.png title="Exit /  Log out">
                &nbsp; &nbsp;
'''

footer = '''
    <tr  height=48>
    <td Align=left> &nbsp; &nbsp; <font size=+2> <b>Contact</b> </font>
            <td> &nbsp Icon Here<td align=right>
                <img src=icons/mail-forward.png class=image title="Mail / Contacr us">
                &nbsp; &nbsp;
'''


imgrow = '''
  <tr><td>
     { image beach-hd.jpeg [ thumbwidth ] [ thumbheight ] }
      <td width=10>
      <td> Image description Image description
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

