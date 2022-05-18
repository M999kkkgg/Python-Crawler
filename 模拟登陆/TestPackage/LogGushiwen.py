# -*- coding: utf-8 -*-
# written by msf

import requests
import os
from lxml import etree
import time
from PIL import Image
from TTShiTu import *

session = requests.Session()
# 原因是验证码图片使用的是 urlretrive 进行的请求,该次请求的时候,服务器端会返回cookie.
# 所以对验证码图片的请求必须使用session进行,将cookie存储在session中,然后使用session继续进行登录请求即可完成.
# session对象和requests作用几乎一样,都可以进行请求的发送,并且请求发送的方式也是一致的,
# session进行请求的发送,如果会产生cookie的话,则cookie会自动被存储到session对象中


class LogGSW:
    # 属性
    LogUrl = "https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
    PicUrl = None
    UserUrl = 'https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx%3ftype%3da'
    UP_URL = "https://so.gushiwen.cn/user/collect.aspx?type=a"

    Headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36"
    }
    UHeaders = {
        'Cookie': "login=flase; ASP.NET_SessionId=1gsquot3bzeteyg0ryitkhpf; Hm_lvt_9007fab6814e892d3020a64454da5a55=1600333535; wsEmail=1183103017%40qq.com; idsMingju2017=%2c162%2c; idsShiwen2017=%2c7722%2c49386%2c71137%2c71138%2c; idsAuthor2017=%2c247%2c183%2c665%2c474%2c; Hm_lpvt_9007fab6814e892d3020a64454da5a55=1600345067; codeyzgswso=1a33ee32dd117134; gsw2017user=1267681%7c31A350C0F42403B695BB7816A2EEE265; login=flase; gswZhanghao=1183103017%40qq.com; gswEmail=1183103017%40qq.com",
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    }
    ViewState = ""
    ViewStateGenerator = ""
    LogData = {
        "__VIEWSTATE": "",      # 需要爬取
        "__VIEWSTATEGENERATOR": "",     # 需要爬取
        "from": "http://so.gushiwen.org/user/collect.aspx",
        "email": "1183103017@qq.com",
        "pwd": "msf97347110lol",
        "code": "",     # 验证码结果
        "denglu": "登录"
    }
    LogPage = None
    LogPageText = None
    Etree = None
    Result = None   # 存储识别的验证码
    FileName = None
    UserPage = None
    UserPageText = None
    UserEtree = None

    # 方法
    def __init__(self):
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, "古诗文网登录验证码")
        self.Path = path
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, "古诗文网用户信息")
        self.InfoPath = path

    def InitDir(self):
        if not os.path.exists(self.Path):
            os.makedirs(self.Path)
        if not os.path.exists(self.InfoPath):
            os.makedirs(self.InfoPath)
        DirList = ['我的诗文', '我的名句', '我的作者', '我的古籍']
        for x in DirList:
            temp = os.path.join(self.InfoPath, x)
            if not os.path.exists(temp):
                os.makedirs(temp)
            else:
                continue
        fp = open(os.path.join(self.InfoPath, '用户信息.txt'), 'w', encoding='utf-8')
        fp.write(f"用户名: {self.LogData['email']}")
        fp.close()

    def LinkLog_1(self):
        self.LogPage = session.get(url=self.LogUrl, headers=self.Headers)
        print("---访问登录界面地址---")
        print("编码格式:", self.LogPage.encoding)
        print("Get请求状态码", self.LogPage.status_code)
        self.LogPageText = self.LogPage.text

    def GetJPG(self):
        self.Etree = etree.HTML(self.LogPageText)
        self.PicUrl = self.Etree.xpath('//*[@id="imgCode"]/@src')[0]
        self.PicUrl = 'https://so.gushiwen.cn' + self.PicUrl
        self.ViewState = self.Etree.xpath('//*[@id="__VIEWSTATE"]/@value')[0]
        self.ViewStateGenerator = self.Etree.xpath('//*[@id="__VIEWSTATEGENERATOR"]/@value')[0]
        # print(self.PicUrl)
        # 保存图片
        temp = session.get(url=self.PicUrl, headers=self.Headers)
        print("---验证码图片地址---")
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
        print("---获取登录页面信息---")
        print(f"{filename} 已被保存...")
        print(f"ViewState: {self.ViewState}")
        print(f"ViewStateGenerator: {self.ViewStateGenerator}")

    def Distinguish(self):
        Uname = 'msf1189'
        Pwd = 'msf97347110'
        Codetype = '3'
        Img = Image.open(os.path.join(self.Path, self.FileName))
        self.Result = stAPI.base64_api(uname=Uname, pwd=Pwd, codetype=Codetype, img=Img)
        print(f"验证码识别: {self.Result}")

    def LinkLog_2(self):
        self.LogData['__VIEWSTATE'] = self.ViewState
        self.LogData['__VIEWSTATEGENERATOR'] = self.ViewStateGenerator
        self.UserPage = session.post(url=self.UserUrl, data=self.LogData, headers=self.UHeaders)
        print("---进行用户登录请求---")
        print("编码格式:", self.UserPage.encoding)
        print("Post请求状态码", self.UserPage.status_code)
        self.UserPageText = self.UserPage.text
        self.UserPage = session.post(url=self.UP_URL, headers=self.UHeaders)
        self.UserPage = session.post(url=self.UP_URL, headers=self.UHeaders)
        self.UserPageText = self.UserPage.text

    def GetUserData(self):
        # 保存HTML文件
        fp = open(os.path.join(self.InfoPath, '用户界面.html'), 'w', encoding='utf-8')
        fp.write(self.UserPageText)
        fp.close()
        # 根据保存的文件进行数据抓取
        # ...
        # 待实现
        # 2020.9.17
