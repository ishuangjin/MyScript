#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-12-15 17:26:42
@LastEditTime: 2023-03-15 15:47:48
@FilePath: \\Github\\MyScript\\tct压测\\control_tct\\model\\ApiPost.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description:
'''
# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import time
from datetime import datetime
import requests
import logging


class ApiPost():

    def __init__(self):
        # 租户端
        self.secret_id = "b5771VXCcW8bR4O7f8F3Td1ebb7da61K"
        self.secret_key = "35BcZcLGaa9U7f3cYcGQ8cE5H513aae2"

        # 接口基础配置
        self.service = "tsf"
        self.host = "192.168.77.2"
        self.port = 80
        self.endpoint = "http://" + self.host
        self.region = "Service-availability-zone"
        self.version = "2018-03-26"
        self.algorithm = "TC3-HMAC-SHA256"
        self.timestamp = int(time.time())
        self.date = datetime.utcfromtimestamp(self.timestamp).strftime("%Y-%m-%d")

        # logger
        logger = logging.getLogger(__name__)
        logger.setLevel(level=logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(filename)s[func:%(funcName)s][line:%(lineno)d] - %(levelname)s: %(message)s')
        console = logging.StreamHandler()
        console.setLevel(logging.INFO)
        console.setFormatter(formatter)
        logger.addHandler(console)

    # 签名方法v3
    def get_sign_heades(self, action, params):
        # ************* 步骤 1：拼接规范请求串 *************
        http_request_method = "POST"
        canonical_uri = "/"
        canonical_querystring = "action=" + action
        ct = "application/json; charset=utf-8"
        payload = json.dumps(params)
        canonical_headers = "content-type:%s\nhost:%s\n" % (ct, self.host)
        signed_headers = "content-type;host"
        hashed_request_payload = hashlib.sha256(payload.encode("utf-8")).hexdigest()
        canonical_request = (http_request_method + "\n" + canonical_uri + "\n" + canonical_querystring + "\n" +
                             canonical_headers + "\n" + signed_headers + "\n" + hashed_request_payload)
        # print(canonical_request)

        # ************* 步骤 2：拼接待签名字符串 *************
        credential_scope = self.date + "/" + self.service + "/" + "tc3_request"
        hashed_canonical_request = hashlib.sha256(canonical_request.encode("utf-8")).hexdigest()
        string_to_sign = (self.algorithm + "\n" + str(self.timestamp) + "\n" + credential_scope + "\n" +
                          hashed_canonical_request)

        # print(string_to_sign)

        # ************* 步骤 3：计算签名 *************
        # 计算签名摘要函数
        def sign(key, msg):
            return hmac.new(key, msg.encode("utf-8"), hashlib.sha256).digest()

        secret_date = sign(("TC3" + self.secret_key).encode("utf-8"), self.date)
        secret_service = sign(secret_date, self.service)
        secret_signing = sign(secret_service, "tc3_request")
        signature = hmac.new(secret_signing, string_to_sign.encode("utf-8"), hashlib.sha256).hexdigest()
        # print(signature)

        # ************* 步骤 4：拼接 Authorization *************
        authorization = (self.algorithm + " " + "Credential=" + self.secret_id + "/" + credential_scope + ", " +
                         "SignedHeaders=" + signed_headers + ", " + "Signature=" + signature)
        # print(authorization)
        headers = {
            "Authorization": authorization,
            "Content-Type": "application/json; charset=utf-8",
            "Host": self.host,
            "X-TC-Action": action,
            "X-TC-Timestamp": str(self.timestamp),
            "X-TC-Version": self.version,
            "X-TC-Region": self.region,
        }
        return headers

    def api_post(self, action, params):
        # 获取签名请求头
        headers = self.get_sign_heades(action=action, params=params)
        url = "http://" + self.host + "/apiDispatch/v3?action=" + action
        r = requests.post(url=url, headers=headers, data=json.dumps(params))

        return r.text
