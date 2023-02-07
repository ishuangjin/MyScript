def alter_task_flow(func, task_start=0, task_count=None):
    """
    修改工作流状态
    :param func: DisableTaskFlow 停用，EnableTaskFlow 启用，DeleteTaskFlow 删除
    :param task_start: 取第task_start个开始
    :param task_count: 共task_count个工作流
    :return: None
    """
    if task_start and task_count:
        if func == "DeleteTaskFlow":
            alter_task("DisableTask", task_start, task_count)
        sql = """SELECT `id`,flow_name FROM task_flow limit {},{};""".format(task_start, task_count)
    else:
        if func == "EnableTaskFlow":
            sql = """SELECT `id`,flow_name FROM task_flow WHERE `state`='DISABLED';"""
        elif func == "DisableTaskFlow":
            sql = """SELECT `id`,flow_name FROM task_flow WHERE `state`='ENABLED';"""
        elif func == "DeleteTaskFlow":
            alter_task("DisableTask")
            sql = """SELECT `id`,flow_name FROM task_flow WHERE `state`='DISABLED';"""
        else:
            sql = ""
            print("请检查sql语句，DisableTaskFlow 停用工作流，EnableTaskFlow 启用工作流，DeleteTaskFlow 删除工作流")
    task_tuple = get_task_id_name(sql)
    for task_id_tuple in task_tuple:
        task_id = task_id_tuple[0]
        task_name = task_id_tuple[1]
        params = {"action": func, "serviceType": "tct", "regionId": 1, "data": {"Version": "2018-03-26", "FlowId": task_id}}
        resp = api_post(action="DescribeReleasedConfig", params=params)
        print("正在{}任务：{}".format(func, task_name))
        print(resp)


def create_task_flow(task_start=0, task_count=0, limit=20, flow_name_start="flow_test"):
    """
    创建工作流，取第task_start个开始，共task_count个任务组装，每个工作流的任务数limit默认为20
    :param flow_name_start:
    :param task_start:取第task_start个开始
    :param task_count:共task_count个任务组装
    :param limit:每个工作流的任务数
    :return:
    """

    def create_flow(params, flow_name):
        print('开始创建工作流:' + flow_name)
        resp = api_post(action="CreateTaskFlow", params=params)
        print(resp)

    sql = """SELECT `id`,`task_name` FROM `task_record` limit {},{};""".format(task_start, task_count)
    sql_results = get_task_id_name(sql)  # ((id1,name1),(id2,name2)...)
    # limit = 20  # 每个工作流的任务数
    pagesize = (len(sql_results) // limit) + 1  # 工作流数
    for page_index in range(0, pagesize):  # 第page_index个工作流
        flow_list = []
        sql_results_split = sql_results[page_index * limit:(page_index + 1) * limit]  # 切割总任务，按照每页limit个切分成pagesize个
        if len(sql_results_split) != limit:  # 如果存在不够limit个任务的退出循环
            break
        # print('第{}个工作流:'.format(page_index))
        # print(sql_results_split, '\n\n\n')
        for i in range(len(sql_results_split)):  # 遍历工作流所有任务
            if i == 0:
                node_task_flow_edge = {
                    "NodeId": 1,
                    "NodeName": "head",
                    "ChildNodeId": sql_results_split[0][0],
                    "CoreNode": "N",
                    "EdgeType": "Y",
                    "NodeType": "START",
                    "PositionX": 40,
                    "PositionY": 160
                }
                flow_list.append(node_task_flow_edge)
                node_task_flow_edge_end = {}
            else:
                s1 = sql_results_split[i][0]
                node_task_flow_edge = {
                    "NodeId": sql_results_split[0][0],  # 父节点ID
                    "NodeName": sql_results_split[0][1],  # 父节点名字
                    "ChildNodeId": s1,  # 当前节点id
                    "CoreNode": "Y",
                    "EdgeType": "Y",
                    "NodeType": "TASK",
                    "PositionX": 360,
                    "PositionY": 120
                }
                flow_list.append(node_task_flow_edge)
                node_task_flow_edge_end = {
                    "NodeId": sql_results_split[i][0],
                    "NodeName": sql_results_split[i][1],
                    "CoreNode": "N",
                    "NodeType": "TASK",
                    "PositionX": 630,
                    "PositionY": i * 100
                }
                flow_list.append(node_task_flow_edge_end)
        if task_start:  # 开始的任务不为0，则任务名续接之前的
            flow_name = flow_name_start + str(page_index + 1 + task_start // limit)
        else:  # 开始的任务为0，则任务名从1开始
            flow_name = flow_name_start + str(page_index + 1)
        params = {
            "action": "CreateTaskFlow",
            "serviceType": "tct",
            "regionId": 1,
            "data": {
                "Version": "2018-03-26",
                "FlowName": flow_name,
                "TimeOut": 9000000,
                "TriggerRule": {
                    "RuleType": "Cron",
                    "Expression": "0 0/5 * * * ?"
                },
                "FlowEdges": flow_list
            }
        }
        create_flow(params=params, flow_name=flow_name)
