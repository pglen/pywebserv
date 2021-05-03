#!/bin/bash

# This will refresh the currenty displayed page in firefox
# Edit if you are using a different browser

# The tail will assure that the last active browser will be targeted
FF=`xdotool search --name "Mozilla Firefox" | tail -1`
#echo $FF
xdotool windowactivate --sync $FF
xdotool key ctrl+r

# Bring focus back to your editor
# Edit string to match the header of the editor you are using
WW=`xdotool search --name "pyedpro:" | head -1`
#echo $WW
xdotool windowactivate --sync $WW

# eof