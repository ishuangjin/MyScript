#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-09-21 17:17:14
@LastEditTime: 2022-09-21 18:40:35
@FilePath: \\Github\\MyScript\\读取xmind\\coding_testcase.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''
import os
from xmindparser import xmind_to_dict
import pandas as pd


def get_data(xm):  # 提取所有用例数据
    # 依次定义用例名称，用例列表，用例步骤，用例结果，用例前置条件
    case_name = []
    case_list = []
    case_step = []
    case_result = []
    case_front = []

    def get_case_name(xm):
        global get_case_name_for
        for i in range(len(xm)):
            get_case_name_for = True
            if xm[i].__contains__('topics'):  # 带topics标签意味着有子标题，递归执行方法
                case_name.append(xm[i]['title'])
                get_case_name(xm[i]['topics'])
            else:  # 不带topics意味着无子标题，此级别既是用例详情
                if xm[i]['title'][:2] == "前置":
                    case_front.append((xm[i]['title'][2:].strip()))
                elif xm[i]['title'][:2] == "步骤":
                    case_step.append((xm[i]['title'][2:].strip()))
                elif xm[i]['title'][:2] == "结果":
                    case_result.append((xm[i]['title'][2:].strip()))

        case_name_str = "_".join(case_name)  # 转化成字符串
        if get_case_name_for:
            case_list.append(case_name_str)
            if len(xm) == 2:  # 如果只有步骤和结果则给前置填充'/'
                case_front.append("/")
        try:
            case_name.pop()
            get_case_name_for = False
        except IndexError:
            print("已获取全部用例名称和用例详情")

    # xm = xmind_to_dict("项目名称.xmind")[0]['topic']['topics']  # 读取xmind文件
    get_case_name(xm)
    case_count = len(case_list)
    # 返回用例数量，用例列表，前置条件列表，用例步骤列表，用例结果列表
    return case_count, case_list, case_front, case_step, case_result


def save_data(xm, file_name="path_to_file.xlsx", case_level="P2") -> None:

    row0 = ["标题", "前置条件", "步骤", "预期结果", "等级"]  # 表头
    some_cos = get_data(xm)

    def lsbd(field):  # list_build，列表长度为用例数量
        return [field for _ in range(some_cos[0])]

    # 构建完整的数据列表，由多个列表组成新的列表
    data_value_list = [some_cos[1], some_cos[2], some_cos[3], some_cos[4], lsbd(case_level)]

    # 将数据转化为字典格式，并将row0表头对应每列数据
    def get_data_value(data_value_list):
        case_data = {}
        n = -1
        for data_title in row0:
            n += 1
            case_data[data_title] = data_value_list[n]
        return case_data

    case_data = get_data_value(data_value_list)
    try:
        df = pd.DataFrame(case_data, columns=row0)
        # print(df.loc[:, "用例名称"], "\n-------------------------\n")
        df.to_excel(file_name, index=None, sheet_name="Sheet1")  # 保存成excel格式
    except ValueError:  # 如果报这个错，可能是用例详情缺少，表的数据长度不一致，不能转成DataFrame格式
        msg = "Error:请检查xmind文件,是否缺失部分用例详情"
    else:
        msg = "success!"
    return print(msg)


def run(xm_file_name):
    # 路径操作
    script_path = os.path.dirname(__file__)  # 当前脚本的绝对路径
    xmind_case = os.path.join(script_path, "XmindCase", xm_file_name)
    excel_case = os.path.join(script_path, "ExcelCase", xm_file_name.replace(".xmind", "coding.xlsx"))
    # case_index = xmind_to_dict(xmind_case)[0]['topic']['title']  # case在tapd上的存放路径，取xmind画布的第一个标题

    xm = xmind_to_dict(xmind_case)[0]['topic']['topics']  # 读取xmind文件
    try:
        save_data(xm=xm, file_name=excel_case)
        print("转化后的文件路径为:", excel_case)
    except PermissionError:
        print("Error:文件被占用,请关闭已打开的xlsx文件")
    else:
        pass


def main():
    # 填写需求ID和xmind文件名
    xm_file_name = "TSF1.29.2to1.29.5组件升级测试用例.xmind"  # 要操作的文件
    run(xm_file_name)


if __name__ == '__main__':
    main()
