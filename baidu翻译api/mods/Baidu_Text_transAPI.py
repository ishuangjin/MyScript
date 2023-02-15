#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2023-02-09 16:04:01
@LastEditTime: 2023-02-13 13:41:12
@FilePath: \\Github\\MyScript\\baidu翻译api\\mods\\Baidu_Text_transAPI.py
@Copyright (c) 2023 by ${git_name}, All Rights Reserved.
@Description:1. 通过调用百度翻译api实现：输入中文，翻译成英语/繁体/俄语并输出

'''
# -*- coding: utf-8 -*-

# This code shows an example of text translation from English to Simplified-Chinese.
# This code runs on Python 2.7.x and Python 3.x.
# You may install `requests` to run this code: pip install requests
# Please refer to `https://api.fanyi.baidu.com/doc/21` for complete api document

import requests
import random
# import json
from hashlib import md5
import os
import sys
now_path = os.path.dirname(os.path.abspath(__file__))
main_path = os.path.join(now_path, "../")
sys.path.insert(0, main_path)

from config import env_init
# import ReadConfig


ini_path = env_init.ini_path
parser_dict = env_init.parser_dict
# parser_dict = Config.ConfigParser(ini_path)
# print(parser_dict)


class DoTranslate():
    # Set your own appid/appkey.
    appid = parser_dict['appid']
    appkey = parser_dict['appkey']

    def __init__(self, from_lang, to_lang, query) -> None:
        # For list of language codes, please refer to `https://api.fanyi.baidu.com/doc/21`
        self.from_lang = to_lang
        self.to_lang = to_lang

        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        self.url = endpoint + path

        self.query = query

        # Generate salt and sign
        def make_md5(s, encoding='utf-8'):
            return md5(s.encode(encoding)).hexdigest()

        salt = random.randint(32768, 65536)
        sign = make_md5(DoTranslate.appid + query + str(salt) + DoTranslate.appkey)

        # Build request
        self.headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        self.payload = {'appid': DoTranslate.appid, 'q': query, 'from': from_lang, 'to': to_lang, 'salt': salt, 'sign': sign}

    # Send request
    def post(self):
        r = requests.post(self.url, params=self.payload, headers=self.headers)
        api_result = r.json()
        result = api_result["trans_result"][0]["dst"]
        # Show response
        # print(json.dumps(result, indent=4, ensure_ascii=False))
        print(result)
        return result


if __name__ == "__main__":
    ini_path = r'D:\Github\MyScript\baidu翻译api\config\config.ini'
    from_lang = 'en'
    to_lang = 'zh'
    # query = 'Hello World! This is 1st paragraph.\nThis is 2nd paragraph.'
    query = 'Hello World! This is 1st paragraph.'
    trans_A = DoTranslate(from_lang, to_lang, query)
    first_result = trans_A.post()
    trans_B = DoTranslate(to_lang, from_lang, first_result)
    second_restult = trans_B.post()
# end main
