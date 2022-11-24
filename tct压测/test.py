

def get_task(sql_txt):
    task_list = []
    with open(sql_txt, 'r') as f:
        lines = f.readlines()
        for line in lines:
            task_line = line.split()
            task_id = task_line[0]
            task_name = task_line[1]
            task_tuple = (task_id, task_name)
            task_list.append(task_tuple)
        task_tuple = tuple(task_list[1:])
    return task_tuple


sql_txt = 'task_record.txt'
s = get_task(sql_txt)
print(s)

