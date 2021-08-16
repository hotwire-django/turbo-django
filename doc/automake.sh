#!/usr/bin/env bash

# This script detects changes in doc files and automatically triggers a rebuild.

FOO=$(mktemp /tmp/turbodocs-automake.XXXXXX)
while true; do
    for SRC in $(find . -name '*.rst' -mmin -1); do
        if [ "$SRC" -nt "$FOO" ]; then
            touch $FOO
            make clean html
            date
            break
        fi
    done
    sleep 1
done

