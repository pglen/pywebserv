#!/bin/bash

# This will refresh ALL currenty displayed pages in all
# firefox instances. Useful for multi access testing.
# Edit if you are using a different browser

# List all Firefox instances
FF=`xdotool search --name "Mozilla Firefox"`
#echo $FF
for AA in $FF; do
    #echo $AA
    # Activate; Send refresh key
    xdotool windowactivate $AA
    #xdotool key --window $AA  --delay 10 ctrl+r
    xdotool key --window $AA  --delay 10 F5
done

# EOF