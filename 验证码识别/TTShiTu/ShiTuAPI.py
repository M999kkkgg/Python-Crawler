# -*- coding: utf-8 -*-
# written by msf

import json
import requests
import base64
from io import BytesIO
from PIL import Image
from sys import version_info


# 识别图片验证码
def base64_api(uname: str, pwd: str,  img, codetype: str):
    img = img.convert('RGB')
    buffered = BytesIO()
    img.save(buffered, format="JPEG")
    if version_info.major >= 3:
        b64 = str(base64.b64encode(buffered.getvalue()), encoding='utf-8')
    else:
        b64 = str(base64.b64encode(buffered.getvalue()))
    data = {
        "username": uname,
        "password": pwd,
        "image": b64,
        'typeid': codetype
    }
    result = json.loads(requests.post("http://api.ttshitu.com/base64", json=data).text)
    if result['success']:
        return result["data"]["result"]
    else:
        return result["message"]
    return ""


# 查询并显示账户信息
def GetUInfo(uname: str, pwd: str):
    URL = f"http://api.ttshitu.com/queryAccountInfo.json?username={uname}&password={pwd}"
    response = requests.get(url=URL).text
    result = json.loads(response)
    print(f"┌───────────────────────────┐")
    print(f"│UserName: {uname:17s}│")
    if result['success']:
        print(f"│Status: {result['message']:19s}│")
        print(f"│Balance: {result['data']['balance']:18s}│")
        print(f"│Consumption: {result['data']['consumed']:14s}│")
        print(f"│SuccessNum: {result['data']['successNum']:15s}│")
        print(f"│FailNUm: {result['data']['failNum']:18s}│")
    else:
        pass
    print(f"└───────────────────────────┙")


# 返回账户余额
def GetBalance(uname: str, pwd: str):
    URL = f"http://api.ttshitu.com/queryAccountInfo.json?username={uname}&password={pwd}"
    response = requests.get(url=URL).text
    result = json.loads(response)
    if result['success']:
        return result['data']['balance']
    else:
        return "连接失败"
