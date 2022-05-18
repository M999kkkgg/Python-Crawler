# -*- coding: utf-8 -*-
# written by msf

import requests
import os
from lxml import etree
import time
from PIL import Image
from TTShiTu import *


class LogGSW:
    # 属性
    LogUrl = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
    PicUrl = None

    Headers = {
        'User-Agent': "",
        'Content-Type': "text/html; charset=utf-8",
        'Cookie': "login=flase; ASP.NET_SessionId=1gsquot3bzeteyg0ryitkhpf; Hm_lvt_9007fab6814e892d3020a64454da5a55=1600333535; codeyzgswso=348f424f85715974; login=flase; gswZhanghao=1183103017%40qq.com; wsEmail=1183103017%40qq.com; wxopenid=defoaltid; Hm_lpvt_9007fab6814e892d3020a64454da5a55=1600333898"
    }
    LogPage = None
    LogPageText = None
    Etree = None
    Path = None
    Result = None   # 存储识别的验证码
    FileName = None

    # 方法
    def __init__(self):
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, "古诗文网登录验证码")
        self.Path = path

    def InitDir(self):
        if not os.path.exists(self.Path):
            os.makedirs(self.Path)

    def LinkLog_1(self):
        self.LogPage = requests.get(url=self.LogUrl, headers=self.Headers)
        print("访问登录界面地址")
        print("编码格式:", self.LogPage.encoding)
        print("Get请求状态码", self.LogPage.status_code)
        self.LogPageText = self.LogPage.text

    def GetJPG(self):
        self.Etree = etree.HTML(self.LogPageText)
        self.PicUrl = self.Etree.xpath('//*[@id="imgCode"]/@src')[0]
        self.PicUrl = 'https://so.gushiwen.cn' + self.PicUrl
        # print(self.PicUrl)
        # 保存图片
        header = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            'Content-Type': "image/Gif"
        }
        temp = requests.get(url=self.PicUrl, headers=header)
        print("验证码图片地址")
        print("编码格式:", temp.encoding)
        print("Get请求状态码", temp.status_code)
        temp = temp.content
        localtime = time.asctime(time.localtime(time.time()))
        localtime = localtime[-13:].replace(" ", "_")
        localtime = localtime.replace(":", "_")
        temp_2 = localtime[-4:]
        localtime = temp_2 + '_' + localtime[0:8]
        del temp_2
        filename = localtime + '.jpg'
        self.FileName = filename
        fp = open(os.path.join(self.Path, filename), 'wb')
        fp.write(temp)
        fp.close()
        print(f"{filename} 已被保存...")

    def Distinguish(self):
        Uname = 'msf1189'
        Pwd = 'msf97347110'
        Codetype = '3'
        Img = Image.open(os.path.join(self.Path, self.FileName))
        self.Result = stAPI.base64_api(uname=Uname, pwd=Pwd, codetype=Codetype, img=Img)
        print(f"验证码识别: {self.Result}")
