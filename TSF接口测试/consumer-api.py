#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-08 11:06:56
@LastEditTime: 2022-08-15 17:51:36
@FilePath: \\Github\\MyScript\\TSF接口测试\\consumer-api.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''
import time
import requests


class TestUrl:

    def __init__(self, host, port, run_speed_times_limit, run_speed_unit_time, run_time):
        """
        run_time：运行时间, 秒，需要跑多久脚本
        run_speed_times_limit: 限流请求数
        run_speed_unit_time: 单位时间
        """
        self.host = host
        self.port = port
        self.run_speed_times_limit = run_speed_times_limit
        self.run_speed_unit_time = run_speed_unit_time
        self.run_time = run_time

    def ping_url(self):
        tag_params = {'tagName': 'user', 'tagValue': 'test'}
        # url='http://{}:{}/echo-rest/hello'.format(self.host, self.port)
        url = 'http://{}:{}/jin-test1/global-ns/shenliufei-consumer-demo1/echo-rest/hello'.format(self.host, self.port)
        re = requests.get(url=url, params=tag_params)
        print(re.text)

    def loop_ping(self):
        count = 0  # 运行次数，ping多少次
        sleep_time = self.run_speed_unit_time / self.run_speed_times_limit  # 休眠时间，两次请求间的空余时间
        start_time = time.time()  # 获取开始时间
        end_time = start_time + self.run_time  # 控制脚本在什么时候结束
        while time.time() < end_time:
            count += 1
            self.ping_url()
            stop_time = time.time()  # 单次运行用时
            print('已ping {} 次, 共使用 {} 秒'.format(count, stop_time - start_time))
            time.sleep(sleep_time)


if __name__ == '__main__':
    host = '192.168.22.4'
    port = '42247'
    run_speed_times_limit = 10  # 请求数
    run_speed_unit_time = 3  # 单位时间
    run_time = 300  # run_time：运行时间, 秒，需要跑多久脚本
    test_url = TestUrl(host, port, run_speed_times_limit, run_speed_unit_time, run_time)
    # test_url.ping_url()
    test_url.loop_ping()
