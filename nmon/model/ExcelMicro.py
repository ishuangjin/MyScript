#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-12-12 10:11:29
@LastEditTime: 2022-12-13 16:33:03
@FilePath: \\Github\\MyScript\\nmon_auto\\nmon\\ExcelMicro.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''

import win32com.client
import pythoncom
import win32api
import os

from NmonLog import log
'''
    @:param
    micro_file：宏文件(全路径)
    nmon_files：待解析的 nmon 文件
    save_path ：解析文件的储存路径(仅在待解析的 nmon 文件数量为一的时候生效), 不传默认与 nmon 文件同路径
    @:return
    返回解析文件路径
'''


def get_nmon_result_file(micro_file, nmon_files, save_path=""):
    x1 = win32com.client.DispatchEx("Excel.Application")
    # print(x1.Name)
    # print(x1.Version)
    # 进程是否可见, True 为可见, False 为不可见
    # x1.Visible = False
    # x1.DisplayAlerts = 0  # 不警告
    nmon_tuple = [0]
    result_file = []

    for index in range(0, len(nmon_files)):
        check_file(nmon_files[index], nmon_tuple)

    x1.Workbooks.Open(micro_file)

    if save_path != "" and len(nmon_files) == 1:
        result_file.append(save_path)
    elif save_path == "" and len(nmon_files) == 1:
        save_path = nmon_files[0] + ".xlsx"
        result_file.append(save_path)
    else:
        for i in range(0, len(nmon_files)):
            result_file.append(nmon_files[i] + ".xlsx")
            # print("nmon_files[i]:", nmon_files[i])
    # print("save_path:", save_path)
    # print("result_file:", result_file)

    try:
        x1.Application.Run("Main", 0, save_path, nmon_tuple)
        print("save_path:", save_path)
        print("nmon_tuple:", nmon_tuple)
        # Analyze nmon data
    except pythoncom.com_error as error:
        log.error(win32api.FormatMessage(error.excepinfo[0]))
        # pass
    finally:
        x1.Quit()
        x1 = None
        return result_file


'''
    检查给定的数组是否内容为文件
    若为文件夹则将文件夹内的所有文件都添加到数组内
'''


def check_file(nmon_files, file_tuple):
    if os.path.isfile(nmon_files):
        file_tuple.append(nmon_files)
    else:
        file_list = os.listdir(nmon_files)
        for index in range(0, len(file_list)):
            file_name = os.path.join(nmon_files, file_list[index])
            check_file(file_name, file_tuple)


if __name__ == '__main__':
    MircoFilePath = r"D:\Github\MyScript\nmon_auto\nmon\data\nmonanalyserv66.xlsm"
    nmon_files = ['D:\\Github\\MyScript\\nmon_auto\\nmon\\data\\nmon_file_dir\\192.168.77.90\\i-po2dqfef_221213_1414.nmon']
    # path = r"D:\Github\MyScript\nmon_auto\nmon\data\nmon_result_file"
    path = ""
    result = get_nmon_result_file(MircoFilePath, nmon_files, path)
    print(result)