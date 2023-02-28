# -*- coding: utf-8 -*-
import argparse
import hashlib, hmac, json, os, sys, time
from datetime import datetime
import requests
import logging
import pandas as pd
import json
import pymysql
import random
from concurrent.futures import ThreadPoolExecutor
import threading
import time

# 租户端
secret_id = "b5771VXCcW8bR4O7f8F3Td1ebb7da61K"
secret_key = "35BcZcLGaa9U7f3cYcGQ8cE5H513aae2"

# 接口基础配置
service = "192"
host = "192.168.77.2"
port = 80
endpoint = "http://" + host
region = "Service-availability-zone"
version = "2018-03-26"
algorithm = "TC3-HMAC-SHA256"
timestamp = int(time.time())
date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

# logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(filename)s[func:%(funcName)s][line:%(lineno)d] - %(levelname)s: %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)


# 签名方法v3
def get_sign_heades(action, params):
    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = ""
    ct = "application/json; charset=utf-8"
    payload = json.dumps(params)
    canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
    signed_headers = "content-type;host"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" + canonical_uri + "\n" + canonical_querystring + "\n" + canonical_headers +
                         "\n" + signed_headers + "\n" + hashed_request_payload)
    # print(canonical_request)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" + str(timestamp) + "\n" + credential_scope + "\n" + hashed_canonical_request)

    # print(string_to_sign)

    # ************* 步骤 3：计算签名 *************
    # 计算签名摘要函数
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    # print(signature)

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " + "Credential=" + secret_id + "/" + credential_scope + ", " + "SignedHeaders=" +
                     signed_headers + ", " + "Signature=" + signature)
    # print(authorization)
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": version,
        "X-TC-Region": region,
    }
    return headers


def api_post(action, params):
    # 获取签名请求头
    headers = get_sign_heades(action=action, params=params)
    url = "http://" + host + "/apiDispatch/v3?action=" + action
    r = requests.post(url=url, headers=headers, data=json.dumps(params))

    return r.text


def get_task_id_name(sql):
    """
    从数据库拿任务的ID
    :param sql: sql语句
    :return: 数据库查询结果，两层元组嵌套((id1,name1),(id2,name2),(id3,name3),(id4,name4)...)
    """
    # global sql_results
    db_cfg = {'host': '192.168.77.4', 'database': 'task_schedule', 'user': 'root', 'password': 'Tcdn@2007'}
    db = pymysql.connect(host=db_cfg['host'],
                         database=db_cfg['database'],
                         user=db_cfg['user'],
                         password=db_cfg['password'],
                         charset='utf8mb4')
    cursor = db.cursor()
    # sql = """SELECT `id`,`task_name` FROM `task_record` limit 2000;"""
    try:
        cursor.execute(sql)
        sql_results = cursor.fetchall()
        # print(sql_results)
    except:
        import traceback
        traceback.print_exc()
        print("Error: unable to fetch data")
    db.close()
    # print('sql语句:', sql_results, '\n\n\n')
    return sql_results


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


def create_shard_task(task_start=1, task_end=100, task_name_start="shard_task"):
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

        resp = api_post(action="DescribeReleasedConfig", params=params)
        print("正在创建分片任务：", task_name)
        print(resp)


def alter_task(func, task_start=0, task_count=None):
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
            sql = """SELECT `id`,task_name FROM task_record WHERE `state`='DISABLED' limit {},{};""".format(
                task_start, task_count)
        elif func == "DisableTask":
            sql = """SELECT `id`,task_name FROM task_record WHERE `state`='ENABLED'  limit {},{};""".format(
                task_start, task_count)
        elif func == "DeleteTask":
            alter_task("DisableTask")
            sql = """SELECT `id`,task_name FROM task_record WHERE `state`='DISABLED'  limit {},{};""".format(
                task_start, task_count)
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


def alter_task_flow(func, task_start=0, task_count=None):
    """
    修改工作流状态
    :param func: DisableTaskFlow 停用，EnableTaskFlow 启用，DeleteTaskFlow 删除
    :param task_start: 取第task_start个开始
    :param task_count: 共task_count个工作流
    :return: None
    """
    if task_start and task_count:
        if func == "DeleteTaskFlow":
            alter_task("DisableTask", task_start, task_count)
        sql = """SELECT `id`,flow_name FROM task_flow limit {},{};""".format(task_start, task_count)
    else:
        if func == "EnableTaskFlow":
            sql = """SELECT `id`,flow_name FROM task_flow WHERE `state`='DISABLED';"""
        elif func == "DisableTaskFlow":
            sql = """SELECT `id`,flow_name FROM task_flow WHERE `state`='ENABLED';"""
        elif func == "DeleteTaskFlow":
            alter_task("DisableTask")
            sql = """SELECT `id`,flow_name FROM task_flow WHERE `state`='DISABLED';"""
        else:
            sql = ""
            print("请检查sql语句，DisableTaskFlow 停用工作流，EnableTaskFlow 启用工作流，DeleteTaskFlow 删除工作流")
    task_tuple = get_task_id_name(sql)
    for task_id_tuple in task_tuple:
        task_id = task_id_tuple[0]
        task_name = task_id_tuple[1]
        params = {"action": func, "serviceType": "tct", "regionId": 1, "data": {"Version": "2018-03-26", "FlowId": task_id}}
        resp = api_post(action="DescribeReleasedConfig", params=params)
        print("正在{}任务：{}".format(func, task_name))
        print(resp)


