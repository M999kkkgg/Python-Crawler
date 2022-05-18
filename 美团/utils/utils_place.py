import os.path
import requests
import json
import openpyxl
import random
import fake_useragent
from utils.util import download_img
import time
from tqdm import tqdm

"""
https://i.meituan.com/lvyou/volga/api/iservice/trip/poi/select/city/55?
limit=40
offset=0
cityId=55
sort=smart
cateId=195
selectedCityId=55
fromCityId=55
uuid=5F859A86563CA88128213ED0AB205059B3A54688C77E8AF5D96FD21E389F18A3
"""


class Place:
    def __init__(self):
        self.data = {
            'limit': 100,
            'offset': 0,
            'cityId': 1,
            'sort': 'smart',
            'cateId': 195,
            'selectedCityId': 1,
            'fromCityId': 1,
            'uuid': '5F859A86563CA88128213ED0AB205059B3A54688C77E8AF5D96FD21E389F18A3'
        }
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Host': 'i.meituan.com',
            'Cookie': 'iuuid=5F859A86563CA88128213ED0AB205059B3A54688C77E8AF5D96FD21E389F18A3; _lxsdk_cuid=17f1efb7725c8-09b85c6ec9201b-a3e3164-1bcab9-17f1efb772562; _lxsdk=5F859A86563CA88128213ED0AB205059B3A54688C77E8AF5D96FD21E389F18A3; mt_c_token=CWv5BQohyiR46Jbj1iJl2BLCqJwAAAAAjBAAAN1GNJr6yddGENq9A8R3Lf1avopClcYoeBADbMsQ3uFFOAYU2Vf7PkATpcBErhk-gg; isid=CWv5BQohyiR46Jbj1iJl2BLCqJwAAAAAjBAAAN1GNJr6yddGENq9A8R3Lf1avopClcYoeBADbMsQ3uFFOAYU2Vf7PkATpcBErhk-gg; logintype=normal; webp=1; __utmz=74597006.1646139987.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __mta=247420219.1646139986819.1646139986819.1646139989101.2; __utma=74597006.1303109177.1646139987.1646139987.1648393441.2; ci=55; cityname=%E5%8D%97%E4%BA%AC; uuid=961a798def054ff4a3cd.1648478674.1.0.0; JSESSIONID=node018kvf76ouab0e10n31816vqjlz59503641.node0; IJSESSIONID=node018kvf76ouab0e10n31816vqjlz59503641; oops=CWv5BQohyiR46Jbj1iJl2BLCqJwAAAAAjBAAAN1GNJr6yddGENq9A8R3Lf1avopClcYoeBADbMsQ3uFFOAYU2Vf7PkATpcBErhk-gg; u=936172994; latlng=32.041547%2C118.767417; ci3=55; i_extend=C_b1Gimthomepagecategory120'
        }
        # url
        self.url = 'https://i.meituan.com/lvyou/volga/api/iservice/trip/poi/select/city/'
        # ip代理
        self.proxy_list = [
            {'https': '49.83.204.46:29290'},
            {'https': '119.102.129.163:27893'},
            {'https': '61.154.90.209:33217'},
            {'https': '117.95.12.19:36044'},
            {'https': '123.162.27.208:49677'},
            {'https': '123.162.6.12:25230'},
            {'https': '114.232.110.199:23606'},
            {'https': '114.99.8.218:36360'},
            {'https': '110.81.106.175:34091'},
            {'https': '114.226.161.95:29468'},
        ]
        # 其他
        self.resp = None
        self.data_json = None
        self.save_json_path = ''

    def Link(self, cityId):
        self.data['cityId'] = cityId
        self.data['selectedCityId'] = cityId
        self.data['fromCityId'] = cityId
        self.url += str(cityId)
        # 随机的浏览器
        ua = fake_useragent.UserAgent()
        self.headers['User-Agent'] = str(ua.random)
        # 代理池
        proxy = random.choice(self.proxy_list)
        # 连接
        while True:
            # self.resp = requests.get(url=self.url, headers=self.headers, params=self.data, proxies=proxy)
            self.resp = requests.get(url=self.url, headers=self.headers, params=self.data)
            if self.resp.status_code == 200:
                break
            else:
                print("连接失败")
                print(f"Url: {self.url}")
                print(f"错误码: {self.resp.status_code}")
        self.data_json = self.resp.text
        self.resp.close()
        with open(self.save_json_path, 'w', encoding='utf-8') as f:
            f.write(self.data_json)

    def data_process(self, read_path, img_path, sheet, isSaveImg):
        with open(read_path, 'r', encoding='utf-8') as f:
            data_dict = json.load(f)['data']
        # 遍历每一个景点的数据
        i = 0
        for data in data_dict:
            i += 1
            place_type = data['cateName']   # 类型
            score = data['avgScore']        # 平均分
            area = data['areaName']         # 所属区域
            sales_volume = data['solds']    # 销售量
            img = data['frontImg']          # 图片链接
            name = data['name']             # 景区名
            lat = data['lat']               # 纬度
            lng = data['lng']               # 经度
            lowest_price = data['lowestPrice']  # 最低价
            avg_price = data['avgPrice']        # 平均价
            addr = data['addr']             # 地址
            infor = data['tour']['tourInfo']    # 景区简介
            # 保存图片
            if isSaveImg:
                img_save_path = os.path.join(img_path, f'{name}.jpg')
                # print(f"图片保存到: {img_save_path}")
                download_img(img, img_save_path)
            # 工作表存储数据
            # '景点名', '景点类型', '景点地址', '所属区域', 'URL', '平均分', '纬度', '经度', '销售量', '最低价', '平均价', '景区简介'
            sheet.append([name, place_type, addr, area, img, score, lat, lng, sales_volume, lowest_price, avg_price, infor])
            if i % 50 == 0:
                print(f"已经解析{i:3d}条景点信息...")
            # if i % 2 == 0:
            #     a = input("暂停")



