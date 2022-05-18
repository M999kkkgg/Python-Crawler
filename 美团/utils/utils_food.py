import os.path
import requests
import json
import openpyxl
import random
import fake_useragent
from utils.util import download_img
import time
from tqdm import tqdm


def list_to_str(x_list):
    if len(x_list) == 0:
        return '无'
    out = ""
    i = 1
    for item in x_list:
        if i != len(x_list):
            out += str(item) + ', '
        else:
            out += str(item)
        i += 1
    return out


def data_process(read_path, save_img_path, sheet, isSaveImg):
    files_name = os.listdir(read_path)
    for file_name in files_name:
        # 对文件夹下每个Json进行处理
        with open(os.path.join(read_path, file_name), 'r', encoding='utf-8') as f:
            datas_json = json.load(f)['data']['poiList']['poiInfos']
        for data in datas_json:
            # 对每个json里每个美食进行处理
            name = data['name']     # 美食店名
            img = data['frontImg']   # 图片
            if img[0:4] != 'http':
                img = 'https:' + img
            food_type = data['cateName']        # 餐馆类
            avg_price = data['avgPrice']        # 均价
            avg_score = data['avgScore']        # 评分
            lat = data['lat']       # 纬度
            lng = data['lng']       # 经度
            area = data['areaName']             # 所属区域
            try:
                tag = data['smartTags'][0]['text']['content']  # 标签
            except:
                tag = "无"
            try:
                point_num = int(data['preferentialInfo']['maidan']['defaultShowNum'])    # 卖点的数目
                points = []     # 卖点
                for i in range(point_num):
                    temp = data['preferentialInfo']['maidan']['entries'][0]['content']
                    points.append(temp)
            except:
                points = ['无']
            # 保存图片
            if isSaveImg:
                img_path = os.path.join(save_img_path, f"{name}.jpg")
                download_img(img, img_path)
            # print(name, img, food_type, avg_price, avg_score, lat, lng, area, tag, list_to_str(points), sep="\n")
            # print(img_path)
            # x = input("暂停")
            # '店名', '店类型', '图片', '所属区域', '均价', '评分', '纬度', '经度', '标签', '卖点'
            sheet.append([name, food_type, img, area, avg_price, avg_score, lat, lng, tag, list_to_str(points)])

