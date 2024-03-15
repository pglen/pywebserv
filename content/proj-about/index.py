#!/usr/bin/env python3

'''
    This is a sample project that is added to the site. The idea here is
    that nothing in this project can down the site, can down only the page.
    (like a syntax error)
    It is imported under a try: except clause, and it is calling only the
    URL registration functions.
    Also, included a default web page function as index.html or as '/'

    The statement above turns out to be false, if this file contains
    items the site is dependent upon. Naturally, this goes without saying.
'''

import os, sys, time

import wsgi_util, wsgi_func, wsgi_data
import wsgi_global, wsgi_parse, wsgi_swear, wsgi_conf

ppp = __file__.split('/')
modname = ppp[-2]
#print("Loaded mod:", modname)

#from . import macros
#from . import common

local_table = []

def got_index(config, carry):

    if config.verbose > 1:
        print("got_index() url = '%s'" % carry.url)

    if config.pgdebug > 1:
        print("got_index()", "url:", carry.url, "query:", carry.query)

    if config.pgdebug > 2:
        print("wsgi_conf", config.getvals())

    if config.pgdebug > 3:
        print("got_index() url=%s"% carry.url, "query=%s" % carry.query,
                    "request=%s" % carry.request,
"template=%s" % carry.template, "fname=%s" % carry.fname)

    #print("carry.request", carry.request)
    #print("carry.query", carry.query)
    carry.local_table = local_table
    content = wsgi_util.process_default(config, carry)
    return content

def _func_center_about(strx, context):
    contents = '''<center><h1>About</h1></center>
    &nbsp; The United Planet Peace (UPP) foundation will create a framework for
    democracy in a global context. All over the world, the proposed framework
    is incentivizing governments to create democratically sound and sustainable
    processes.<p>

    &nbsp; Processes for fair elections, for judicial fairness and social equilibrium.
    This is achieved both at the grassroots level and political level. Finally
    an international body that does not control the low level activities of the
    world, but the high level democratic and not so democratic institutions.
    <p>
    &nbsp; Many countries have gone through their democratic 'Founding' era. An era in
    which (among other things) a system of justice is established. In many
    places, this is called the Founding Father's era. Where an equitable
    distribution of power and resources is created. A system that
    assures fair and  equal representation for all.
    However, some countries have not gone through this 'Founding' era.
    The UPP is set out to bring this Founding Father's era to the whole planet.
    <p>
    &nbsp; There are plenty of organizations to help in cooperating internationally;
    mostly aiding / controlling inter-governmental affairs. And there are
    plenty of enforcement instruments. However, the most important instrument
    is missing: Containment of the Country's Leadership. In the twenty-first
    century, there should be standards of leadership, standards of governance
    and especially, standards for justice. Term limits for every position. High
    standards for democracy, accountability and equality. UPP is set out to
    create a framework where these shortcomings are addressed. Globally. The
    whole planet.
    <p>
    &nbsp; United Planet Peace is set up on an important mission. It's success would
    make a significant impact, saving lives, and improving it for many. Please
    help by donating on our donation page.
    <p>

    <table width=100% border=0>

    <tr><td><td> &nbsp; &nbsp; &nbsp; <b>Contacts:</b>
    <tr><td height=8>
    <tr><td><td> Peter Glen: <td> +71 302 354 6551 <td> PeterGlen@unitedplanetpeace.com
    <tr><td><td> Administrator: <td> <td> admin@unitedplanetpeace.com
    <tr><td><td> Founder:    <td><td> PetergGlen99@gmail.com
    </table>
    '''
    return contents

# ------------------------------------------------------------------------
# Add all the functions for the urls;
# This function is called when the module is loaded
#

'''
Initialize the current module
'''

try:
    # Add default enties to tables
    wsgi_global.urlmap.add_one_url("/about/", got_index, "index.html", __file__)
    wsgi_global.urlmap.add_one_url("/about/index.html", got_index, "index.html", __file__)
    wsgi_util.add_all_vars(locals().copy(), local_table)
except:
    print("Cannot add module globals:", "'" + modname + "'", sys.exc_info())

