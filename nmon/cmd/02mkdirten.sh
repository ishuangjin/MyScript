#!/bin/bash
iplist=(192.168.1.11 192.168.1.12 192.168.1.13 192.168.1.14 192.168.1.15 192.168.1.16 192.168.1.17 192.168.1.18 192.168.1.19 192.168.1.20)
for ip in ${iplist[*]}
do
 ssh -p 10022 root@$ip "cd;mkdir nmon-test-result;mv nmon nmon-test-result/;exit;"&
 echo $ip
done