#!/usr/bin/env python3

'''
 This is a sample project that is added to the site. The idea here is
 that nothing in this project can down the site, as it is
 imported under a try: except clause, and it is calling only the
 URL registration functions

'''

ppp = __file__.split('/')
plen = len(ppp)
modname = ppp[plen-2] + "-" + ppp[plen-1]

#print("Loaded mod:", modname)

import os, sys, random, datetime, time

sys.path.append("../")

from . import common

import wsgi_global, wsgi_util, wsgi_func, wsgi_parse

# Add URL; too simple, but is communicates the idea

def got_aa(config, url, query, req, templ):
    content = "AA file " + url + " " + str(query) + " "
    return content

def got_bb(config, url, query, req, templ):
    content = "bb file " + url + " " + str(query) + " "
    return content

# ------------------------------------------------------------------------
# Add Mock calendar

def     mock_cal_func(strx, context):

    '''
    Mock calendar. Does nothing but presents a calendar looking user interface
    '''

    from calendar import monthrange

    try:
        content = '''<table width=100% border=1>
            <tr><td colspan=7>
                <table width=100% border=0 bgcolor=#cccccc>
                    <tr>
                    <td align=center colspan=1>
                         <a href=?forw=1><<</a>
                    <td align=center colspan=5>
                        <b>APP THREE
                    <td align=center colspan=1>
                         <a href=?back=1>>></a>

                 <tr bgcolor=#cccccc>
                 <td align=center colspan=7>
                    (mock Calendar)
                 </table>
        '''

        dt2 = datetime.datetime.now()
        dt = datetime.datetime(dt2.year, dt2.month, 1)
        #print("dt", dt, "wd:", dt.weekday())
        mon = dt.weekday()
        rrr = monthrange(dt2.year, dt2.month)[1]
        #print("mock_cal_func() wd:", dt.weekday(), "rrr", rrr)

        content += "<tr><td colspan=7>"
        cnt = 0; cnt2 = 0;
        wday = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        content += "<tr>"
        for cc in range(7):
            content += "<td> <font size=-1>" + wday[cc]
        for aa in range(5):
            content += "<tr>"
            colx = "#ffffff"
            for bb in range(7):
                if dt.year == dt2.year and dt.month == dt.month and dt2.day == cnt:
                    #print("today", dt2.day)
                    colx = "#dddddd"
                #aa*7 + bb + 1
                cnt += 1
                if cnt > rrr:
                    content += "<td> <font size=-1>"
                else:
                    if cnt > mon:
                        content += "<td bgcolor=" + colx + "> <font size=-1>" + "<a href=?cal-" + \
                             str(dt.year) + "-" +  str(dt.month) + "-" + str(cnt) + \
                            ">" + str(cnt2+1) + "</a>"

                        if random.randint(0, 255) % 4 == 0:
                            content += "*"
                        else:
                            content += "&nbsp;"
                    else:
                        content += "<td bgcolor=" + colx +  "> <font size=-1>" + "&nbsp;"
                cnt2 += 1

        content += "</table>Active marked by asterisk (*)"
    except:
        print("Exception on two", sys.exc_info())
    return content

def     got_index(config, carry):

    if config.verbose:
        print("got_index() url = '%s'" % carry.url)

    if config.pgdebug > 1:
        print("got_index()", "url:", carry.url, "query:", carry.query)

    carry.local_table = common.local_table
    content = wsgi_util.process_default(config, carry)
    return content

# ------------------------------------------------------------------------
# Add all the functions for the urls; this function is called
# When the url is accessed

wsgi_global.urlmap.add_one_url("/resp/",  got_index, "index.html", __file__)
#wsgi_global.urlmap.add_one_url("/resp/",  got_index, "resp.html", __file__)
wsgi_global.urlmap.add_one_url("/resp/index.html", got_index, "index.html", __file__)
wsgi_global.urlmap.add_one_url("/resp/resp.html", got_index, "resp.html", __file__)

# ------------------------------------------------------------------------
# Add all the functions and the macro names here
# Simply refer to the macro in the html temple, and it will get called
# and the output substituted

wsgi_global.gl_table.add_one_func("app3", mock_cal_func)

# EOF