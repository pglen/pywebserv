#!/bin/bash

#if [ ! -e ANYFILE ] ; then

make clean

#if [ ! -e /mnt/remote-home/upload ] ; then
#    echo "Please mount remote. (mount_remote_home.sh)"
#    exit
#fi

#rsync -r -uv --times --exclude .git/ * /mnt/remote-home/upload
rsync -r -uv --times --exclude .git/ --exclude html/ --exclude latex/ \
 --exclude content/data --exclude content/tmp --exclude __pycache__ --exclude media \
	 --rsh "ssh -p2222"  * peterglen@209.124.64.123:/home/peterglen/upload