def create_task_flow(task_start=0, task_count=0, limit=20, flow_name_start="flow_test"):
    """
    创建工作流，取第task_start个开始，共task_count个任务组装，每个工作流的任务数limit默认为20
    :param flow_name_start:
    :param task_start:取第task_start个开始
    :param task_count:共task_count个任务组装
    :param limit:每个工作流的任务数
    :return:
    """

    def create_flow(params, flow_name):
        print('开始创建工作流:' + flow_name)
        resp = api_post(action="CreateTaskFlow", params=params)
        print(resp)

    sql = """SELECT `id`,`task_name` FROM `task_record` limit {},{};""".format(task_start, task_count)
    sql_results = get_task_id_name(sql)  # ((id1,name1),(id2,name2)...)
    # limit = 20  # 每个工作流的任务数
    pagesize = (len(sql_results) // limit) + 1  # 工作流数
    for page_index in range(0, pagesize):  # 第page_index个工作流
        flow_list = []
        sql_results_split = sql_results[page_index * limit:(page_index + 1) * limit]  # 切割总任务，按照每页limit个切分成pagesize个
        if len(sql_results_split) != limit:  # 如果存在不够limit个任务的退出循环
            break
        # print('第{}个工作流:'.format(page_index))
        # print(sql_results_split, '\n\n\n')
        for i in range(len(sql_results_split)):  # 遍历工作流所有任务
            if i == 0:
                node_task_flow_edge = {
                    "NodeId": 1,
                    "NodeName": "head",
                    "ChildNodeId": sql_results_split[0][0],
                    "CoreNode": "N",
                    "EdgeType": "Y",
                    "NodeType": "START",
                    "PositionX": 40,
                    "PositionY": 160
                }
                flow_list.append(node_task_flow_edge)
                node_task_flow_edge_end = {}
            else:
                s1 = sql_results_split[i][0]
                node_task_flow_edge = {
                    "NodeId": sql_results_split[0][0],  # 父节点ID
                    "NodeName": sql_results_split[0][1],  # 父节点名字
                    "ChildNodeId": s1,  # 当前节点id
                    "CoreNode": "Y",
                    "EdgeType": "Y",
                    "NodeType": "TASK",
                    "PositionX": 360,
                    "PositionY": 120
                }
                flow_list.append(node_task_flow_edge)
                node_task_flow_edge_end = {
                    "NodeId": sql_results_split[i][0],
                    "NodeName": sql_results_split[i][1],
                    "CoreNode": "N",
                    "NodeType": "TASK",
                    "PositionX": 630,
                    "PositionY": i * 100
                }
                flow_list.append(node_task_flow_edge_end)
        if task_start:  # 开始的任务不为0，则任务名续接之前的
            flow_name = flow_name_start + str(page_index + 1 + task_start // limit)
        else:  # 开始的任务为0，则任务名从1开始
            flow_name = flow_name_start + str(page_index + 1)
        params = {
            "action": "CreateTaskFlow",
            "serviceType": "tct",
            "regionId": 1,
            "data": {
                "Version": "2018-03-26",
                "FlowName": flow_name,
                "TimeOut": 9000000,
                "TriggerRule": {
                    "RuleType": "Cron",
                    "Expression": "0 0/5 * * * ?"
                },
                "FlowEdges": flow_list
            }
        }
        create_flow(params=params, flow_name=flow_name)


def main():

    # 创建随机任务 random_task1、random_task2、...random_task100
    # create_random_task(1, 10000)

    # 创建分片任务 shard_task1、shard_task2、...shard_task100
    # create_shard_task(1, 10000)

    # DisableTask 停用任务，EnableTask 启用任务，DeleteTask 删除任务
    # 改变第1条数据起，一共100条数据的状态为启用
    # alter_task("EnableTask", 0, 1)

    # DisableMultipleTask 停用任务，EnableMultipleTask 启用任务，DeleteMultipleTask 删除任务
    # 改变第1条数据起，一共100条数据的状态为启用
    # alter_multi_task("EnableMultipleTask", 0, 1)

    # DisableTaskFlow 停用工作流，EnableTaskFlow 启用工作流，DeleteTaskFlow 删除工作流
    # 改变第200条数据起，一共100条数据的状态为停止
    # alter_task_flow("EnableTaskFlow", 200, 100)

    # 创建工作流任务 flow_test4001、flow_test4002、...flow_test6000
    # create_task_flow(4000, 2000)

    # alter_task("DisableTask", 0, 1)


if __name__ == '__main__':
    main()
