from xmindparser import xmind_to_dict
import pandas as pd


def get_data(xm):  # 提取所有用例数据
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
                if xm[i]['title'][:3] == "前置：":
                    case_front.append(xm[i]['title'][3:])
                elif xm[i]['title'][:3] == "步骤：":
                    case_step.append(xm[i]['title'][3:])
                elif xm[i]['title'][:3] == "结果：":
                    case_result.append(xm[i]['title'][3:])

        case_name_str = "_".join(case_name)  # 转化成字符串
        if get_case_name_for:
            case_list.append(case_name_str)
            if len(xm) == 2:  # 如果只有步骤和结果则给前置填充'/'
                case_front.append("/")
        try:
            case_name.pop()
            get_case_name_for = False
        except IndexError:
            pass

    # xm = xmind_to_dict("项目名称.xmind")[0]['topic']['topics']  # 读取xmind文件
    get_case_name(xm)
    # case_list.pop()
    case_count = len(case_list)
    # print(json.dumps(xm, indent=2, ensure_ascii=False))
    return case_count, case_list, case_front, case_step, case_result


def save_data(xm,
              file_name="path_to_file.xlsx",
              case_index="",
              demand_id="请填写需求ID",
              case_type="功能测试",
              case_state="正常",
              case_level="中",
              case_creater="黄金"):
    """
        “用例目录”请填写完整路径，用“-”分隔。如果目录为空，默认导入为“未规划目录”中；如果用例目录不存在，请在预览页面选择是否要自动创建目录。
        “用例名称”为必填项。
        “需求ID”请填写需求ID，多个需求ID以英文;号隔开。需求必须是本项目下的需求。
        “前置条件”请填写合法文本。
        “用例步骤”请填写合法文本。
        “预期结果”请填写合法文本。
        “用例类型”请填写：功能测试、性能测试、安全性测试、其他。
        “用例状态”请填写：正常、待更新、已废弃。
        “用例等级”请填写：高、中、低。	人员类型字段请填写人员的昵称。
        “回归状态”（单选字段）请填写以下选项之一：OK、NG	日期型字段格式为：YYYY-MM-DD。	人员类型字段请填写人员的昵称。	日期型字段格式为：YYYY-MM-DD。
        """
    row0 = [
        "用例目录", "用例名称", "需求ID", "前置条件", "用例步骤", "预期结果", "用例类型", "用例状态", "用例等级",
        "创建人", "回归状态", "回归时间", "执行人", "执行时间", "备注", "实际结果"
    ]
    some_cos = get_data(xm)

    def lsbd(field):  # list_build
        return [field for _ in range(some_cos[0])]

    data_value_list = [
        lsbd(case_index), some_cos[1],
        lsbd(demand_id), some_cos[2], some_cos[3], some_cos[4],
        lsbd(case_type),
        lsbd(case_state),
        lsbd(case_level),
        lsbd(case_creater),
        lsbd(""),
        lsbd(""),
        lsbd(""),
        lsbd(""),
        lsbd(""),
        lsbd("")
    ]

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
        df.to_excel(file_name, index=None, sheet_name="Sheet1")
        # print(df)
    except ValueError:
        print("Error：请检查xmind文件，用例详情是否缺失")


def main():
    xmind_file = r"D:\pythonProject\读取xmind\Redis故障切换测试用例.xmind"  # 要操作的文件
    file_name = xmind_file.replace(".xmind", ".xlsx")
    case_index = "Redis故障切换"  # case存放路径 # 南网-TSF应用安全合规性检查不合规整改方案
    demand_id = "1024593"  # 需求ID

    xm = xmind_to_dict(xmind_file)[0]['topic']['topics']  # 读取xmind文件
    try:
        save_data(xm, file_name, case_index, demand_id)
    except PermissionError:
        print("Error：文件被占用，请关闭已打开的xlsx文件")
    else:
        print("Done")


if __name__ == '__main__':
    main()
