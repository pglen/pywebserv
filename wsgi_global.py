#!/usr/bin/env python3

# These tags are global to the site

import wsgi_res

def     deep_func(strx):
    return "Deep from code"

def     crap_func(strx):
    return "<b>crap</b> from code"

def     image_func(strx):
    sss = strx.split()
    print("Image func:", sss)

    if len(sss) == 4:
        return "<img src=" + sss[2] + ">"

    if len(sss) == 5:
        return "<img src=" + sss[2] + " height=" + sss[3] + " >"

    if len(sss) == 6:
        return "<img src=" + sss[2] + " height=" + sss[3] + " width= " + sss[4] + " >"

    return "Put image heree"


global_table = \
  [
    ["header2", " <font size=+2>Sub Header here</font>"],
    ["header", wsgi_res.header],
    ["footer", wsgi_res.footer],
    ["var", "<font size=+1>variable { deep } </font>"],
    ["no problem", "no even a <b>little</b> problem? "],
    ["bigtext", wsgi_res.bigtext],
    ["deep", deep_func],
    ["crap", crap_func],
    ["image", image_func],
    ["mystyle", wsgi_res.mystyle],
    ["spacer", "<table><tr><td></table>"],
    ["mycolor", "bgcolor=#aaffbb"],
    ["thumbwidth", "150"],
    ["imgrow", wsgi_res.imgrow],
  ]


def global_items(item):

    #print("item", "'" + item + "'")
    for aa in global_table:
        if item[2:-2] == aa[0]:
            if type(aa[1]) == str:
                return aa[1]
            if type(aa[1]) == type(global_items):
                return aa[1](item)

    # "??" #return str(item[2:-2]) + "??"
    return item

# Parameterized last

def global_para_items(item):

    #print("item", "'" + item + "'")

    # rescan for parameterized
    for aa in global_table:
        if item[2:-2].split()[0] == aa[0]:
            if type(aa[1]) == type(global_items):
                return aa[1](item)

    return "!!" + str(item[2:-2]) + "!!"
