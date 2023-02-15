#!/bin/bash
###
 # @Author: ishuangjin
 # WebSite: blog.ishuangjin.cn
 # QQ: 1525053461
 # Mail: ishuangjin@foxmail.com
 # @Date: 2022-12-15 13:51:53
 # @LastEditTime: 2022-12-15 13:52:23
 # @FilePath: \\Github\\MyScript\\nmon\\cmd\\01copynmon.sh
 # Copyright (c) 2022 by ishuangjin, All Rights Reserved.
 # @Description: 
### 
iplist=(192.168.1.11 192.168.1.12 192.168.1.13 192.168.1.14 192.168.1.15 192.168.1.16 192.168.1.17 192.168.1.18 192.168.1.19 192.168.1.20)
for ip in ${iplist[*]}
do
 scp -P 10022 /root/nmon root@$ip:/root/ &
 echo $ip
done