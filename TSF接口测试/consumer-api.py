#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-08 11:06:56
@LastEditTime: 2022-10-10 17:50:12
@FilePath: \\Github\\MyScript\\TSF接口测试\\consumer-api.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 测试tsf服务限流，脚本运行run_time秒，在每个unit_time内运行count次
'''
import time
import requests


class TestUrl:

    def __init__(self, count, unit_time, run_time, all_url, *args):
        '''
        @description: 测试tsf服务限流，脚本运行run_time秒，在每个unit_time内运行count次
        @param  self:  /
        @param  count: 请求次数
        @param  unit_time: 单位时间(s)
        @param  run_time: 程序运行时间(s)
        @param  all_url: 测试url
        @param  tag_params: 标签
        @return None
        '''
        self.count = count
        self.unit_time = unit_time
        self.run_time = run_time
        self.url = all_url
        self.tag_params = args[0]
        self.headers = args[1]

    def ping_url(self):
        re = requests.get(url=self.url, headers=self.headers, params=self.tag_params)
        return print(f'响应时间: {re.elapsed.total_seconds():.2f}s, 响应结果: {re.status_code}, 响应内容: {re.text}')

    def loop_ping(self):
        loop_num = self.run_time // self.unit_time  # 运行多少个循环
        loop_start_time = time.time()
        print(f"每{self.unit_time}秒运行{self.count}次，共运行{loop_num}个循环，开始执行！")
        for loop_n in range(loop_num):
            start_time = time.time()  # 获取开始时间
            start_time_format = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
            print(f"{start_time_format}: 开始运行第{loop_n+1}个{self.unit_time}秒")
            for _ in range(self.count):
                self.ping_url()
            use_time = time.time() - start_time
            sleep_time = self.unit_time - use_time
            print(f"第{loop_n+1}次循环总耗时: {use_time:.2f}s, 程序已运行{time.time()-loop_start_time:.2f}s")
            # print(f"\n......\n")
            if sleep_time > 0:
                print(f"等待: {sleep_time:.2f}s ......")
            else:
                sleep_time = 0
                print(f"第{loop_n+1}次循环，总耗时: {use_time:.2f}s > 单位时间: {self.unit_time}s")
                print("不等待直接开始下一个单位时间")
            print()
            time.sleep(sleep_time)
        return print("done")


def run():
    # 每unit_time秒运行count次
    count = 105
    unit_time = 60
    # 运行run_time秒
    run_time = 6000

    all_url = r"http://192.168.45.29:26435/group-jin/demo2/shenliufei-consumer-demo1/echo-rest/hello"
    # all_url = r"http://192.168.45.29:44980/echo-rest/hello"
    headers = r"x-mg-traceid: 55b00164-4880-11ed-83f0-2811a82fb6cd"

    tag_params = {'tagName': 'user', 'tagValue': 'test'}
    test_url = TestUrl(count, unit_time, run_time, all_url, tag_params, headers)
    test_url.loop_ping()


if __name__ == '__main__':
    run()
