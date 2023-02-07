#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-12-15 17:32:50
@LastEditTime: 2023-01-03 17:31:19
@FilePath: \\Github\\MyScript\\tct压测\\control_tct\\run.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description:
'''
from model.FlowControl import *
from model.TaskControl import create_random_task, create_shard_task, alter_task, alter_multi_task
import argparse

parser = argparse.ArgumentParser(description='TCT任务控制台')
# 给这个解析对象添加命令行参数
parser.add_argument('type', type=str, help='类型：任务/工作流')
parser.add_argument('func', type=str, help='操作：创建/删除/启用/停用')
parser.add_argument('-r', '--radius', type=int, help='Radius of cylinder')
parser.add_argument('-H', '--height', type=int, help='Height of cylinder')
args = parser.parse_args()  # 获取所有参数


def main():

    # 创建随机任务 random_task1、random_task2、...random_task100
    # create_random_task(1, 100)

    # 创建分片任务 shard_task1、shard_task2、...shard_task100
    # create_shard_task(9001, 10000)

    # DisableTask 停用任务，EnableTask 启用任务，DeleteTask 删除任务
    # 改变第1条数据起，一共100条数据的状态为启用
    # alter_task("DisableTask", 0, 10000)

    # DisableMultipleTask 停用任务，EnableMultipleTask 启用任务，DeleteMultipleTask 删除任务
    # 改变第1条数据起，一共100条数据的状态为启用
    alter_multi_task("EnableMultipleTask", 0, 3000)

    # DisableTaskFlow 停用工作流，EnableTaskFlow 启用工作流，DeleteTaskFlow 删除工作流
    # 改变第200条数据起，一共100条数据的状态为停止
    # alter_task_flow("EnableTaskFlow", 200, 100)

    # 创建工作流任务 flow_test4001、flow_test4002、...flow_test6000
    # create_task_flow(4000, 2000)

    # alter_task("DisableTask", 0, 1)


if __name__ == '__main__':
    main()
