#!/bin/bash

# This will refresh the currenty displayed page in firefox
# Edit if you are using a different browser
xdotool search --name "Mozilla Firefox" windowactivate --sync key ctrl+r

# Bring focus back to your editor
# Edit string to match the header of the editor you are using
WW=`xdotool search --name "pyedpro:" | head -1`
#echo $WW
xdotool windowactivate --sync $WW

