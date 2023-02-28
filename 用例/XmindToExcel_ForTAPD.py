#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-08 11:06:56
@LastEditTime: 2023-02-27 14:57:15
@FilePath: \\Github\\MyScript\\用例\\XmindToExcel_ForTAPD.py
@Description: 将Xmind测试用例转化为需要的Excel格式
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
'''
import os
from xmindparser import xmind_to_dict
import pandas as pd


def get_data(xm):  # 提取所有用例数据
    # 依次定义用例名称，用例列表，用例步骤，用例结果，用例前置条件
    print("开始读取xmind文件...")
    case_name = []
    case_list = []
    case_step = []
    case_result = []
    case_front = []
    case_other = []

    def get_case_name(xm):
        global get_case_name_for
        writeTo = 0
        for i in range(len(xm)):
            get_case_name_for = True
            if xm[i].__contains__('topics'):  # 带topics标签意味着有子标题，递归执行方法
                case_name.append(xm[i]['title'])
                get_case_name(xm[i]['topics'])
            else:  # 不带topics意味着无子标题，此级别既是用例详情
                writeTo += 1
                if len(xm) == 1:  # 如果只有一条数据，则判定为未填写用例详情的用例标题
                    case_name.append(xm[0]['title'])
                    case_other.append("-".join(case_name))
                    case_front.append("/")
                    case_step.append("/")
                    case_result.append("/")
                elif len(xm) == 2:  # 如果有两条则依次填入步骤、结果
                    if writeTo % 2:
                        continue
                    else:
                        case_front.append("/")
                        case_step.append(xm[0]['title'])
                        case_result.append(xm[1]['title'])
                elif len(xm) == 3:  # 如果有三条则依次填入前置、步骤、结果
                    if writeTo % 3:
                        continue
                    else:
                        case_front.append(xm[0]['title'])
                        case_step.append(xm[1]['title'])
                        case_result.append(xm[2]['title'])

        if get_case_name_for:  # 每次循环添加最后一级用例名称
            case_list.append("-".join(case_name))  # 转化成字符串，并拼接为完整用例名称
        try:
            case_name.pop()  # 删除最后一级用例名称
            get_case_name_for = False  # 判断进入新的循环
        except IndexError:
            print("done")

    get_case_name(xm)
    print("已获取全部用例名称和用例详情，共 {} 条测试用例\n".format(len(case_list)))
    if case_other:
        print("!!!：请注意，以下用例无用例详情：\n")
        for other in case_other:
            print(other)

    return case_list, case_front, case_step, case_result


def save_data(xm,
              file_name="path_to_file.xlsx",
              case_index="",
              demand_id="/",
              case_type="功能测试",
              case_state="正常",
              case_level="中",
              case_creater="黄金") -> None:
    case_data = {}
    case_data["用例名称"], case_data["前置条件"], case_data["用例步骤"], case_data["预期结果"] = get_data(xm)

    print("开始写入Excel表格...")
    row0 = ["用例目录", "用例名称", "需求ID", "前置条件", "用例步骤", "预期结果", "用例类型", "用例状态", "用例等级", "创建人"]  # 表头
    df = pd.DataFrame(case_data, columns=row0)
    # print("\n-------------------------\n")
    # print(df.loc[:, "用例名称"], "\n-------------------------\n")
    df["用例目录"] = case_index
    df["需求ID"] = demand_id
    df["用例类型"] = case_type
    df["用例状态"] = case_state
    df["用例等级"] = case_level
    df["创建人"] = case_creater
    df.to_excel(file_name, index=None, sheet_name="Sheet1")  # 保存成excel格式

    return print("success!文件已写入Excel表格")


def get_path(xm_file_name):
    # 路径操作
    print("获取路径...")
    script_path = os.path.dirname(__file__)  # 当前脚本的绝对路径
    xmind_case = os.path.join(script_path, "XmindCase", xm_file_name)
    excel_case = os.path.join(script_path, "ExcelCase", xm_file_name.replace(".xmind", ".xlsx"))
    print("获取路径成功\n")

    return excel_case, xmind_case


if __name__ == '__main__':
    # 填写xmind文件名
    xm_file_name = "太保TCT导入导出功能.xmind"  # 要操作的文件
    excel_case, xmind_case = get_path(xm_file_name)  # 获取绝对路径

    case_index = xmind_to_dict(xmind_case)[0]['topic']['title']  # case在tapd上的存放路径，取xmind画布的第一个标题
    xm = xmind_to_dict(xmind_case)[0]['topic']['topics']  # 读取xmind文件
    try:
        save_data(xm=xm, file_name=excel_case, case_index=case_index)  # 保存到Excel
        if os.path.exists(excel_case):
            print("转化后的文件路径为:", excel_case)
    except PermissionError:
        print("Error:文件被占用,请关闭已打开的xlsx文件")
