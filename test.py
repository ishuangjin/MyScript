#!/usr/bin/env python3
# encoding:utf-8
'''
@Author: ishuangjin
@WebSite: blog.ishuangjin.cn
@QQ: 1525053461
@Mail: ishuangjin@foxmail.com
@Date: 2022-10-04 00:23:25
@LastEditTime: 2022-10-10 16:30:10
@FilePath: \\Github\\MyScript\\test.py
@Copyright (c) 2022 by ishuangjin, All Rights Reserved.
@Description: 
'''
import sys
from hashlib import sha1
import string
import random
import hmac
import base64
import uuid

seed = [
    '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
    'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
    'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'
]
si = "ZsJjsA8FSdC4Qr7WA02xyw=="
sk = "t/EtD53nN+Oa5OuxDhAjvQ=="
nonce = "".join(random.sample(seed, 22)).replace(" ", "")
print(nonce)
signstr = nonce + si + sk
print(signstr)
local_sign_seed = hmac.new(sk.encode('utf-8'), signstr.encode('utf-8'), sha1).digest()
print(local_sign_seed)
sign = base64.b64encode(local_sign_seed).decode('ascii')
print(sign)
print("")
print("generate local sign: " + sign)
print("")
print("=== http request headers as followed === ")
print("x-mg-nonce: " + nonce)
print("x-mg-secretid: " + si)
print("x-mg-traceid: " + str(uuid.uuid1()))
print("x-mg-alg: 1")
print("x-mg-sign: " + sign)