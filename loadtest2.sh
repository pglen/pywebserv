#!/bin/bash

echo "test" $$
time wget -o test.html localhost:8000/
echo end $$

