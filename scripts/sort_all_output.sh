#!/bin/bash

do_normalization="$2"

function sort_directory {
    for i in $(ls $1/*.txt); do
        python $(dirname $0)/../python/util/sort_by_value.py $i "$i"_s "$do_normalization" &
    done
}

echo "sorting in folder " $1 "..."
sort_directory $1
echo "done"
