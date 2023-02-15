#!/bin/bash
###
 # @Author: ishuangjin
 # WebSite: blog.ishuangjin.cn
 # QQ: 1525053461
 # Mail: ishuangjin@foxmail.com
 # @Date: 2022-12-15 13:53:09
 # @LastEditTime: 2022-12-15 13:53:14
 # @FilePath: \\Github\\MyScript\\nmon\\cmd\\03runnmon.sh
 # Copyright (c) 2022 by ishuangjin, All Rights Reserved.
 # @Description: 
### 
iplist=(192.168.1.11 192.168.1.12 192.168.1.13 192.168.1.14 192.168.1.15 192.168.1.16 192.168.1.17 192.168.1.18 192.168.1.19 192.168.1.20)
for ip in ${iplist[*]}
do
 ssh -p 10022 root@$ip "cd /root/nmon-test-result/;mkdir project050;/root/nmon-test-result/nmon -s1 -c300 -f -m /root/nmon-test-result/project050/;exit;"&
 echo $ip
done