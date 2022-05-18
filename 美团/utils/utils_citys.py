import json
import os
import openpyxl


def save_citys(file_path):
    """
    读取utils下的city.json中的数据，并保存到data中的citys.xlsx

    :return: None
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)['data']
    # 创建新的工作簿
    wb = openpyxl.Workbook()
    # 在其中创建一张新的工作表
    wb.create_sheet("citys")
    sheet = wb["citys"]
    sheet.append(['id', '中文', '英文'])
    for item in json_data:
        sheet.append([item['id'], item['name'], item['pinyin']])
    save_path = os.path.join(os.path.abspath(os.path.dirname(os.getcwd())), 'data')
    save_path = os.path.join(save_path, 'citys.xlsx')
    wb.save(save_path)


def get_city_names(file_path):
    """
    读取utils下的city.json中的数据，并返回城市中文名和英文名
    仅返回前24个热门城市

    :return: 城市中文名(list), 城市英文名(list)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)['data']
    names_ch = []
    names_eng = []
    for item in json_data:
        names_ch.append(item['name'])
        names_eng.append(item['pinyin'])
    return names_ch[0:12], names_eng[0:12]


def get_city_ids(file_path):
    """
    读取utils下的city.json中的数据，并返回城市id
    仅返回前24个热门城市

    :return: 城市id(list)
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)['data']
    ids = []
    for item in json_data:
        ids.append(item['id'])
    return ids[0:12]


def get_city_data(file_path):
    """
    读取utils下的city.json中的数据，并返回全部信息
    仅返回前24个热门城市

    :return: 城市信息 [id],[name],[pinyin]
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        json_data = json.load(f)['data']
    return json_data[0:12]
