# -*- coding: utf-8 -*-
import requests

url = 'http://192.168.77.2/apiDispatch/v3?action=CreateApiGroup'
data = {'AuthType': "none",
        'Description': "",
        'GatewayInstanceId': "gw-ins-xh5y9j59",
        'GroupContext': "/test3",
        'GroupName': "test3",
        'GroupType': "ms",
        'Version': "2018-03-26"}
headers = {'Accept': '*/*',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language': 'zh-CN,zh;q=0.9',
           'Connection': 'keep-alive',
           'Content-Length': '226',
           'Content-Type': 'application/json',
           'Cookie': 'accessToken=7bb59095be397f5f009207c0ee6ec101; JSESSIONID=C934F195600551A31973210521687F5C',
           'Host': '192.168.77.2',
           'Origin': 'http://192.168.77.2',
           'Referer': 'http://192.168.77.2/tsf/gateway-instance-detail?rid=1&id=gw-ins-xh5y9j59&tab=apiGroup'
                      '&microserviceId=ms-4y49wq6a',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/99.0.4844.51 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest'}
re = requests.post(url=url, data=data, headers=headers)
print(re.text)
