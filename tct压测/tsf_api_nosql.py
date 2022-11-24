# -*- coding: utf-8 -*-
import argparse
import hashlib, hmac, json, os, sys, time
from datetime import datetime
import requests
import logging
import json


# 租户端
secret_id = "52H5f9G2e7aOc4e9Qd859fb4F5ReTe06"
secret_key = "QeSa56PbafP8O96L0LceN278aI5326Te"

# 接口基础配置
service = "tsf"
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
formatter = logging.Formatter(
    '%(asctime)s - %(filename)s[func:%(funcName)s][line:%(lineno)d] - %(levelname)s: %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)

# 签名方法v3
def get_sign_heades(action, params):
    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = "action=" + action
    ct = "application/json; charset=utf-8"
    payload = json.dumps(params)
    canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
    signed_headers = "content-type;host"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" +
                         canonical_uri + "\n" +
                         canonical_querystring + "\n" +
                         canonical_headers + "\n" +
                         signed_headers + "\n" +
                         hashed_request_payload)
    # print(canonical_request)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" +
                      str(timestamp) + "\n" +
                      credential_scope + "\n" +
                      hashed_canonical_request)

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
    authorization = (algorithm + " " +
                     "Credential=" + secret_id + "/" + credential_scope + ", " +
                     "SignedHeaders=" + signed_headers + ", " +
                     "Signature=" + signature)
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


def get_task(sql_txt):
    task_list = []
    with open(sql_txt, 'r') as f:
        lines = f.readlines()
        for line in lines:
            task_line = line.split()
            task_id = task_line[0]
            task_name = task_line[1]
            task_tuple = (task_id, task_name)
            task_list.append(task_tuple)
        task_tuple = tuple(task_list[1:])
    return task_tuple


def create_random_task(task_start=1, task_end=None, task_name_start="random_task"):
    """
    创建执行方式为随机的任务
    :param task_name_start:任务名字前缀
    :param task_start:任务名字起始
    :param task_end:任务名字结束
    :return: None
    eg:create_random_task(1, 3),创建任务太保_task1、太保_task2、太保_task3
    """
    for num in range(int(task_start), int(task_end) + 1):
        task_name = task_name_start + str(num)
        params = {"action": "CreateTask",
                  "serviceType": "tsf",
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
                          "Expression": "0 0/5 * * * ?"},
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


def create_shard_task(task_start=1, task_end=None, task_name_start="shard_task"):
    """
    创建分片任务
    :param task_name_start:任务名字前缀
    :param task_start:任务名字起始
    :param task_end:任务名字结束
    :return:None
    """
    for num in range(int(task_start), int(task_end) + 1):
        task_name = task_name_start + str(num)
        params = {"action": "CreateTask",
                  "serviceType": "tsf",
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
                          "Expression": "0 0/5 * * * ?"},
                      "ShardArguments": [
                          {
                              "ShardKey": 1,
                              "ShardValue": "a"
                          },
                          {
                              "ShardKey": 2,
                              "ShardValue": "b"
                          },
                          {
                              "ShardKey": 3,
                              "ShardValue": "c"
                          }
                      ],
                      "TaskArgument": "",
                      "ProgramIdList": [],
                      "RetryCount": 0,
                      "RetryInterval": 0,
                      "ShardCount": 3,
                      "AdvanceSettings": {
                          "SubTaskConcurrency": 2
                      }
                  }
                  }

        resp = api_post(action="DescribeReleasedConfig", params=params)
        print("正在创建分片任务：", task_name)
        print(resp)


def alter_task(func, sql_txt, task_start=0, task_count=None):
    task_tuple = get_task(sql_txt)
    for task_id_tuple in task_tuple:
        task_id = task_id_tuple[0]
        task_name = task_id_tuple[1]
        params = {"action": func,
                  "serviceType": "tsf",
                  "regionId": 1,
                  "data": {
                      "Version": "2018-03-26",
                      "TaskId": task_id
                  }
                  }
        resp = api_post(action="DescribeReleasedConfig", params=params)
        print("正在{}任务：{}".format(func, task_name))
        print(resp)


def alter_task_flow(func, sql_txt, task_start=0, task_count=None):
    task_tuple = get_task(sql_txt)
    for task_id_tuple in task_tuple:
        task_id = task_id_tuple[0]
        task_name = task_id_tuple[1]
        params = {"action": func,
                  "serviceType": "tsf",
                  "regionId": 1,
                  "data": {
                      "Version": "2018-03-26",
                      "FlowId": task_id
                  }
                  }
        resp = api_post(action="DescribeReleasedConfig", params=params)
        print("正在{}任务：{}".format(func, task_name))
        print(resp)


def create_task_flow(sql_txt, task_start=0, task_count=0, limit=20, flow_name_start="flow_test"):
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
    sql_results = get_task(sql_txt)  # ((id1,name1),(id2,name2)...)
    # limit = 20  # 每个工作流的任务数
    pagesize = (len(sql_results) // limit) + 1  # 工作流数
    for page_index in range(0, pagesize):  # 第page_index个工作流
        flow_list = []
        sql_results_split = sql_results[page_index * limit: (page_index + 1) * limit]  # 切割总任务，按照每页limit个切分成pagesize个
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
        params = {"action": "CreateTaskFlow",
                  "serviceType": "tsf",
                  "regionId": 1,
                  "data": {
                      "Version": "2018-03-26",
                      "FlowName": flow_name,
                      "TimeOut": 9000000,
                      "TriggerRule": {
                          "RuleType": "Cron",
                          "Expression": "0 0/5 * * * ?"
                      },
                      "FlowEdges": flow_list}}
        create_flow(params=params, flow_name=flow_name)


def main():
    """
    # 创建随机任务 random_task1、random_task2、...random_task100
    # create_random_task(1, 100)

    # 创建分片任务 shard_task1、shard_task2、...shard_task100
    # create_shard_task(1, 100)

    # DisableTask 停用任务，EnableTask 启用任务，DeleteTask 删除任务
    # 改变第1条数据起，一共100条数据的状态为启用
    # alter_task("EnableTask", sql_txt, 0, 100)

    # DisableTaskFlow 停用工作流，EnableTaskFlow 启用工作流，DeleteTaskFlow 删除工作流
    # 改变第200条数据起，一共100条数据的状态为停止
    # alter_task_flow("EnableTaskFlow", sql_txt, 200, 100)

    # 创建工作流任务 flow_test4001、flow_test4002、...flow_test6000
    # create_task_flow(sql_txt, 4000, 2000)
    """

    sql_txt = 'task_record.txt'
    alter_task("DisableTask", sql_txt, 0, 1)


if __name__ == '__main__':
    main()
