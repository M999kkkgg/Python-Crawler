# -*- coding: utf-8 -*-
# written by msf

import requests
import os
from lxml import etree


class GetCity:
    # 属性
    Params = {}
    Headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Cookie': "UM_distinctid=174970e898d0-051b1d8bf3dd6b-36664c08-1fa400-174970e898f5ef; CNZZDATA5808503=cnzz_eid%3D523662296-1600259623-%26ntime%3D1600259623Host: www.aqistudy.cn",
        'Content-Type': "text/html; charset=UTF-8"
    }
    Response = None
    ResponseText = None
    CityNameList = {}
    EtreeData = None

    # 方法
    def __init__(self):
        self.Url = "https://www.aqistudy.cn/historydata/"
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, '5_全国城市名称爬取')
        self.Path = path
        self.FileName = 'CityName_CN.txt'
        self.FilePath = os.path.join(self.Path, self.FileName)

    def InitDir(self):
        if not os.path.exists(self.Path):
            os.makedirs(self.Path)
        if os.path.isfile(self.FilePath):
            os.remove(self.FilePath)
        else:
            fp = open(self.FilePath, 'w', encoding='utf-8')
            fp.write("")
            fp.close()

    def LinkURL(self):
        self.Response = requests.get(url=self.Url, params=self.Params, headers=self.Headers)
        print("编码格式:", self.Response.encoding)
        print("Get请求状态码", self.Response.status_code)

    def ReadData(self):
        self.ResponseText = self.Response.text
        self.EtreeData = etree.HTML(self.ResponseText)
        ul_list = self.EtreeData.xpath('//div[@class="all"]/div[@class="bottom"]/ul')
        # print(len(ul_list), '\n', ul_list)
        for ul in ul_list:
            # 获取城市分类标签（即首字母）
            label = ul.xpath('./div[1]/b/text()')[0].replace(".", "")
            # print(label, end="")
            li_list = ul.xpath('./div[2]/li')
            # print(len(li_list), '\n', li_list)
            # 获取该标签下的所有城市名
            info = []
            for li in li_list:
                temp = li.xpath('./a/text()')[0]
                info.append(temp)
                del temp
            # print(info)
            # 以标签为key，城市名列表为value做为一个字典元素存储到CityNameList中
            self.CityNameList[label] = info
            del label, info
        # print(self.CityNameList)
        print("数据解析...")

    def SaveTXT(self):
        path = self.FilePath
        label_list = list(self.CityNameList.keys())
        # 打开文件
        fp = open(path, 'w', encoding='utf-8')
        fp.write("中国全部城市\n按照首字母分类\n")
        # 写入数据到txt中
        for i in range(len(label_list)):
            fp.write(f"\n{(i+1):02d}. {label_list[i]}\n")
            temp = ", "
            temp = temp.join(self.CityNameList[label_list[i]])  # 列表转字符串，并设置分隔符
            fp.write(f"{temp}\n")
            i += 1
        # 关闭文件
        fp.close()
        print(f"文件保存路径")
        print(self.FilePath)
