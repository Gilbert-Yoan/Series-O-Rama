#!/bin/sh

find "$1" -name '*.zip' -exec ./zipfunction.sh {} \;