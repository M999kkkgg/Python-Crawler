# -*- coding: utf-8 -*-
# written by msf

import requests
import os
import re
import shutil
import pandas as pd


# 定义函数初始化目录
def InitDir(page: int):
    path = os.getcwd()
    path = os.path.join(path, 'Data')
    if not os.path.exists(path):
        os.makedirs(path)
    path = os.path.join(path, '1_糗事百科热图爬取')
    if not os.path.exists(path):
        os.makedirs(path)
    dir_list = os.listdir(path)
    # 重置文件夹 (仅当扫描第一页时重置)./Data/1_糗事百科热图爬取
    if page == 1:
        for x in dir_list:
            temp = path
            temp = os.path.join(temp, x)
            if os.path.isdir(temp):
                shutil.rmtree(temp)
            elif os.path.isfile(temp):
                os.remove(temp)
    filename = f'图片地址目录_{page}.csv'
    with open(os.path.join(path, filename), 'w', encoding="utf-8") as fp:
        fp.write("")
    path = os.path.join(path, f'图片_Page{page}')
    os.makedirs(path)


class GetJPG:
    # 属性值
    Url = 'https://www.qiushibaike.com/imgrank/'
    Headers_1 = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Cookie': "_xsrf=2|415ce99f|f2cd40e80c7a673e52f3948cad546f05|1600158951; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1600158953; _ga=GA1.2.672281190.1600158953; _gid=GA1.2.887522345.1600158953; gr_user_id=84521454-de00-45b5-a7f3-2a62c595c0df; ff2672c245bd193c6261e9ab2cd35865_gr_session_id=935c56fe-b04a-46fa-902b-0aeb9dab3c63; _qqq_uuid_=\"2|1:0|10:1600158952|10:_qqq_uuid_|56:YzA5MDliMTdhYTVkNzA2YjRiNWY1NDMzMTgyMTYzMWMxNTQ3MGZhOA==|91e9da5651d3fbf246b03915858aa9897aa54031828b03f5c23d5de517217ca4\"; ff2672c245bd193c6261e9ab2cd35865_gr_session_id_935c56fe-b04a-46fa-902b-0aeb9dab3c63=true; grwng_uid=049c3942-cfc7-4a92-b5ab-e894060a9f33; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1600159369; _gat=1",
        'Content-Type': "text/html; charset=UTF-8"
    }
    Headers_2 = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Cookie': "_ga=GA1.2.672281190.1600158953; _gid=GA1.2.887522345.1600158953; gr_user_id=84521454-de00-45b5-a7f3-2a62c595c0df; _qqq_uuid_=\"2|1:0|10:1600158952|10:_qqq_uuid_|56:YzA5MDliMTdhYTVkNzA2YjRiNWY1NDMzMTgyMTYzMWMxNTQ3MGZhOA==|91e9da5651d3fbf246b03915858aa9897aa54031828b03f5c23d5de517217ca4\"; grwng_uid=049c3942-cfc7-4a92-b5ab-e894060a9f33; __cur_art_index=3900; Hm_lvt_2670efbdd59c7e3ed3749b458cafaa37=1600158953,1600166885; ff2672c245bd193c6261e9ab2cd35865_gr_session_id=450fe350-8bbe-4a5f-91c5-9188cdf8178c; ff2672c245bd193c6261e9ab2cd35865_gr_session_id_450fe350-8bbe-4a5f-91c5-9188cdf8178c=true; Hm_lpvt_2670efbdd59c7e3ed3749b458cafaa37=1600167300",
    }
    Params = {}
    Response = None
    ImgSrc_List = None
    ImgB_Temp = None
    Page = 1

    # 初始化函数
    def __init__(self, x):
        self.Page = x   # 设置访问的页面

    # 发出请求
    def SendGet(self):
        self.Response = requests.get(url=self.Url + f'page/{self.Page}/', params=self.Params, headers=self.Headers_1)
        # print("1-发出请求")

    # 获取响应数据
    def GetData(self):
        self.Response = self.Response.text
        # print("2-已经获得相应数据")

    # 数据解析
    def DataAnalysis(self):
        ex = '<div class="thumb">.*?href=.*?<img src=\"(.*?)\" alt=.*?</div>'
        self.ImgSrc_List = re.findall(ex, self.Response, re.S)
        # print("3-正在进行数据解析")

    # 本地化存储csv
    def SaveCSV(self):
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, '1_糗事百科热图爬取')
        path = os.path.join(path, f'图片地址目录_{self.Page}.csv')
        Columns = ['图片序号', '图片地址']
        i = 0
        for x in self.ImgSrc_List:
            data = pd.DataFrame({
                '图片序号': str(i),
                '图片地址': x
            }, columns=Columns, index=[0])
            fp_csv = open(path, 'a', encoding='utf-8', newline="")
            if i == 0:
                data.to_csv(fp_csv, header=True, index=False)
            else:
                data.to_csv(fp_csv, header=False, index=False)
            i += 1
        # print("4-全部图片的地址数据已经存储到以下路径")
        # print(path)

    # 本地化存储JPG
    def SaveJPG(self):
        # 设置存储路径
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, '1_糗事百科热图爬取')
        path = os.path.join(path, f'图片_Page{self.Page}')
        # 循环访问存储csv中的url
        index = 0
        for x in self.ImgSrc_List:
            self.ImgB_Temp = requests.get(url='http:' + x, params=self.Params, headers=self.Headers_2)
            self.ImgB_Temp = self.ImgB_Temp.content
            filename = f"Picture_{index:04d}.jpg"
            # 向路径写入jpg文件
            with open(os.path.join(path, filename), 'wb') as fp:
                fp.write(self.ImgB_Temp)
            index += 1
        # print("4-全部图片(jpg)已经存储到以下文件夹中")
        # print(path)
        print(f"Page_{self.Page}上的图片已经全部保存")
