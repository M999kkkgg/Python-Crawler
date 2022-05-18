# -*- coding: utf-8 -*-
# written by msf

import requests
import os
from lxml import etree

# 图片种类列表
ClassDict = {
    '风景': '4kfengjing', '美女': '4kmeinv', '游戏': '4kyouxi',
    '动漫': '4kdongman', '影视': '4kyingshi', '明星': '4kmingxing',
    '汽车': '4kqiche', '动物': '4kdongwu', '人物': '4krenwu',
    '美食': '4kmeishi', '宗教': '4kzongjiao', '背景': '4kbeijing'
}


# 爬取图片类
class Get4k:
    # 属性
    Headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Cookie': "__cfduid=df76734a2f17c063406d91a0bab834f0e1600242191; Hm_lvt_526caf4e20c21f06a4e9209712d6a20e=1600242194; zkhanecookieclassrecord=%2C54%2C65%2C66%2C53%2C55%2C60%2C56%2C59%2C58%2C62%2C67%2C63%2C; Hm_lpvt_526caf4e20c21f06a4e9209712d6a20e=1600242961",
        'Content-Type': "text/html"
    }
    Params = {}
    Response = None
    ResponseText = None
    ImgSrcList = None
    ImgNameList = None
    EtreeData = None
    PageNum = None

    # 方法
    def __init__(self, page: str, cname: str):
        self.Page = page    # 该类实例化对象要爬取的页面
        self.CName = cname
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, '4_超级高清图片爬取')
        path = os.path.join(path, cname)
        self.Path = path    # 图片存储的文件夹
        if page != '1':
            self.Url = f"http://pic.netbian.com/{ClassDict[cname]}/index_{page}.html"
        else:
            self.Url = f"http://pic.netbian.com/{ClassDict[cname]}/index.html"

    # 初始化文件夹
    def InitDir(self):
        if not os.path.exists(self.Path):
            os.makedirs(self.Path)

    # 连接
    def LinkURL(self):
        self.Response = requests.get(url=self.Url, params=self.Params, headers=self.Headers)
        print('编码:', self.Response.encoding)   # ISO-8859-1
        # 设置响应数据的整体编码
        self.Response.encoding = 'gbk'
        print("Get请求状态码:", self.Response.status_code)

    # 数据解析
    def GetData(self):
        self.ResponseText = self.Response.text
        self.EtreeData = etree.HTML(self.ResponseText)
        temp = self.EtreeData.xpath('//body//div[@class="slist"]/ul//img/@src')
        self.ImgSrcList = temp
        temp = self.EtreeData.xpath('//body//div[@class="slist"]/ul//a/b/text()')
        # 通用处理中文乱码的解决方案
        # temp = temp.encode('ISO-8859-1').decode('gbk')
        temp = [x.replace(" ", "") for x in temp]   # 去除多余的空格
        # print(len(self.ImgSrcList), self.ImgSrcList)
        # print(len(temp), temp)
        self.ImgNameList = temp
        # 获取总共的页码
        temp = self.EtreeData.xpath('//div[@class="page"]/a/text()')
        # print(temp)
        self.PageNum = int(temp[-2])
        print("数据解析完成")

    # 保存本地文件
    def SaveJPG(self):
        ImgUrlList = ['http://pic.netbian.com' + x for x in self.ImgSrcList]
        headers_temp = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
            'Content-Type': "image/jpeg"
        }
        index = 1
        for url in ImgUrlList:
            response_temp = requests.get(url=url, params=self.Params, headers=headers_temp)
            response_temp = response_temp.content
            FileName = f"{int(self.Page):03d}_{index:02d}_{self.ImgNameList[index-1]}.jpg"
            fp = open(os.path.join(self.Path, FileName), 'wb')
            fp.write(response_temp)
            fp.close()
            del response_temp
            print(f"{FileName} 下载成功...")
            index += 1
        print(f"已经获得 {self.CName} 类中第 {self.Page} 页的全部图片")
        print("它们被保存在该目录下")
        print(self.Path)

    # 返回总共的页码
    def ReturnPageNum(self):
        return self.PageNum
