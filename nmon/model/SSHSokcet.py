#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-11-30 09:54:57
@LastEditTime: 2022-12-15 14:25:43
@FilePath: \\Github\\MyScript\\nmon\\model\\SSHSokcet.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: SSH 连接远程服务器下载指定文件夹或文件
'''

import paramiko
import os
from stat import S_ISDIR
from model.NmonLog import log


class sshSocket(object):

    def __init__(self, hostname, username, password):
        tran = paramiko.Transport((hostname, 22))
        tran.connect(username=username, password=password)
        self.sftp = paramiko.SFTPClient.from_transport(tran)
        self.hostname = hostname

    def get_all_file(self, path, basepath, filelist):

        files = self.sftp.listdir_attr(path)

        if basepath == path:
            last_index = basepath.rfind("/")

            root = basepath[last_index + 1:]
            basepath = basepath[:last_index]

            if root == "":
                last_index = basepath[:last_index].rfind("/")
                root = basepath[last_index + 1:]
                basepath = basepath[:last_index]
        else:
            root = path[basepath.__len__() + 1:]

        for file in files:
            if S_ISDIR(file.st_mode):
                newpath = path + "/" + file.filename
                self.get_all_file(newpath, basepath, filelist)
            else:
                if root == "":
                    filelist.append(file.filename)
                else:
                    filelist.append(root + "/" + file.filename)

        return filelist

    def download_file(self, filespath, localpath, remotepath):
        log.info("======开始下载" + self.hostname + "上的监控文件=======")

        if not os.path.exists(localpath):
            os.makedirs(localpath)

        # 替换下载的 nmon 监控文件根目录名称为服务器ip
        winfilespath = []

        for filepath in filespath:
            index = filepath.find("/")
            winfilespath.append(self.hostname + filepath[index:])

        for filepath in winfilespath:
            winfilepath = localpath + "\\" + filepath.replace("/", "\\")
            winpathindex = winfilepath.rfind("\\")
            winpath = winfilepath[:winpathindex]
            root_index = filepath.find("/")
            log.info("正在下载:" + winfilepath[winpathindex + 1:])
            if not os.path.exists(winpath):
                os.makedirs(winpath)

            file = open(winfilepath, 'w')
            file.close()
            self.sftp.get(remotepath + "/" + filepath[root_index:], winfilepath)

        log.info("======" + self.hostname + "监控文件下载完成=======")

    def close(self):
        self.sftp.close()


if __name__ == "__main__":
    hostname = "192.168.77.90"
    uesrname = "root"
    password = "Meiyisi@123"
    remotePath = r"/random1"
    localPath = r"G:\Git\MyScript\tct压测\nmon\local_data"
    ssh = sshSocket(hostname=hostname, username=uesrname, password=password)
    files = ssh.get_all_file(remotePath, remotePath, [])
    ssh.download_file(files, localPath, remotePath)
    ssh.close()
