#!/bin/bash
find . -type d -depth -name "__pycache__" -exec rm -rf {} \;  2>/dev/null
find . -type d -depth -name "*.pyc" -exec rm -f {} \;  2>/dev/null
# Remove log
rm -f content/data/*.log
# Remove generated docs
rm -rf html
rm -rf latex

