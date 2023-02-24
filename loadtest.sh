#!/bin/bash

mkdir -p test
cd test
rm *
for aa in  {1..100}
do
    ../loadtest2.sh &
done

echo "Last"

