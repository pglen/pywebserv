#!/usr/bin/env python3

''' The simplest web server, utilities module. This is where we parse the
    incoming (loaded) files for macros. The substitution occures in steps
    recursively.
'''

import sys, os, time, re, traceback
import wsgi_global, wsgi_util, wsgi_str

_MAX_RECURSE = 10           # This many recursions
_MAX_REPARSE = 2            # This many passes

_regex = "{ .*? }"
_regex2 = "\[ .*? \]"

# ------------------------------------------------------------------------

def _parse_items(item, context, table):

    cccc = ""

    #print("parse item", "'" + item + "\n'")
    item2 = item.split(" ")
    in_arg = item2[0] == "[" or item2[0] == "]"
    #print("item2", item2, in_arg)

    # Scan backwards so items can be overridden
    for ii in range(len(table)-1, -1, -1):
        aa = table[ii]
        #print("aa", aa)
        #if item2[1][2:-2] == aa[0]:
        if item2[1] == aa[0]:
            # String expansion
            if type(aa[1]) == str:
                if context.configx.parse_verbose:
                    print("str: ",  context.url, wsgi_str.strpad(item),
                             wsgi_str.strupt(aa[1],40))

                # This polluted inside the tag
                if context.configx.parse_inline and not in_arg :
                    #print("\n<!-- print var from: " + aa[0] + " -->" + aa[1])
                    pass
                return aa[1]

            # Function?
            if type(aa[1]) == type(_parse_items):
                # print(context.getvals())
                if context.configx.parse_verbose:
                    print("func:", context.url, wsgi_str.strpad(item),
                            aa[1].__name__)
                try:
                    cccc = aa[1](item, context)
                except:
                    wsgi_util.put_exception("Cannot exec: " + str(item))
                    #print("item", item, "aa[1]", aa[1])
                    pass
                #print("cccc", cccc[:12])

                if context.configx.parse_inline and not in_arg :
                    return "<!-- expanded func from: " + aa[0] + " -->\n" + cccc

                return cccc
    return item

# Parse buffer; build it hopping on regexes

def parse_buffer(buff, regex, context, table):

    count = 0; prog = 0
    rrr = re.compile(regex)
    arr = []
    while(True):
        frag = re.search(rrr, buff[prog:])
        if not frag:
            arr.append(buff[prog:])
            break
        #print ("match", frag)
        bbb = prog+frag.start()
        eee = prog+frag.end()
        arr.append(buff[prog:bbb])
        #print("match", buff[bbb:eee])
        conv = _parse_items(buff[bbb:eee], context, table)
        #print("conv", wsgi_str.strupt(conv))
        arr.append(conv)
        prog += frag.end()
        count += 1

    #print("parsed", count)
    #print ("arr", arr)
    return arr, count

# ------------------------------------------------------------------------

def _parse_one(buff, context, tablex, regex):

    # Recursively process
    content = buff
    cnt2 = 0; old_cnt = 0

    while(True):
        arr, cnt = parse_buffer(content, regex, context, tablex)
        content = ""
        for aa in arr:
            content += str(aa)
        #print("recursive", cnt)
        if cnt <= 1:
            break
        # Maximun recurse exceeded
        if cnt2 >= _MAX_RECURSE:
            print("Maximum recursion exceeded.")
            break
        cnt2 += 1

        # No change, exit; most likely undefined macros
        if old_cnt == cnt:
            break

        old_cnt = cnt

    return content

# ------------------------------------------------------------------------
# Parse buffer

def recursive_parse(buff, context, local_table):

    #print("contextx", context)
    #print(context.getvals())
    #print("recursive_parse() buff:", wsgi_str.strunesc(buff[:12]))

    # if local_table:
    #   if context.configx.pgdebug > 3:
    #       wsgi_util.dump_table("Local Table:", local_table)
    cnt = 0
    sss =   time.perf_counter()

    while 1:
        # Pre set the stage vars
        parsed2 = ""; parsed3 = "";

        # Do local table first, so it overrides global
        if local_table:
            try:
                parsed2 = _parse_one(buff, context,  local_table, _regex)
                #print("parsed2", parsed2)
            except:
                print(" **** -----------First parser exception ------------------ ****")
                wsgi_util.put_exception("exception in local parser", )
                parsed2 = buff
        else:
            parsed2 = buff

        #print("Local %.4f" % ( (time.perf_counter() - sss) * 1000), "ms")

        # Recursively process
        try:
            parsed3 = _parse_one(parsed2, context,  wsgi_global.gl_table.mytable, _regex)
        except:
            #wsgi_util.put_exception("exception in global parser", )
            parsed3 = parsed2

        #print("global %.4f" % ( (time.perf_counter() - sss) * 1000), "ms")

        ## Do local table again as global expansion may uncover new items
        # Please do not have complex interdependent macros, as it defeats
        # the purpose of this subsystem
        # Remeber max 10 levels in and 4 levels across tables

        # Mon 20.Feb.2023 deleted in favour of repeat logic
        #if local_table:
        #    try:
        #        parsed4 = _parse_one(parsed3, context,  local_table, _regex)
        #        #print("parsed4", parsed4)
        #    except:
        #        #wsgi_util.put_exception("exception in local parser second run", )
        #        parsed4 = parsed3
        #else:
        #    parsed4 = parsed3
        #print("re-local %.4f" % ( (time.perf_counter() - sss) * 1000), "ms")
        #buff = parsed4

        # Are we done yet?
        if cnt > _MAX_REPARSE:
            break

        cnt += 1
        # Loop back
        buff = parsed3

        #break

    #print("Full %.4f" % ( (time.perf_counter() - sss) * 1000), "ms")

    #return parsed4
    return parsed3

# EOF