# -*- coding: UTF-8 -*-

from OutputPackage import *
import requests
import os
import json

if __name__ == "__main__":
    Fm.Start_PG()
    # UA伪装
    UAHeaders = {
       'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    kw = input("请输入要翻译的内容（中文 -> 英文）：")
    post_data = {
        "kw": kw
    }
    post_url = "https://fanyi.baidu.com/sug"
    try:
        response = requests.post(url=post_url, data=post_data, headers=UAHeaders)
    except OSError as err:
        print(f"{OSError}: 请求失败")
        raise
    else:
        print("请求成功")
    # json返回一个对象，要确认响应数据为json类型
    dict_data = response.json()
    # 持久化存储
    path = os.getcwd() + f'\\Data'
    fp = open(path + f'\\zh_en_{kw}.json', 'w', encoding='utf-8')
    json.dump(dict_data, fp=fp, ensure_ascii=False)     # 中文不用ascii码
    Fm.End_PG()
