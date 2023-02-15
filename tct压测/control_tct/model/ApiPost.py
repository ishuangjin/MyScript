#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-12-15 17:26:42
@LastEditTime: 2023-01-03 14:43:44
@FilePath: \\Github\\MyScript\\tct压测\\control_tct\\model\\SetHeader.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description:
'''
# -*- coding: utf-8 -*-
# import argparse
import hashlib
import hmac
import json
# import os
# import sys
import time
from datetime import datetime
import requests
import logging
# import pandas as pd
# import json
# import pymysql
# import random
# from concurrent.futures import ThreadPoolExecutor
# import threading
# import time

# 租户端
secret_id = "b5771VXCcW8bR4O7f8F3Td1ebb7da61K"
secret_key = "35BcZcLGaa9U7f3cYcGQ8cE5H513aae2"

# 接口基础配置
service = "tsf"
host = "192.168.77.2"
port = 80
endpoint = "http://" + host
region = "Service-availability-zone"
version = "2018-03-26"
algorithm = "TC3-HMAC-SHA256"
timestamp = int(time.time())
date = datetime.utcfromtimestamp(timestamp).strftime("%Y-%m-%d")

# logger
logger = logging.getLogger(__name__)
logger.setLevel(level=logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(filename)s[func:%(funcName)s][line:%(lineno)d] - %(levelname)s: %(message)s')
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)


# 签名方法v3
def get_sign_heades(action, params):
    # ************* 步骤 1：拼接规范请求串 *************
    http_request_method = "POST"
    canonical_uri = "/"
    canonical_querystring = "action=" + action
    ct = "application/json; charset=utf-8"
    payload = json.dumps(params)
    canonical_headers = "content-type:%s\nhost:%s\n" % (ct, host)
    signed_headers = "content-type;host"
    hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
    canonical_request = (http_request_method + "\n" + canonical_uri + "\n" + canonical_querystring + "\n" + canonical_headers +
                         "\n" + signed_headers + "\n" + hashed_request_payload)
    # print(canonical_request)

    # ************* 步骤 2：拼接待签名字符串 *************
    credential_scope = date + "/" + service + "/" + "tc3_request"
    hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
    string_to_sign = (algorithm + "\n" + str(timestamp) + "\n" + credential_scope + "\n" + hashed_canonical_request)

    # print(string_to_sign)

    # ************* 步骤 3：计算签名 *************
    # 计算签名摘要函数
    def sign(key, msg):
        return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

    secret_date = sign(("TC3" + secret_key).encode("utf-8"), date)
    secret_service = sign(secret_date, service)
    secret_signing = sign(secret_service, "tc3_request")
    signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
    # print(signature)

    # ************* 步骤 4：拼接 Authorization *************
    authorization = (algorithm + " " + "Credential=" + secret_id + "/" + credential_scope + ", " + "SignedHeaders=" +
                     signed_headers + ", " + "Signature=" + signature)
    # print(authorization)
    headers = {
        "Authorization": authorization,
        "Content-Type": "application/json; charset=utf-8",
        "Host": host,
        "X-TC-Action": action,
        "X-TC-Timestamp": str(timestamp),
        "X-TC-Version": version,
        "X-TC-Region": region,
    }
    return headers


def api_post(action, params):
    # 获取签名请求头
    headers = get_sign_heades(action=action, params=params)
    url = "http://" + host + "/apiDispatch/v3?action=" + action
    r = requests.post(url=url, headers=headers, data=json.dumps(params))

    return r.text
