#!/usr/bin/env bash

script=feature_extract.py
input_dir="$1"
output_dir="$2"

for f in "$input_dir"/*
do
    file_name=$(basename $f .entity)
    cat $f | python3 $script > $output_dir/"$file_name".fts
done
