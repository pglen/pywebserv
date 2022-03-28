 #!/usr/bin/env python3

import os, sys, time

import wsgi_util, wsgi_func, wsgi_data, wsgi_global


''' Local macros and data. Register it after fribe or use "_mac_ prefix to auto register
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

_mac_article5 = '''
Hello
'''

_mac_art_header = '''
Header here
'''

#wsgi_util.append_file("Importing macros\n")

vvv = locals().copy()
for aa in vvv:
    if "_mac_" in aa[:5]:
        #wsgi_util.append_file("register: " + aa[5:] + "\n")
        wsgi_global.add_one_func(aa[5:],  vvv[aa])




