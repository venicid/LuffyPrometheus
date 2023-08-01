#!/usr/bin/env bash
LISTEN_PORT="5004"
pidfile=app.pid
py_file_name=perf_api
acc_log_file="perf_api.log"

function start() {

    gunicorn -w 5 -b 0.0.0.0:${LISTEN_PORT} ${py_file_name}:app -D --pid $pidfile --access-logfile  $acc_log_file --log-level debug
    sleep 1
    echo -n "${py_file_name} started..., pid="
    cat $pidfile
}




function stop() {
    ps -ef |grep gunicorn |grep ${LISTEN_PORT} |grep -v grep |awk '{print $2}' |xargs kill
    echo "${py_file_name} quit..."
}



function restart() {
    stop
    sleep 2
    start
}



function help() {
    echo "$0 start|stop|restart|status|tail|kill9|version|pack"
}

if [ "$1" == "" ]; then
    help
elif [ "$1" == "stop" ];then
    stop
elif [ "$1" == "kill9" ];then
    kill9
elif [ "$1" == "start" ];then
    start
elif [ "$1" == "restart" ];then
    restart
elif [ "$1" == "status" ];then
    status
elif [ "$1" == "tail" ];then
    tailf
elif [ "$1" == "pack" ];then
    pack
elif [ "$1" == "version" ];then
    show_version
else
    help
fi
