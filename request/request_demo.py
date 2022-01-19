# -*- coding:utf-8 -*-
'''
author:zhangyu
date:2022/1/14
description：请求接口
'''

import requests
import json

data = {
    "id": "HYPERPULSE_default_001",
    "msgType": "DATA_SERVICE_MSG",
    "request": {
        "header": {
            "requestId": "001"
        },
        "body": {
            "instruction": "RMS_GET_BOX_FETCH_LANE",
            "skuCodes": ["ATBASE_b_goods_06", "ATBASE_b_goods_08"]
        }
    }
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36"
    , "Content-Type": "application/json"
}
url = "http://172.18.1.22:8557/hyperpulse/api/hyper"

response = requests.post(url=url, data=json.dumps(data), headers=headers)
print(response.text)
