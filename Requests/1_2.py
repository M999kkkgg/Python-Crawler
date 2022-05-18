# -*- coding: UTF-8 -*-

from OutputPackage import *
import requests
import os

if __name__ == "__main__":
    Fm.Start_PG()
    # UA伪装
    UAHeaders = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    url = "https://www.sogou.com/web"
    # 处理url携带的参数封装到字典中
    kw = input("请输入要检索的关键词: ").replace(" ", "")
    param = {
        "query": kw
    }
    # 发出请求
    # params参数（字典）会自动在url后面添加参数
    # headers 附带get请求的头信息
    try:
        response = requests.get(url=url, params=param, headers=UAHeaders)
    except OSError as err:
        print(f"{err}: 请求失败")
        raise
    else:
        print("请求成功")
    # 获取响应数据
    page_text = response.text
    # 指定保存路径
    path = os.getcwd() + '\\Data'
    path = os.path.join(path, 'sogou_' + kw + '.html')
    with open(path, 'w', encoding='utf-8') as fp:
        fp.write(page_text)
    print(f"{kw}.html 已经保存到路径 {os.path.abspath(path)}")
    Fm.End_PG()
