#!/bin/sh

find "$1" -name '*.zip' -exec ./preprocessing/zipfunction.sh "{}" \;