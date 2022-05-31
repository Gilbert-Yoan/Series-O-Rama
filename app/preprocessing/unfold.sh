#!/bin/sh

for f in `ls "$1" `
do
	path="$1/$f/"
	find "$path" -mindepth 2 -type f -exec mv -t $path {} \;
done

for f in `ls "$1" `
do
	path="$1/$f/"
	find "$path" -type d -empty -delete
done