import os

path = r'D:\Github\MyScript\nmon_auto\nmon\data\nmon_file_dir'

file_list = []


def get_all_nmon_file(path):
    if os.path.isfile(path):
        extend = path.rsplit(".", 1)
        if (len(extend) == 2):
            if extend[1] == "nmon":
                file_list.append(path)

    elif os.path.isdir(path):
        for file in os.listdir(path):
            get_all_nmon_file(path + "\\" + file)


get_all_nmon_file(path)
print(file_list)