# -*- coding: utf-8 -*-
# written by msf

import time
import random
import requests
import os
from lxml import etree
# 线程池
from multiprocessing import Pool


class GetVideo:
    # 属性
    URL = "https://www.pearvideo.com/category_5"
    urls = []
    VideoName = []
    VideoURL = []
    VideoNum = 0
    Headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    Response = None
    ResponseText = None
    VideoResponseText = []
    VideoData = []

    # 方法
    def __init__(self):
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, 'PearVideo')
        self.TextFileName = '视频URL.txt'
        self.Path = path

    def InitDir(self):
        if not os.path.exists(self.Path):
            os.makedirs(self.Path)
        fp = open(os.path.join(self.Path, self.TextFileName), 'w', encoding='utf-8')
        fp.write("")
        fp.close()

    # 连接首页，并解析数据
    def Link_1(self):
        self.Response = requests.get(url=self.URL, headers=self.Headers)
        print(f"发出请求 {self.URL}")
        print("编码格式:", self.Response.encoding)
        print("Get请求状态码", self.Response.status_code)
        self.ResponseText = self.Response.text
        tree = etree.HTML(self.ResponseText)
        li_list = tree.xpath('//ul[@id="listvideoListUl"]/li')
        # print(li_list)
        # 获取每一个视频详情页链接和名称
        for li in li_list:
            temp_url = 'https://www.pearvideo.com/' + li.xpath('./div[@class="vervideo-bd"]/a/@href')[0]
            self.urls.append(temp_url)
            temp_name = li.xpath('./div/a/div[@class="vervideo-title"]/text()')[0].replace(" ", "") + '.mp4'
            self.VideoName.append(temp_name)
            del temp_url, temp_name
        # print(self.urls)
        # print(self.VideoName)
        self.VideoNum = len(self.urls)

    # 对每一个详情页url发出请求，并解析出视频地址
    def Link_2(self):
        for i in range(self.VideoNum):
            temp = requests.get(url=self.urls[i], headers=self.Headers)
            print(f"发出请求 {self.urls[i]}")
            print("编码格式:", temp.encoding)
            print("Get请求状态码", temp.status_code)
            self.VideoResponseText.append(temp.text)
            del temp
            # 数据解析解析出视频url
            tree = etree.HTML(self.VideoResponseText[i])
            temp = tree.xpath('//*[@id="JprismPlayer"]/video/src')
            '''
            当前网站已经参数加密
            '''
            del temp

