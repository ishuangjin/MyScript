#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-10-10 16:04:47
@LastEditTime: 2022-10-10 16:42:05
@FilePath: \\Github\\MyScript\\TSF接口测试\\gen_sign.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description:  微服务网关密钥对鉴权
使用 SHA1 算法生成签名，入参为 SecretId 和 SecetKey
参考：https://cloud.tencent.com/document/product/649/41238
使用时执行：python gen_sign.py {secretId} {secretKey}
'''

import sys
from hashlib import sha1
import random
import hmac
import base64
import uuid


def fun(secretId, secretKey):
    seed = [
        '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
        'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L',
        'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
    ]

    nonce = "".join(random.sample(seed, 22)).replace(" ", "")
    signstr = nonce + secretId + secretKey
    local_sign_seed = hmac.new(secretKey.encode('utf-8'), signstr.encode('utf-8'), sha1).digest()
    sign = base64.b64encode(local_sign_seed).decode('ascii')
    print("")
    print("generate local sign: " + sign)
    print("")
    print("=== http request headers as followed === ")
    print("x-mg-nonce: " + nonce)
    print("x-mg-secretid: " + secretId)
    print("x-mg-traceid: " + str(uuid.uuid1()))
    print("x-mg-alg: 1")
    print("x-mg-sign: " + sign)


if __name__ == "__main__":
    secretId = "ZsJjsA8FSdC4Qr7WA02xyw=="
    secretKey = "t/EtD53nN+Oa5OuxDhAjvQ=="
    if len(sys.argv) == 3:
        secretId = sys.argv[1]
        secretKey = sys.argv[2]
    fun(secretId, secretKey)

# end main