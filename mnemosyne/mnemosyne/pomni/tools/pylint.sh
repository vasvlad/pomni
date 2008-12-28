#!/bin/sh

ls *.py | grep -v __init__| while read f; do echo $f $(pylint $f 2>/dev/null | grep rated) ; done


