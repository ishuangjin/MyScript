#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-08 11:06:56
@LastEditTime: 2022-08-16 10:49:25
@FilePath: \\Github\\MyScript\\TSF接口测试\\consumer-api.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 测试tsf服务限流，脚本运行run_time秒，在每个unit_time内运行count次
'''
import time
import requests


class TestUrl:

    def __init__(self, host, port, url_merge, count, unit_time, run_time):
        '''
        @description: 测试tsf服务限流，脚本运行run_time秒，在每个unit_time内运行count次
        @param  self: /
        @param  host: 被测主机
        @param  port: 端口
        @param  url_merge: url路径
        @param  count: 请求次数
        @param  unit_time: 单位时间
        @param  run_time: 程序运行时间
        @return /
        '''
        self.host = host
        self.port = port
        self.count = count
        self.unit_time = unit_time
        self.run_time = run_time
        self.url_merge = url_merge

    def ping_url(self):
        tag_params = {'tagName': 'user', 'tagValue': 'test'}
        url = 'http://{}:{}'.format(self.host, self.port) + self.url_merge
        re = requests.get(url=url, params=tag_params)
        return print(re.text)

    def loop_ping(self):
        loop_num = self.run_time // self.unit_time  # 运行多少个循环
        print(f"每{self.unit_time}秒运行{self.count}次，开始执行")
        for loop_n in range(loop_num):
            start_time = time.time()  # 获取开始时间
            start_time_format = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(f"{start_time_format}: 开始运行第{loop_n+1}个{self.unit_time}秒")
            for _ in range(self.count):
                self.ping_url()
            use_time = time.time() - start_time
            sleep_time = self.unit_time - use_time
            print(f"used {use_time:.2f}s")
            print(f"watting {sleep_time:.2f}s ......\n")
            time.sleep(sleep_time)
        return print("done")


if __name__ == '__main__':
    host = '192.168.22.4'  # consumer 服务主机
    port = '42247'  # consumer 端口
    count = 10  # 请求数
    unit_time = 3  # 单位时间，秒
    run_time = 300  # run_time：脚本运行时间, 秒，需要跑多久脚本
    url_merge = r'/jin-test1/global-ns/shenliufei-consumer-demo1/echo-rest/hello'  # 要访问的路径
    test_url = TestUrl(host, port, url_merge, count, unit_time, run_time)
    # test_url.ping_url()
    test_url.loop_ping()
