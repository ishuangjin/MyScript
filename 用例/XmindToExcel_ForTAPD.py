#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-08-08 11:06:56
@LastEditTime: 2023-02-22 16:28:01
@FilePath: \\Github\\MyScript\\用例\\XmindToExcel_ForTAPD.py
@Description: 将Xmind测试用例转化为需要的Excel格式
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
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

    # case_other = []

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
                if len(xm) == 2:  # 如果有两条则依次填入步骤、结果
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

        case_name_str = "-".join(case_name)  # 转化成字符串
        # print(case_name_str)
        if get_case_name_for:
            case_list.append(case_name_str)
        try:
            case_name.pop()
            get_case_name_for = False
        except IndexError:
            print("已获取全部用例名称和用例详情，共 {} 条测试用例\n".format(len(case_list)))

    get_case_name(xm)
    # 返回用例数量，用例列表，前置条件列表，用例步骤列表，用例结果列表
    # print(len(case_list))
    # print(len(case_front))
    # print(len(case_step))
    # print(len(case_result))
    return len(case_list), case_list, case_front, case_step, case_result


def save_data(xm,
              file_name="path_to_file.xlsx",
              case_index="",
              demand_id="",
              case_type="功能测试",
              case_state="正常",
              case_level="中",
              case_creater="黄金") -> None:
    row0 = ["用例目录", "用例名称", "需求ID", "前置条件", "用例步骤", "预期结果", "用例类型", "用例状态", "用例等级", "创建人"]  # 表头
    some_cos = get_data(xm)

    def lsbd(field):  # list_build，列表长度为用例数量
        return [field for _ in range(some_cos[0])]

    # 构建完整的数据列表，由多个列表组成新的列表
    data_value_list = [
        lsbd(case_index), some_cos[1],
        lsbd(demand_id), some_cos[2], some_cos[3], some_cos[4],
        lsbd(case_type),
        lsbd(case_state),
        lsbd(case_level),
        lsbd(case_creater)
    ]

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
        print("开始写入Excel表格...")
        df.to_excel(file_name, index=None, sheet_name="Sheet1")  # 保存成excel格式
        # print(df)
    except ValueError:  # 如果报这个错，可能是用例详情缺少，表的数据长度不一致，不能转成DataFrame格式
        msg = "Error:请检查xmind文件,是否缺失部分用例详情"
    else:
        msg = "success!"
    return print(msg)


def run(xm_file_name, demand_id):
    # 路径操作
    print("获取路径...")
    script_path = os.path.dirname(__file__)  # 当前脚本的绝对路径
    xmind_case = os.path.join(script_path, "XmindCase", xm_file_name)
    excel_case = os.path.join(script_path, "ExcelCase", xm_file_name.replace(".xmind", ".xlsx"))
    case_index = xmind_to_dict(xmind_case)[0]['topic']['title']  # case在tapd上的存放路径，取xmind画布的第一个标题
    print("获取路径成功\n")

    print("开始读取xmind文件...")
    xm = xmind_to_dict(xmind_case)[0]['topic']['topics']  # 读取xmind文件
    try:
        save_data(xm=xm, file_name=excel_case, case_index=case_index, demand_id=demand_id)
        if os.path.exists(excel_case):
            print("转化后的文件路径为:", excel_case)
    except PermissionError:
        print("Error:文件被占用,请关闭已打开的xlsx文件")
    else:
        pass


if __name__ == '__main__':
    # 填写需求ID和xmind文件名
    demand_id = "/"  # 需求ID
    xm_file_name = "科园核销测试用例 - 副本.xmind"  # 要操作的文件
    run(xm_file_name, demand_id)
