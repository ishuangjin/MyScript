import hashlib


def find_md5():
    md = "4d6f497a0966dc30b75c4822b7eb41f2D/76"  # 加密后的
    for i in range(1000000000, 9999999999):
        # print(i)
        md5 = hashlib.md5()  # 获取一个md5加密算法对象
        md5.update(str(i).encode('utf-8'))  # 指定需要加密的字符串
        newmd5 = md5.hexdigest()  # 获取加密后的16进制字符串
        # print newmd5
        if newmd5 == md:
            print('明文是：' + str(i))  # 打印出明文字符串


if __name__ == '__main__':
    find_md5()
