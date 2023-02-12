#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-11-07 12:57:36
@LastEditTime: 2022-12-09 20:11:25
@FilePath: \\Git\\MyScript\\test.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''
import xlrd
import os

import win32com.client
import pythoncom
import win32api

file = 'F:\Git\MyScript\tct压测\nmon\local_data\192.168.77.90\i-o6lll6p5_221129_1110.nmon'
# workbook = xlrd.open_workbook(file)
# print(workbook)
nmon_files = r"F:\Git\MyScript\tct压测\nmon\nmonanalyserv66.xlsm"


def get_nmon_result_file(micro_file, nmon_files, save_path=""):
    x1 = win32com.client.Dispatch("Excel.Application")
    x1.Visible = True
    x1.DisplayAlerts = False
    nmon_tuple = [0]
    result_file = []

    for index in range(0, len(nmon_files)):
        check_file(nmon_files[index], nmon_tuple)

    y = x1.Workbooks.Open(micro_file)

    if save_path != "" and len(nmon_files) == 1:
        result_file.append(save_path)
    elif save_path == "" and len(nmon_files) == 1:
        save_path = nmon_files[0] + ".xlsx"
        result_file.append(save_path)
    else:
        for i in range(0, len(nmon_files)):
            result_file.append(nmon_files[i] + ".xlsx")

    try:
        #  Main代表nmon analyser v46.xlsm VB函数入库名称
        x1.Application.Run("Main", 0, save_path, nmon_tuple)
        y.Save()
        y.Close(SaveChanges=0)
    except pythoncom.com_error as error:
        print(win32api.FormatMessage(error.excepinfo[0]))
    finally:
        x1.Quit()
        x1 = None
        return result_file


def check_file(nmon_files, file_tuple):
    if os.path.isfile(nmon_files):
        file_tuple.append(nmon_files)
    else:
        file_list = os.listdir(nmon_files)
        for index in range(0, len(file_list)):
            file_name = os.path.join(nmon_files, file_list[index])
            check_file(file_name, file_tuple)


get_nmon_result_file(file, nmon_files, save_path="F:\Git\MyScript\tct压测\nmon\nmon_test.xls")