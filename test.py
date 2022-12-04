#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-11-07 12:57:36
@LastEditTime: 2022-11-29 10:24:12
@FilePath: \\Git\\MyScript\\test.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''
import pymysql


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


sql = """SELECT `id`,task_name FROM task_record WHERE `state`='DISABLED';"""
# print(get_task_id_name(sql))

task_tuple = get_task_id_name(sql)

for task_id_tuple in task_tuple:
    task_id_value = task_id_tuple[0]
    task_name = task_id_tuple[1]
    task_id_list = [str(task_id_value)]
    print(task_id_list)
    # params = {"action": func, "serviceType": "tsf", "regionId": 1, "data": {"Version": "2018-03-26", "Ids": task_id_list}}
    # resp = api_post(action="DescribeReleasedConfig", params=params)
    # print("正在{}任务：{}".format(func, task_name))
    # print(resp)