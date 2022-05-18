import os
from utils.utils_hotel import Hotel
from utils.utils_citys import (get_city_ids, get_city_data, get_city_names)
from tqdm import tqdm
import random
import time
import openpyxl

if __name__ == "__main__":
    isSearch = False
    isSave = True

    # 获取城市信息
    city_path = os.path.join('data', 'city.json')
    city_ids = get_city_ids(city_path)
    city_names_ch, city_names_eng = get_city_names(city_path)
    # 构建酒店类
    hotel = Hotel()
    dir_path = os.path.join('data', 'hotel_infor')
    img_path = os.path.join('data', 'hotel_img')
    ddir_path = []  # json文件保存路径
    img_dir_path = []   # img保存路径
    # 初始化文件夹
    for city_name in city_names_eng:
        file_path = os.path.join(dir_path, city_name)
        file_path = os.path.join(file_path, 'json')
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        ddir_path.append(file_path)
        file_path2 = os.path.join(img_path, city_name)
        if not os.path.exists(file_path2):
            os.mkdir(file_path2)
        img_dir_path.append(file_path2)
    # 对每个城市爬取, 默认设置爬取前10页
    page_num = 10
    start = '20220328'
    end = '20220328'
    if isSearch:
        for city_id, city_name_ch, city_name_eng, d_path in zip(city_ids, city_names_ch, city_names_eng, ddir_path):
            print(f"爬取城市: {city_id}: {city_name_ch}  爬取内容共{page_num}页...")
            for i in tqdm(range(0, page_num)):
                file_name = city_name_eng + "_" + f"{i:02d}" + ".json"
                hotel.set_save_json_path(os.path.join(d_path, file_name))
                hotel.Link(i, city_id, start, end)
                # 随机休眠10-20秒来模拟真实访问
                time.sleep(random.randint(10, 20))
        print("结束爬取")
    # 对爬取内容数据处理（存储到xlsx表格与数据库中）
    if isSave:
        wb = openpyxl.Workbook()
        for path1, path2, city_name_ch, city_name_eng in zip(ddir_path, img_dir_path, city_names_ch, city_names_eng):
            wb.create_sheet(city_name_ch)
            sheet = wb[city_name_ch]
            sheet.append(['酒店名称', '酒店地址', '酒店图片链接', '酒店所属区域', '纬度', '经度', '酒店类型', '酒店价格', '销售数', '评分', '标签', '可提供的服务'])
            print(f'正在解析{city_name_ch}的酒店信息')
            for i in tqdm(range(0, page_num)):
                hotel.data_process(path1, path2, [city_name_ch, city_name_eng], i, sheet)
        hotel.set_save_data_path(os.path.join(dir_path, 'hotel.xlsx'))
        wb.save(hotel.save_data_path)
        print("数据解析完成")


