#!/usr/bin/env python3

# ------------------------------------------------------------------------
# This is a sample project that is added to the site. The idea here is
# that nothing in this project can syntax error (down) the site, as it is
# imported under a try: except clause, and it is calling only the
# URL registration functions
# ------------------------------------------------------------------------

import os, sys, random, datetime, time

# Add URL; too simple, but is communicates the idea

def got_aa(config, url, query):
    content = "AA file " + url + " " + str(query) + " "
    return content

def got_bb(config, url, query):
    content = "bb file " + url + " " + str(query) + " "
    return content

# ------------------------------------------------------------------------
# Add Mock calendar

def     mock_cal_func(strx):

    try:
        content = '''<table width=100% border=1>
            <tr><td align=center bgcolor=#cccccc colspan=7><b>APP THREE <br>(mock Calendar)</b><br>
        '''
        #        <tr><td>code for app 2 comes here
        dt = datetime.datetime.now()
        anchor = dt.day % 7;
        mon = anchor - dt.weekday()
        #print("dt", dt.weekday(), dt.day, mon, anchor)
        content += "<tr><td colspan=5>"
        cnt = 0; cnt2 = 0;
        wday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        content += "<tr>"
        for cc in range(7):
            content += "<td> <font size=-1>" + wday[cc]
        for aa in range(5):
            content += "<tr>"
            for bb in range(7):
                #aa*7 + bb + 1
                cnt += 1
                if cnt > mon:
                    content += "<td> <font size=-1>" + str(cnt2+1)
                    cnt2 += 1
                    if random.randint(0, 255) % 4 == 0:
                        content += "*"
                    else:
                        content += "&nbsp;"
                else:
                    content += "<td> <font size=-1>" + "&nbsp;"

        content += "</table>"
    except:
        print("Exception on two", sys.exc_info())
    return content

# ------------------------------------------------------------------------
# Add all the functions for the urls; this function is called
# When the url is accessed

sys.path.append("../")

from wsgi_global import add_one_url

add_one_url("/aa", got_aa)
add_one_url("/bb", got_bb)

# ------------------------------------------------------------------------
# Add all the functions and the macro names here
# Simply refer to the macro in the html temple, and it will get called
# and the output substituted

from wsgi_global import add_one_func

add_one_func("app3", mock_cal_func)

# EOF