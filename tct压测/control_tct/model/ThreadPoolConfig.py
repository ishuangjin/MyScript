#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-09-21 18:22:23
@LastEditTime: 2023-05-19 14:45:29
@FilePath: \\Github\\MyScript\\tct压测\\control_tct\\model\\ThreadPoolconfig.py
@Copyright (c) 2023 by ${git_name}, All Rights Reserved.
@Description:
'''
from concurrent.futures import ThreadPoolExecutor  # 线程池
import threading
import time
import hashlib
import hmac
import json
import time
from datetime import datetime
import requests
import logging
import random


def get_thread_name(func):

    def wrapper(*args, **kwargs):
        thread_name = threading.current_thread().name
        # 获取锁
        # self.threadLock.acquire()
        print(f"this is thread : {thread_name}")

        # self.do_create_random_task(task_name)
        func(*args, **kwargs)

        # 释放锁
        # self.threadLock.release()
        time.sleep(0.2)

    return wrapper


# class ThreadPoolConfig():

# def __init__(self, loop_range):
#     # 定义锁和线程池,锁不能在线程类内部实例化，这个是调用类不是线程类，所以可以在这里实例化
#     self.threadLock = threading.Lock()
#     # 定义2个线程的线程池
#     self.thread_pool = ThreadPoolExecutor(2)
#     # 定义2个进程的进程池。进程池没用写在这里只想表示进程池的用法和线程池基本一样
#     # self.process_pool = ProcessPoolExecutor(2)
#     self.loop_range = loop_range
#     pass

# def main_logic(self):
#     for i in self.loop_range:
#         # 线程池+线程同步改造添加代码处3/5： 注释掉原先直接调的do_something的形式，改成通过添加的中间函数调用的形式
#         # self.do_something(i)
#         self.call_do_something(i)
#     pass

# # 线程池+线程同步改造添加代码处2/5： 添加一个通过线程池调用do_something的中间方法。参数与do_something一致
# def call_do_something(self, para):
#     self.thread_pool.submit(self.do_something, para)

# def do_something(self, para):
#     thread_name = threading.current_thread().name
#     # 线程池+线程同步改造添加代码处4/5： 获取锁
#     self.threadLock.acquire()
#     print(f"this is thread : {thread_name}")
#     print(f"the parameter value is  : {para}")
#     # 线程池+线程同步改造添加代码处5/5： 释放锁
#     self.threadLock.release()
#     time.sleep(1)
#     pass


class ApiPost():

    def __init__(self):
        # 租户端
        self.secret_id = "b5771VXCcW8bR4O7f8F3Td1ebb7da61K"
        self.secret_key = "35BcZcLGaa9U7f3cYcGQ8cE5H513aae2"

        # 接口基础配置
        self.service = "tsf"
        self.host = "192.168.77.2"
        self.port = 80
        self.endpoint = "http://" + self.host
        self.region = "Service-availability-zone"
        self.version = "2018-03-26"
        self.algorithm = "TC3-HMAC-SHA256"
        self.timestamp = int(time.time())
        self.date = datetime.utcfromtimestamp(self.timestamp).strftime("%Y-%m-%d")

        # logger
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(filename)s[func:%(funcName)s][line:%(lineno)d] - %(levelname)s: %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logger.addHandler(console)

    # 签名方法v3
    def get_sign_heades(self, action, params):
        # ************* 步骤 1：拼接规范请求串 *************
        http_request_method = "POST"
        canonical_uri = "/"
        # canonical_querystring = "action=" + action
        canonical_querystring = ""
        ct = "application/json; charset=utf-8"
        payload = json.dumps(params)
        canonical_headers = "content-type:%s\nhost:%s\n" % (ct, self.host)
        signed_headers = "content-type;host"
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (http_request_method + "\n" + canonical_uri + "\n" + canonical_querystring + "\n" +
                             canonical_headers + "\n" + signed_headers + "\n" + hashed_request_payload)
        # print(canonical_request)

        # ************* 步骤 2：拼接待签名字符串 *************
        credential_scope = self.date + "/" + self.service + "/" + "tc3_request"
        hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = (self.algorithm + "\n" + str(self.timestamp) + "\n" + credential_scope + "\n" +
                          hashed_canonical_request)

        # print(string_to_sign)

        # ************* 步骤 3：计算签名 *************
        # 计算签名摘要函数
        def sign(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        secret_date = sign(("TC3" + self.secret_key).encode("utf-8"), self.date)
        secret_service = sign(secret_date, self.service)
        secret_signing = sign(secret_service, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
        # print(signature)

        # ************* 步骤 4：拼接 Authorization *************
        authorization = (self.algorithm + " " + "Credential=" + self.secret_id + "/" + credential_scope + ", " +
                         "SignedHeaders=" + signed_headers + ", " + "Signature=" + signature)
        # print(authorization)
        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json; charset=utf-8",
            "Host": self.host,
            "X-TC-Action": action,
            "X-TC-Timestamp": str(self.timestamp),
            "X-TC-Version": self.version,
            "X-TC-Region": self.region,
        }
        return headers

    def api_post(self, action, params):
        # 获取签名请求头
        headers = self.get_sign_heades(action=action, params=params)
        url = "http://" + self.host + "/apiDispatch/v3?action=" + action
        r = requests.post(url=url, headers=headers, data=json.dumps(params))

        return r.text


class MultiTask(ApiPost):

    def __init__(self):
        super().__init__()
        # self.threadLock = threading.Lock()
        self.thread_pool = ThreadPoolExecutor(2)
        # {"task_id": "task_name"}
        self.random_task_dict = {}
        self.shard_task_dict = {}

    def create_task(self, task_type, task_start, task_end):
        for num in range(int(task_start), int(task_end) + 1):
            task_name = (task_type + "_" + str(num))
            # self.threadLock.acquire()
            self.thread_pool.submit(self.do_create_task, task_name)
            # self.threadLock.release()

    def do_create_task(self, task_name):
        random_params = {
            "action": "CreateTask",
            "serviceType": "tct",
            "regionId": 1,
            "data": {
                "Version": "2018-03-26",
                "TaskName": task_name,
                "GroupId": "group-6yog6evl",
                "TaskType": "java",
                "TaskContent": "com.tencent.cloud.task.spring.SimpleSpringBeanLogTask",
                "ExecuteType": "unicast",
                "TimeOut": 900000,
                "SuccessOperator": "GTE",
                "SuccessRatio": 80,
                "TaskRule": {
                    "RuleType": "Cron",
                    "Expression": "0 0/5 * * * ?"
                },
                "ShardArguments": [],
                "TaskArgument": "",
                "RetryCount": 0,
                "RetryInterval": 0,
                "AdvanceSettings": {
                    "SubTaskConcurrency": 2
                }
            }
        }
        shard_params = {
            "action": "CreateTask",
            "serviceType": "tct",
            "regionId": 1,
            "data": {
                "Version": "2018-03-26",
                "TaskName": task_name,
                "GroupId": "group-6yog6evl",
                "TaskType": "java",
                "TaskContent": "com.tencent.cloud.task.SimpleShardExecutableTask" + str(random.randint(1, 30)),
                "ExecuteType": "shard",
                "TimeOut": 300000,
                "SuccessOperator": "GTE",
                "SuccessRatio": 100,
                "TaskRule": {
                    "RuleType": "Cron",
                    "Expression": "0 0/5 * * * ?"
                },
                # "ShardArguments": [{
                #     "ShardKey": 1,
                #     "ShardValue": "a"
                # }, {
                #     "ShardKey": 2,
                #     "ShardValue": "b"
                # }, {
                #     "ShardKey": 3,
                #     "ShardValue": "c"
                # }],
                "ShardArguments": [],
                "TaskArgument": "",
                "ProgramIdList": [],
                "RetryCount": 0,
                "RetryInterval": 0,
                "ShardCount": random.randint(10, 30),
                # "ShardCount": 20,
                "AdvanceSettings": {
                    "SubTaskConcurrency": 100
                }
            }
        }
        params_dict = {"random": random_params, "shard": shard_params}
        # resp = self.api_post(action="DescribeReleasedConfig", params=params_dict[task_type])
        task_type = task_name.lsplit("_")
        resp = params_dict[task_type]
        task_id = resp["Response"]["Result"]
        msg = task_id + ":" + task_name
        print(msg)
        print(resp)
        print("1")
        self.random_task_dict[task_id] = task_name
        return msg

    def create_random_task(self, task_type, task_start, task_end):
        for num in range(int(task_start), int(task_end) + 1):
            task_name = (task_type + str(num))
            self.thread_pool.submit(self.do_create_random_task, task_name)

    def do_create_random_task(self, task_name):
        params = {
            "action": "CreateTask",
            "serviceType": "tct",
            "regionId": 1,
            "data": {
                "Version": "2018-03-26",
                "TaskName": task_name,
                "GroupId": "group-6yog6evl",
                "TaskType": "java",
                "TaskContent": "com.tencent.cloud.task.spring.SimpleSpringBeanLogTask",
                "ExecuteType": "unicast",
                "TimeOut": 900000,
                "SuccessOperator": "GTE",
                "SuccessRatio": 80,
                "TaskRule": {
                    "RuleType": "Cron",
                    "Expression": "0 0/5 * * * ?"
                },
                "ShardArguments": [],
                "TaskArgument": "",
                "RetryCount": 0,
                "RetryInterval": 0,
                "AdvanceSettings": {
                    "SubTaskConcurrency": 2
                }
            }
        }
        resp = self.api_post(action="DescribeReleasedConfig", params=params)
        task_id = resp["Response"]["Result"]
        print(task_id, ":", task_name)
        self.random_task_dict[task_id] = task_name

    def create_shard_task(self, task_type, task_start, task_end):
        for num in range(int(task_start), int(task_end) + 1):
            task_name = (task_type + str(num))
            self.thread_pool.submit(self.do_create_shard_task, task_name)

    def do_create_shard_task(self, task_name):
        params = {
            "action": "CreateTask",
            "serviceType": "tct",
            "regionId": 1,
            "data": {
                "Version": "2018-03-26",
                "TaskName": task_name,
                "GroupId": "group-6yog6evl",
                "TaskType": "java",
                "TaskContent": "com.tencent.cloud.task.SimpleShardExecutableTask" + str(random.randint(1, 30)),
                "ExecuteType": "shard",
                "TimeOut": 300000,
                "SuccessOperator": "GTE",
                "SuccessRatio": 100,
                "TaskRule": {
                    "RuleType": "Cron",
                    "Expression": "0 0/5 * * * ?"
                },
                # "ShardArguments": [{
                #     "ShardKey": 1,
                #     "ShardValue": "a"
                # }, {
                #     "ShardKey": 2,
                #     "ShardValue": "b"
                # }, {
                #     "ShardKey": 3,
                #     "ShardValue": "c"
                # }],
                "ShardArguments": [],
                "TaskArgument": "",
                "ProgramIdList": [],
                "RetryCount": 0,
                "RetryInterval": 0,
                "ShardCount": random.randint(10, 30),
                # "ShardCount": 20,
                "AdvanceSettings": {
                    "SubTaskConcurrency": 100
                }
            }
        }
        resp = self.api_post(action="DescribeReleasedConfig", params=params)
        task_id = resp["Response"]["Result"]
        print(task_id, ":", task_name)
        self.shard_task_dict[task_id] = task_name

    def func_None(self):
        print("cannot find func")

    def create_sometasktype(self, task_name, task_start, task_end):
        print("do", task_name, task_start, task_end)

    def start_task(self):
        for task_id, task_name in self.shard_task_dict:
            pass
        pass

    def do_start_task(self):
        task_id, task_name = task_id_tuple
        print(task_id)
        params = {"action": func, "serviceType": "tct", "regionId": 1, "data": {"Version": "2018-03-26", "TaskId": task_id}}
        resp = api_post(action="DescribeReleasedConfig", params=params)
        print("正在{}任务：{}".format(func, task_name))
        print(resp)
        print(threading.current_thread().name)
        pass

    def create(self, task_type, task_start, task_end):
        func_name = "create_" + task_type
        return getattr(MultiTask(), func_name)(task_type, task_start, task_end)


if __name__ == "__main__":
    obj = MultiTask()
    obj.create_task("shard", 6, 20)
    obj.create_random_task("shard", 6, 20)
    # obj.start("sometasktype", 777730, 777740)
# stop
# delete
