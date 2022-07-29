# 批量 创建文件夹
import os  # 倒入OS模块 创建文件夹 需要的
import stat

# for root, dirs, files in os.walk(os.getcwd(), topdown=False):
#     os.chmod(root, stat.S_IREAD)
root = os.getcwd()

# 创建10个文件夹，序号为0-9
for i in range(10):
    path_jin = os.path.join(root, 'jin{}'.format(i+1))
    # isExists = os.path.exists(path_jin + str(i + 1))
    isExists = os.path.exists(path_jin)
    if not isExists:
        # print(path_jin + str(i + 1))
        print(path_jin)
        # os.makedirs(path_jin + str(i + 1))
