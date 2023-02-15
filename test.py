
for task_id_tuple in task_tuple:
    task_id_value = task_id_tuple[0]
    task_name = task_id_tuple[1]
    task_id_list = [str(task_id_value)]
    print(task_id_list)
    # params = {"action": func, "serviceType": "tsf", "regionId": 1, "data": {"Version": "2018-03-26", "Ids": task_id_list}}
    # resp = api_post(action="DescribeReleasedConfig", params=params)
    # print("正在{}任务：{}".format(func, task_name))
    # print(resp)
