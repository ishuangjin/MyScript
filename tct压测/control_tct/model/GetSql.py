#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-12-15 17:30:54
@LastEditTime: 2023-01-03 15:32:57
@FilePath: \\Github\\MyScript\\tct压测\\control_tct\\model\\GetSql.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description:
'''
import pymysql
import traceback


def get_task_id_name(sql):
    """
    从数据库拿任务的ID
    :param sql: sql语句
    :return: 数据库查询结果，两层元组嵌套((id1,name1),(id2,name2),(id3,name3),(id4,name4)...)
    """
    global sql_results
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
    except Exception:
        traceback.print_exc()
        print("Error: unable to fetch data")
    db.close()
    # print('sql语句:', sql_results, '\n\n\n')
    return sql_results
