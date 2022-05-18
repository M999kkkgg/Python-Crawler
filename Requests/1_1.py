# -*- coding: UTF-8 -*-

from OutputPackage import *
import requests

if __name__ == "__main__":
    Fm.Start_PG()
    # 指定url
    url = "https://www.sogou.com"
    # 发起请求,get 方法返回一个响应对象
    try:
        response = requests.get(url=url)
    except OSError as rqErr:
        print(f"{rqErr}: Requests请求失败")
        raise
    else:
        # 获取响应数据，text返回的是字符串形式的响应数据
        page_text = response.text
        print(f"The data of sogou is as follows:\n{page_text}")
    # 持久化存储
    with open('Data/sogou.html', 'w', encoding='utf-8') as fp:
        fp.write(page_text)

    Fm.End_PG()
