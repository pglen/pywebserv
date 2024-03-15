#!/bin/bash

# Wait fot stuff to arrive

while [ 1 ]; do
    echo Started monitor
    inotifywait test_dir  > /dev/null 2>&1
    echo New files arrived
    sleep 1
done

