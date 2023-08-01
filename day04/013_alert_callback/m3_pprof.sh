#!/usr/bin/env bash



input_host_file=$1
output_dir=$2
for i in `cat $1`;do
    #curl $i:7201/debug/dump >${i}_`date "+%Y_%m_%d_%H_%M_%S"`.zip &
    curl -s $i:7201/debug/dump >${output_dir}/${i}_`date "+%Y_%m_%d_%H_%M_%S"`.zip &
done