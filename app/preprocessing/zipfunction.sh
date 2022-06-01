#!/bin/sh

for f in "$@" ;
do
    unzip -o -d `dirname $f` $f
    if [ "$?" -eq "0" ]
    then
        rm $f;
    else
        rar x -o+ $f `dirname $f`
        if [ "$?" -eq "0" ]
        then
            rm $f;
        fi
    fi
done
