#!/usr/bin/env python3

# These tags are global to the site

bigtext = '''
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

global_table = [
                ["header", "<font size=+2>Header here</font>"],
                ["var", "<font size=+1>variable { deep } </font>"],
                ["no problem", "no even a <b>little</b> problem? "],
                ["bigtext", bigtext],
                ["deep2", "deep"],
               ]

def global_items(item):

    #print("item", "'" + item + "'")
    for aa in global_table:
        if item[2:-2] == aa[0]:
            return aa[1]

    return "??" + str(item[2:-2]) + "??"

