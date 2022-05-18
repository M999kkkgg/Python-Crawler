import os
from utils.utils_food import data_process
from utils.utils_citys import (get_city_ids, get_city_data, get_city_names)
from tqdm import tqdm
import random
import time
import openpyxl

if __name__ == "__main__":
    # 获取城市信息
    city_path = os.path.join('data', 'city.json')
    city_ids = get_city_ids(city_path)
    city_names_ch, city_names_eng = get_city_names(city_path)
    # 初始化文件夹
    json_path = os.path.join('data', 'food_infor')
    img_path = os.path.join('data', 'food_img')
    dir_json_path = []  # json文件保存路径
    dir_img_path = []   # img保存路径
    for city_name_eng in city_names_eng:
        file_json_path = os.path.join(json_path, city_name_eng)
        file_img_path = os.path.join(img_path, city_name_eng)
        if not os.path.exists(file_json_path):
            os.mkdir(file_json_path)
        if not os.path.exists(file_img_path):
            os.mkdir(file_img_path)
        dir_json_path.append(file_json_path)
        dir_img_path.append(file_img_path)
    # dir_json_path
    # ['data\\food_infor\\beijing', 'data\\food_infor\\shanghai', ... ]
    # dir_img_path
    # ['data\\food_img\\beijing', 'data\\food_img\\shanghai', ...]
    # print(dir_json_path)
    # print(dir_img_path)
    wb = openpyxl.Workbook()
    isSaveImg = True
    for i in range(len(city_ids)):
        # 建立一个子表
        wb.create_sheet(city_names_ch[i])
        sheet = wb[city_names_ch[i]]
        sheet.append(['店名', '店类型', '图片', '所属区域', '均价', '评分', '纬度', '经度', '标签', '卖点'])
        print(f"正在解析 {city_names_ch[i]}的数据")
        # 数据解析
        data_process(dir_json_path[i], dir_img_path[i], sheet, isSaveImg)
    # 保存表格
    wb.save(os.path.join(json_path, 'food.xlsx'))
    print("处理完成")

