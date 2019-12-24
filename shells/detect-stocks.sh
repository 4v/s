#!/bin/sh
 function check(){
    count=`ps -ef |grep $1 |grep -v "grep" |wc -l`
    #echo $count
    if [ 0 == $count ];then
        # cd /root/srcs/s/stocks/ && nohup python3 $1 &
        nohup python3 /root/srcs/s/stocks/$1 >/root/logs/nohup.out 2>&1 &
    fi
}

check server.py