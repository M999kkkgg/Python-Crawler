# -*- coding: utf-8 -*-
# written by msf

import requests
import os
import pandas as pd
from lxml import etree

# 城市字典
CityDict = {
    '南京': 'nj', '北京': 'bj',
    '上海': 'sh', '广州': 'gz',
    '深圳': 'sz', '成都': 'cd',
    '杭州': 'hz', '天津': 'tj',
    '武汉': 'wh', '重庆': 'cq'
}


# 获取房源信息的类
class GetWuBa:
    # 初始属性值
    Headers = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Cookie': "f=n; f=n; f=n; isp=true; id58=c5/nfF6O+9mNY3MpA/bhAg==; 58tj_uuid=f6e25717-7be5-402d-9c08-8857a92cb225; bj58_new_uv=1; bj58_id58s=\"eG11ZkVrSGd5dm1mOTM0NA==\"; wmda_uuid=d093f2c5824e9b6039bafa97b00cfe26; wmda_new_uuid=1; ppStore_fingerprint=6B00F5699C36F935F1BC2346682819C0DBADC5BDD27410DE%EF%BC%BF1594989281397; xxzl_deviceid=0saIBvZo44aNsTZJ1cVqZrSCSRA9pPZI%2F4RhhDbwABUzvoWka1vCy7Z26n0PB5cZ; als=0; new_uv=2; utm_source=; spm=; init_refer=; wmda_session_id_11187958619315=1600221281029-ab3b39a5-4375-2aa0; new_session=0; wmda_session_id_2385390625025=1600221417335-d6bab1df-dd74-573e; wmda_visited_projects=%3B1731918550401%3B11187958619315%3B2385390625025; f=n; city=nj; 58home=nj; commontopbar_new_city_info=172%7C%E5%8D%97%E4%BA%AC%7Cnj; commontopbar_ipcity=nj%7C%E5%8D%97%E4%BA%AC%7C0; xxzl_cid=199f19870cc04f85b98d4394bdb49c15; xzuid=fd937a61-2451-47bd-a4b8-87e35b7ff3b4; 58_ctid=172; is_58_pc=1; commontopbar_new_city_info=16%7C%E5%8D%97%E4%BA%AC%7Cnj; ctid=16; aQQ_ajkguid=2E661FB1-5A71-C14F-1AD8-SX0916095810; sessid=093CC0DA-1A71-DA15-FB94-SX0916095810; wmda_session_id_8788302075828=1600221492031-15ea4887-b495-7dae; wmda_visited_projects=%3B1731918550401%3B11187958619315%3B2385390625025%3B8788302075828; __xsptplusUT_8=1; __xsptplus8=8.1.1600221492.1600221642.13%234%7C%7C%7C%7C%7C%23%23bs72reAHEs2qXlWQ7vOllZec4raEEKkZ%23",
        'Content-Type': "text/html; charset=utf-8"
    }
    Params = {}
    HouseData = {
        'index': [],
        'Name': [],
        'Address': [],
        'Size': [],
        'Prize': []
    }
    Columns = {'index': '序号', 'Name': '房名', 'Address': '位置', 'Size': '大小', 'Prize': '市场价'}
    Response = None
    DataEtree = None

    # 方法
    def __init__(self, page: str, city: str):
        self.Page = page
        self.City = city
        self.CityID = CityDict[city]
        # 更新url
        self.Url = f"https://{self.CityID}.58.com/xinfang/loupan/all/p{self.Page}/"
        # 设置文件存储路径与文件名
        path = os.getcwd()
        path = os.path.join(path, 'Data')
        path = os.path.join(path, '3_五八同城新房信息')
        path = os.path.join(path, city)
        self.Path = path
        self.FileName = f'{self.City}_{int(self.Page):03d}.csv'

    # 初始化文件夹以及文件
    def InitDir(self):
        if not os.path.exists(self.Path):
            os.makedirs(self.Path)
        filepath = os.path.join(self.Path, self.FileName)
        if os.path.isfile(filepath):
            os.remove(filepath)
        else:
            pass
        fp = open(filepath, 'w', encoding='utf-8')
        fp.write("")
        fp.close()
        print("初始化文件夹完成...")

    # 连接
    def LinkURL(self):
        self.Response = requests.get(url=self.Url, params=self.Params, headers=self.Headers)
        print("Get状态码:", self.Response.status_code)
        self.Response = self.Response.text

    # 数据解析
    def GetData(self):
        self.DataEtree = etree.HTML(self.Response)
        # 获取当页显示的房子数目
        AllHouse = self.DataEtree.xpath('//body/div[@id="container"]//div[@class="key-list imglazyload"]/div')
        num = len(AllHouse)
        self.HouseData['index'] = list(range(num))
        # print(len(self.HouseData['index']))
        # 获取每栋房子的信息
        HouseName = self.DataEtree.xpath('//span[@class="items-name"]/text()')
        # print(len(HouseName))
        self.HouseData['Name'] = HouseName
        HouseMap = self.DataEtree.xpath('//span[@class="list-map"]/text()')
        HouseMap = [x.replace("\xa0", " ") for x in HouseMap]   # 去除\xa0字符
        # print(len(HouseMap))
        self.HouseData['Address'] = HouseMap
        HouseInfo = self.DataEtree.xpath('//span[@class="building-area"]/text()')
        HouseInfo = [x.replace("建筑面积：", "") for x in HouseInfo]
        # print(len(HouseInfo))
        self.HouseData['Size'] = HouseInfo
        # 获取房子价格
        # HousePrize = self.DataEtree.xpath('//a[@class="favor-pos"]/p//text()')
        # 处理爬到的字符串（去除无用信息）
        # HousePrize = [x.replace("售价待定", "") for x in HousePrize]
        # HousePrize = [x.replace(" ", "") for x in HousePrize]
        # HousePrize = [x.replace("\n", "") for x in HousePrize]
        # for i in range(HousePrize.count("")):
            # HousePrize.remove("")
        # HousePrize = [HousePrize[i] + HousePrize[i+1] + HousePrize[i+2] for i in range(len(HousePrize)) if i % 3 == 0]
        # print(len(HousePrize))
        for i in range(num):
            self.HouseData['Prize'].append("")
        # self.HouseData['Prize'] = HousePrize
        print("数据解析完成")

    # 本地存储
    def SaveCSV(self):
        PDdata = pd.DataFrame(data=self.HouseData)
        PDdata = PDdata.rename(columns=self.Columns)
        fp_csv = open(os.path.join(self.Path, self.FileName), 'w', encoding='utf-8', newline="")
        PDdata.to_csv(fp_csv, index=False)
        fp_csv.close()
        print("文件已经存储到如下路径中")
        print(os.path.join(self.Path, self.FileName))
