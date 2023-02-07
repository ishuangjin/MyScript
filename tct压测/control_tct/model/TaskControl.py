#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-12-15 17:29:12
@LastEditTime: 2023-01-03 15:22:00
@FilePath: \\Github\\MyScript\\tct压测\\control_tct\\model\\TaskControl.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description:
'''
from concurrent.futures import ThreadPoolExecutor
from model.ApiPost import api_post
from random import randint
from model.GetSql import get_task_id_name
import threading


def create_random_task(task_start=1, task_end=1, task_name_start="random_task"):
    """
    创建执行方式为随机的任务
    :param task_name_start:任务名字前缀
    :param task_start:任务名字起始
    :param task_end:任务名字结束
    :return: None
    eg:create_random_task(1, 3),创建任务random_task1、random_task2、random_task3
    """
    for num in range(int(task_start), int(task_end) + 1):
        task_name = task_name_start + str(num)
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
        resp = api_post(action="DescribeReleasedConfig", params=params)
        print("正在创建随机任务：", task_name)
        print(resp)


def create_shard_task(task_start=1, task_end=1, task_name_start="shard_task"):
    """
    创建分片任务
    :param task_name_start:任务名字前缀
    :param task_start:任务名字起始
    :param task_end:任务名字结束
    :return:None
    """
    for num in range(int(task_start), int(task_end) + 1):
        task_name = task_name_start + str(num)
        params = {
            "action": "CreateTask",
            "serviceType": "tct",
            "regionId": 1,
            "data": {
                "Version": "2018-03-26",
                "TaskName": task_name,
                "GroupId": "group-6yog6evl",
                "TaskType": "java",
                "TaskContent": "com.tencent.cloud.task.SimpleShardExecutableTask",
                "ExecuteType": "shard",
                "TimeOut": 900000,
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
                "ShardCount": randint(10, 30),
                "AdvanceSettings": {
                    "SubTaskConcurrency": 10
                }
            }
        }

        resp = api_post(action="DescribeReleasedConfig", params=params)
        print("正在创建分片任务：", task_name)
        print(resp)


def alter_task(func, task_start=0, task_count=0):
    """
    修改任务状态，task_count=0，修改全部任务
    :param func:DisableTask 停用，EnableTask 启用，DeleteTask 删除
    :param task_start: 数据库task_record表第几条数据开始，默认为0，第1条数据
    :param task_count: 数据库task_record表取条数据，默认为0，取全部数据
    :return: None
    """
    if task_count:
        if func == "DeleteTask":
            alter_task("DisableTask", task_start, task_count)
        sql = """SELECT `id`,task_name FROM task_record limit {},{};""".format(task_start, task_count)
    else:
        if func == "EnableTask":
            sql = """SELECT `id`,task_name FROM task_record WHERE `state`='DISABLED';"""
        elif func == "DisableTask":
            sql = """SELECT `id`,task_name FROM task_record WHERE `state`='ENABLED';"""
        elif func == "DeleteTask":
            alter_task("DisableTask")
            sql = """SELECT `id`,task_name FROM task_record WHERE `state`='DISABLED';"""
        else:
            sql = ""
            print("请检查sql语句，DisableTaskFlow 停用任务，EnableTaskFlow 启用任务，DeleteTaskFlow 删除任务")
    task_tuple = get_task_id_name(sql)
    # 创建一个包含20条线程的线程池
    pool = ThreadPoolExecutor(max_workers=20)

    for task_id_tuple in task_tuple:
        # 向线程池提交一个task
        pool.submit(do_alter_task, func, task_id_tuple)


def do_alter_task(func, task_id_tuple):
    task_id = task_id_tuple[0]
    task_name = task_id_tuple[1]
    print(task_id)
    params = {"action": func, "serviceType": "tct", "regionId": 1, "data": {"Version": "2018-03-26", "TaskId": task_id}}
    resp = api_post(action="DescribeReleasedConfig", params=params)
    print("正在{}任务：{}".format(func, task_name))
    print(resp)
    print(threading.current_thread().name)


def alter_multi_task(func, task_start=0, task_count=None):
    """
    修改任务状态，task_count=0，修改全部任务
    :param func:DisableMultiTask 停用，EnableMultiTask 启用，DeleteMultiTask 删除
    :param task_start: 数据库task_record表第几条数据开始，默认为0，第1条数据
    :param task_count: 数据库task_record表取条数据，默认为0，取全部数据
    :return: None
    """
    if func == "EnableMultipleTask":
        sql = """SELECT `id`,task_name FROM task_record WHERE `state`='DISABLED' limit {},{};""".format(task_start, task_count)
    elif func == "DisableMultipleTask":
        sql = """SELECT `id`,task_name FROM task_record WHERE `state`='ENABLED' limit {},{};""".format(task_start, task_count)
    elif func == "DeleteMultipleTask":
        alter_multi_task("DisableMultipleTask")
        sql = """SELECT `id`,task_name FROM task_record WHERE `state`='DISABLED' limit {},{};""".format(task_start, task_count)
    else:
        sql = ""
        print("请检查sql语句，DisableTaskFlow 停用任务，EnableTaskFlow 启用任务，DeleteTaskFlow 删除任务")
    task_tuple = get_task_id_name(sql)

    task_ids = []
    for i in task_tuple:
        task_ids.append(i[0])

    sub_count = 1000
    task_ids_size = len(task_ids)
    page_limit = int(task_ids_size / sub_count)
    page_limit += 0 if ((task_ids_size % sub_count) == 0) else 1
    res_list = []
    for i in range(0, page_limit):
        start_off_set = i * sub_count
        end_off_set = ((i + 1)) * sub_count
        end_off_set = end_off_set if end_off_set <= task_ids_size else task_ids_size
        res_list.append(task_ids[start_off_set:end_off_set])

    # 创建一个包含20条线程的线程池
    # pool = ThreadPoolExecutor(max_workers=20)
    for sub_task_ids in res_list:
        do_alter_multi_task(func, sub_task_ids)
    # 向线程池提交一个task
    #     pool.submit(do_alter_multi_task, func, sub_task_ids)


def do_alter_multi_task(func, sub_task_ids):
    params = {"action": func, "serviceType": "tct", "regionId": 1, "data": {"Version": "2018-03-26", "Ids": sub_task_ids}}
    resp = api_post(action="DescribeReleasedConfig", params=params)
    print("正在{}任务：{}".format(func, sub_task_ids))
    print(resp)
    print(threading.current_thread().name)
