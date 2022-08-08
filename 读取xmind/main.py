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


def save_data(xm,
              file_name="path_to_file.xlsx",
              case_index="",
              demand_id="请填写需求ID",
              case_type="功能测试",
              case_state="正常",
              case_level="中",
              case_creater="黄金") -> None:
    """
    “用例目录”请填写完整路径，用“-”分隔。如果目录为空，默认导入为“未规划目录”中；如果用例目录不存在，请在预览页面选择是否要自动创建目录。
    “用例名称”为必填项。
    “需求ID”请填写需求ID,多个需求ID以英文;号隔开。需求必须是本项目下的需求。
    “前置条件”请填写合法文本。
    “用例步骤”请填写合法文本。
    “预期结果”请填写合法文本。
    “用例类型”请填写：功能测试、性能测试、安全性测试、其他。
    “用例状态”请填写：正常、待更新、已废弃。
    “用例等级”请填写：高、中、低。
    """
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
        print(df.loc[:, "用例名称"], "\n-------------------------\n")
        df.to_excel(file_name, index=None, sheet_name="Sheet1")  # 保存成excel格式
        # print(df)
    except ValueError:  # 如果报这个错，可能是用例详情缺少，表的数据长度不一致，不能转成DataFrame格式
        msg = "Error:请检查xmind文件,是否缺失部分用例详情"
    else:
        msg = "success!"
    return print(msg)


def main():
    # 自定义用例名称和用例详情以外的内容
    case_index = "Redis故障切换"  # case在tapd上的存放路径
    demand_id = "1024593"  # 需求ID
    xm_file_name = "TCT历史执行记录迁移.xmind"  # 要操作的文件

    # 路径操作
    script_path = os.path.dirname(__file__)  # 当前脚本的绝对路径
    xmind_case = os.path.join(script_path, "XmindCase", xm_file_name)
    excel_case = os.path.join(script_path, "ExcelCase", xm_file_name.replace(".xmind", ".xlsx"))

    xm = xmind_to_dict(xmind_case)[0]['topic']['topics']  # 读取xmind文件
    try:
        save_data(xm, excel_case, case_index, demand_id)
        print("转化后的文件路径为:", excel_case)
    except PermissionError:
        print("Error:文件被占用,请关闭已打开的xlsx文件")
    else:
        pass


if __name__ == '__main__':
    main()
