import os
from utils.utils_place import Place
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
    # 构建景点类
    place = Place()
    infor_path = os.path.join('data', 'place_infor')
    img_path = os.path.join('data', 'place_img')
    img_dir_path = []   # img保存路径
    # 初始化文件夹
    if not os.path.exists(infor_path):
        os.mkdir(infor_path)
    for city_name in city_names_eng:
        file_path2 = os.path.join(img_path, city_name)
        if not os.path.exists(file_path2):
            os.mkdir(file_path2)
        img_dir_path.append(file_path2)
    # 对每个城市的景点信息进行爬取
    if isSearch:
        i = 1
        for city_id, city_name_ch, city_name_eng in zip(city_ids, city_names_ch, city_names_eng):
            print(f"正在爬取 {city_name_ch} {i}/{len(city_ids)}...")
            i += 1
            place.save_json_path = os.path.join(infor_path, city_name_ch + '.json')
            place.Link(city_id)
            # 随机休眠10-20秒来模拟真实访问
            seconds = random.randint(10, 20)
            print(f"随机休眠{seconds}s...")
            time.sleep(seconds)
        print("全部爬取完成")
    # 数据解析
    if isSave:
        isSaveImg = False
        wb = openpyxl.Workbook()
        for city_name_ch, path in zip(city_names_ch, img_dir_path):
            file_path = os.path.join(infor_path, f'{city_name_ch}.json')
            wb.create_sheet(city_name_ch)
            sheet = wb[city_name_ch]
            sheet.append(['景点名', '景点类型', '景点地址', '所属区域', 'URL', '平均分', '纬度', '经度', '销售量', '最低价', '平均价', '景区简介'])
            print(f"正在处理json: {file_path}...")
            place.data_process(read_path=file_path, img_path=path, sheet=sheet, isSaveImg=isSaveImg)
        wb_save_path = os.path.join(infor_path, 'place.xlsx')
        wb.save(wb_save_path)
        print("数据解析完成")
