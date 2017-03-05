#!/bin/bash

SCRIPT_DIR=`dirname $0`
BIN_PYTHON=python
cmd="$BIN_PYTHON bin/main.py"
echo ${cmd}

function usage() {
    echo "Usage: bash $0 command"
    echo "command:"
    echo "    start|stop"
    exit 1
}
PROFILE=""

start(){
    cd ${SCRIPT_DIR}/../
    bin_path=`pwd`/bin
    export PYTHONPATH=${PYTHONPATH}:${bin_path}
    if ps axu | grep "$cmd" | grep -vq grep
    then
        echo ${PROFILE}" already started, exit..."
        return
    fi
    echo ${PROFILE}" start server..."
    mkdir -p logs
    nohup $cmd 0</dev/null 1>logs/main.out 2>&1 &
    echo ${PROFILE}" start done"
    sleep 3
    ps aux | grep python
}

stop(){
    echo ${PROFILE}" kill server..."
    ps axu | grep "$cmd" | grep -v grep | awk '{print $2}' | xargs kill
    sleep 3
    if ps axu | grep "$cmd" | grep -vq grep
    then
        echo ${PROFILE}" stop failed!"
    else
        echo ${PROFILE}" stop success"
    fi
    sleep 1
    ps aux | grep python
}

restart(){
    stop;
    sleep 3;
    start;
}

case "$1" in
start)
    start
    ;;
stop)
    stop
    ;;
restart)
    restart
    ;;
esac
