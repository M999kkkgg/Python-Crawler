# -*- coding: utf-8 -*-
# written by msf

import requests
import os
import pandas as pd
from bs4 import BeautifulSoup


def InitDir():
    path = os.getcwd()
    path = os.path.join(path, 'Data')
    path = os.path.join(path, '2_三国演义小说爬取')
    if not os.path.exists(path):
        os.makedirs(path)
    filename = '三国演义.txt'
    filepath = os.path.join(path, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)
    fp = open(filepath, 'w', encoding='utf-8')
    fp.write("")
    fp.close()
    filename = '三国演义URL.csv'
    filepath = os.path.join(path, filename)
    if os.path.isfile(filepath):
        os.remove(filepath)
    fp = open(filepath, 'w', encoding='utf-8')
    fp.write("")


class GetSanguo:
    # 各个属性值
    Url = "https://www.shicimingju.com/book/sanguoyanyi.html"
    UrlTemp: str = None
    Headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Cookie': "Hm_lvt_6181c6e4531be00fa696eb631fbd2a4b=1600173902; Hm_lpvt_6181c6e4531be00fa696eb631fbd2a4b=1600173902",
        'Content-Type': "text/html; charset=UTF-8"
    }
    HeadersTemp = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Cookie': "Hm_lvt_6181c6e4531be00fa696eb631fbd2a4b=1600173902; Hm_lpvt_6181c6e4531be00fa696eb631fbd2a4b=1600174899",
        'Content-Type': "text/html; charset=UTF-8"
    }
    Params = {}
    DataText = ""
    DataSoup = None
    DataTemp = ""
    TempSoup = None
    ChapterURL = []

    # 方法
    def __init__(self):
        pass

    # 连接
    def LinkGet(self):
        self.DataText = requests.get(url=self.Url, params=self.Params, headers=self.Headers).text

    # 数据的初步解析
    def ReadData(self):
        # 设置保存路径（即之前创建好的txt文件中）
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, '2_三国演义小说爬取')
        path_csv = path
        path = os.path.join(path, '三国演义.txt')
        self.DataSoup = BeautifulSoup(self.DataText, 'lxml')
        fp = open(path, 'a', encoding='utf-8')
        path_csv = os.path.join(path_csv, '三国演义URL.csv')
        fp_csv = open(path_csv, 'a', encoding="utf-8", newline="")
        # 读取书名
        temp = self.DataSoup.select('h1')
        fp.write(temp[0].string + '\n')
        # 读取年代与作者
        temp = self.DataSoup.select('p')
        fp.write(temp[0].string + '\n')
        fp.write(temp[1].string + '\n')
        # 读取书本简介
        temp = self.DataSoup.select('p.des')
        fp.write('简介' + temp[0].string + '\n')
        # 读取每一个章节的url到self.ChapterURL中
        temp = self.DataSoup.select('.book-mulu > ul > li')
        fp.write("\n目录\n")
        Columns = ['序号', '章节', 'URL']
        index = 0
        for x in temp:
            index += 1
            # 将目录名字写入到文件中
            fp.write(x.a.string + '\n')
            # 读取属性href
            self.ChapterURL.append('https://www.shicimingju.com' + x.a['href'])
            # 保存url到csv文件中
            PD_data = pd.DataFrame({
                '序号': index,
                '章节': x.a.string,
                'URL': 'https://www.shicimingju.com' + x.a['href']
            }, columns=Columns, index=[0])
            if index == 1:
                PD_data.to_csv(fp_csv, header=True, index=False)
            else:
                PD_data.to_csv(fp_csv, header=False, index=False)
        fp_csv.close()
        fp.close()  # 关闭文件

    # 读取每一个章节页面
    def ReadChapter(self):
        # 设置保存路径（即之前创建好的txt文件中）
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, '2_三国演义小说爬取')
        path = os.path.join(path, '三国演义.txt')
        fp = open(path, 'a', encoding='utf-8')
        fp.write("\n正文\n")
        for i in range(len(self.ChapterURL)):
            self.DataTemp = requests.get(url=self.ChapterURL[i], params=self.Params, headers=self.HeadersTemp).text
            self.TempSoup = BeautifulSoup(self.DataTemp, 'lxml')
            temp = self.TempSoup.select('h1')
            fp.write('\n' + temp[0].string + '\n')
            temp = self.TempSoup.select('.chapter_content > p')
            for x in temp:
                fp.write(x.string.replace(" ", "", 4) + '\n')
        fp.close()
