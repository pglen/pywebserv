#!/bin/bash
find . -name "*.py" -exec grep -H $1 {} \;
