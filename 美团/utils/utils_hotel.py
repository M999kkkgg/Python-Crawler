import os.path
from utils.util import download_img
import requests
import json
import openpyxl
import random
import fake_useragent
import time


# wb = openpyxl.Workbook()
# sheet = wb.active()
# sheet.append(['酒店ID', '酒店名称', '酒店地址', '酒店类型', '价格', '评价', '经度', '纬度'])
def to_str(a):
    if not isinstance(a, list):
        return None
    if len(a) == 0:
        return "无"
    y = ''
    for i in range(len(a) - 1):
        y += str(a[i]) + ', '
    y += str(a[-1])
    return y


# x = ['wo', 'shi', 123]
# print(to_str(x))
# print(0)

class Hotel:
    def __init__(self):
        self.data = {
            'utm_medium': 'touch',
            'version_name': 999.9,
            'platformid': 1,
            'cateId': 20,
            'newcate': 1,
            'limit': 20,  # 每页最大数
            'offset': 0,  # 控制翻页 0 20 40 ...
            'cityId': 1,  # 城市id（已经获取保存在data/citys.xlsx中）
            'ci': 1,  # 与cityId相同
            'startendday': '20220329~20220329',
            'startDay': '20220329',
            'endDay': '20220329',
            'mypos': '33.041547%2C119.767417',
            'attr_28': 129,
            'sort': 'defaults',
            'userid': '936172994',
            'uuid': '5F859A86563CA88128213ED0AB205059B3A54688C77E8AF5D96FD21E389F18A3',
            'lat': '33.041547',
            'lng': '119.767417',
            'accommodationType': 1
        }
        # 请求头
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
            'Referer': 'https://i.meituan.com/',
            'Origin': 'https://i.meituan.com',
            }
        # url
        self.url = 'https://ihotel.meituan.com/hbsearch/HotelSearch'
        # 代理的ip
        self.proxy_list = []
        with open('ip.json', 'r', encoding='utf-8') as f:
            ips_dict = json.load(f)['data']
        for ip in ips_dict:
            dic = {'https': str(ip['ip']) + ':' + str(ip['port'])}
            self.proxy_list.append(dic)
        # 其他内容
        self.save_json_path = ''
        self.save_data_path = ''
        self.save_img_path = ''
        self.resp = None
        self.data_json = None

    def set_offset(self, page):
        """
        设置翻页，page = 0表示第1页...

        :param page: 页数
        :return: None
        """
        self.data['offset'] = page

    def set_city(self, city_id):
        """
        设置搜索城市的id

        :param city_id: 城市id
        :return:
        """
        self.data['cityId'] = city_id
        self.data['ci'] = city_id

    def set_day(self, start, end):
        """
        设置搜索的起止日期

        :param start: 起始日期
        :param end: 截止日期
        :return:
        """
        self.data['startendday'] = start + '~' + end
        self.data['startDay'] = start
        self.data['endDay'] = end

    def set_save_json_path(self, path):
        """
        设置爬取的Json数据的保存路径

        :param path: 路径
        :return:
        """
        self.save_json_path = path

    def set_save_data_path(self, path):
        """
        设置处理后的数据的保存路径

        :param path:
        :return:
        """
        self.save_data_path = path

    def Link(self, page, cityId, start, end):
        self.set_offset(page * 20)
        self.set_city(cityId)
        self.set_day(start, end)
        proxy = random.choice(self.proxy_list)      # 代理池
        ua = fake_useragent.UserAgent()             # 随机的浏览器
        self.headers['User-Agent'] = str(ua.random)
        self.resp = requests.get(url=self.url, headers=self.headers, params=self.data, proxies=proxy)
        if self.resp.status_code != 200:
            print(self.resp.status_code)
            print(f"ip: {proxy}")
            print(f"ua: {self.headers['User-Agent']}")
            exit(-1)
        # self.resp = requests.get(url=self.url, headers=self.headers, params=self.data)
        self.data_json = self.resp.text
        self.resp.close()
        with open(self.save_json_path, 'w', encoding='utf-8') as f:
            f.write(self.data_json)


    def data_process(self, read_path, save_img_path, city_name, page, sheet):
        dir_path = os.path.join(read_path, f"{city_name[1]}_{page:02d}.json")
        with open(dir_path, 'r', encoding='utf-8') as f:
            data_dict = json.load(f)['data']['searchresult']
        for data in data_dict:
            img = data['frontImg']
            addr = data['addr']
            name = data['name']
            areaName = data['areaName']
            lat = data['lat']
            lng = data['lng']
            price = data['lowestPrice']
            hotel_type = data['hotelStar']
            num = data['historyCouponCount']
            score = data['avgScore']
            labels = str(data['posdescr']).split(' · ')
            service = data['forward']['serviceIcons']
            services = []
            for x in service:
                services.append(x['attrDesc'])
            # print(Img, addr, name, areaName, lat, lng, price, type, num, score, labels, services, sep="\n")
            # 保存图片
            img_path = os.path.join(save_img_path, name+'.jpg')
            download_img(img, img_path)
            # 随机休眠1-3秒来模拟真实访问
            # time.sleep(random.randint(1, 3))
            # 其他数据解析到表格中
            # '酒店名称', '酒店地址', '酒店图片链接', '酒店所属区域', '纬度', '经度', '酒店类型', '酒店价格', '销售数', '评分', '标签', '可提供的服务'
            sheet.append([name, addr, img, areaName, lat, lng, hotel_type, price, num, score, to_str(labels), to_str(services)])



    # 数据解析
    """
    frontImg: 酒店图片(注意监测有无/w.h/字段，有的话删除即可访问到)
    addr: 地址
    areaName: 所属区域
    name: 酒店名
    lat: 纬度（北纬）
    lng: 经度（东经）
    lowestPrice: 价格
    hotelStar: 酒店类型：经济型，舒适型...
    historyCouponCount: 销售数
    avgScore: 评分
    posdescr: 优势，用' · '分割
    forward -> serviceIcons -> attrDesc 可提供的服务
    
    """


def ajax_url(ajax_path):
    headers = []
    params = []
    with open(ajax_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            line = line[:-1]
            header, param = line.split('?')
            headers.append(header)
            param = param.split('&')
            param_dict = {}
            for p in param:
                p1, p2 = p.split('=')
                param_dict[p1] = p2
            params.append(param_dict)
    return headers, params
