#!/bin/sh

(cd ./website; run npm ProdLinux;)&

python3 "./app/BDD/scheduler_update.py" >/dev/null 2>/dev/null =;