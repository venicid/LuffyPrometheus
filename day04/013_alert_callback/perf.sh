#!/usr/bin/env bash


#采集
#target_dir=/App/perf/cpu
target_dir=$1
app=$2
#app=m3coordinator
file_name=${app}_cpu_perf_`date "+%Y_%m_%d_%H_%M_%S"`
perf record -F 99 -o  ${target_dir}/${file_name} -p `pgrep -f ${app}` -g -- sleep 120
gzip  ${target_dir}/${file_name}

# perf script -i *cpu_perf.data | stackcollapse-perf.pl | flamegraph.pl > res.svg