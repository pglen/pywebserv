#!/bin/bash

mkdir -p test
cd test
rm *
for aa in  {1..100}
do
    time wget localhost:8000/editor/ &
    #sleep 0.1
done

echo "Last"

