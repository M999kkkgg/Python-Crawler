# -*- coding: UTF-8 -*-
# 获取国家药监局化妆品生产许可证相关数据

from OutputPackage import *
import requests
import os
import json
import pandas as pd
import shutil


# 根据参数path判断，存在则重置文件夹，不存在则创建新文件夹
def New_dir(DirPath: str):
    if not os.path.exists(DirPath):
        os.makedirs(DirPath)
    else:
        shutil.rmtree(DirPath)
        os.makedirs(DirPath)


# 初始化文件夹
def Init_Dir():
    path = os.getcwd()
    # 一级目录，Data文件夹已经存在了
    path = os.path.join(path, 'Data')
    # 二级目录
    path = os.path.join(path, 'Cosmetic_production_license_China')
    New_dir(path)
    # 三级目录
    path = os.path.join(path, 'ProInfo')
    New_dir(path)
    # Json与Csv目录
    path = os.getcwd()
    path = os.path.join(path, 'Data')
    path = os.path.join(path, 'Cosmetic_production_license_China')
    path = os.path.join(path, 'JSON')
    New_dir(path)
    path = os.getcwd()
    path = os.path.join(path, 'Data')
    path = os.path.join(path, 'Cosmetic_production_license_China')
    path = os.path.join(path, 'CSV')
    New_dir(path)


# json转换为csv文件
def JSON_2_CSV(FilePath):
    PathCSV = os.getcwd()
    PathCSV = os.path.join(PathCSV, 'Data')
    PathCSV = os.path.join(PathCSV, 'Cosmetic_production_license_China')
    PathCSV = os.path.join(PathCSV, 'CSV')
    Json_Name = os.listdir(FilePath)
    Columns = ['序号', 'ID', '企业名称', '许可证编号', '发证机关', '发证日期', '有效期至']
    for x in Json_Name:
        fp_json = open(os.path.join(FilePath, x), 'r', encoding='utf-8')
        fp_csv = open(os.path.join(PathCSV, f"BriefInfo.csv"), 'a', encoding='utf-8', newline="")
        DataTemp = json.load(fp_json)['list']
        data = pd.DataFrame({
            '序号': [(index+1) + (Json_Name.index(x)*15) for index in range(len(DataTemp))],
            'ID': [DataTemp[index]['ID'] for index in range(len(DataTemp))],
            '企业名称': [DataTemp[index]['EPS_NAME'] for index in range(len(DataTemp))],
            '许可证编号': [DataTemp[index]['PRODUCT_SN'] for index in range(len(DataTemp))],
            '发证机关': [DataTemp[index]['QF_MANAGER_NAME'] for index in range(len(DataTemp))],
            '发证日期': [DataTemp[index]['XC_DATE'] for index in range(len(DataTemp))],
            '有效期至': [DataTemp[index]['XK_DATE'] for index in range(len(DataTemp))],
        }, columns=Columns)
        if Json_Name.index(x) != 0:
            data.to_csv(fp_csv, encoding='UTF-8', header=False, index=False)
        else:
            data.to_csv(fp_csv, encoding='UTF-8', header=True, index=False)
        fp_csv.close()
        fp_json.close()


# 主函数
if __name__ == "__main__":
    Fm.Start_PG()
    # url
    # 获取总览页面
    post_url_1 = "http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsList"
    # 获取某个许可证的具体页面
    post_url_2 = "http://scxk.nmpa.gov.cn:81/xk/itownet/portalAction.do?method=getXkzsById"
    # ua
    UAHeader_1 = {
        'Content-Tpye': "application/x-www-form-urlencoded;utf-8",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Cookie': "JSESSIONID=934B4B4EC94E678AA175E4617B7D2967; acw_tc=2f624a0716000849562545396e53d32b800ce6ac632da2874b3c7ae151fd09; JSESSIONID=66A40F8483811FDEAA4FB96868697EF1"
    }
    UAHeader_2 = {
        'Content-Tpye': "application/x-www-form-urlencoded;utf-8",
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36",
        'Cookie': "JSESSIONID=0C73C0491520D5E56666599F0683E0B5; acw_tc=2f624a0c16000968688043020e66ad09424da54cf458ad065bac9b1082c1da; JSESSIONID=57768DD6F1B893673F97F87BEDF4B440"
    }
    # 新建文件夹
    Init_Dir()
    # 设置扫描总览页面的参数
    FromData_1 = {
        'on': 'true',
        'page': '1',
        'pageSize': '15',   # 每次爬取50条记录
        'productName:': '',
        'conditionType': '',
        'applyname': '',
        'applysn': ''
    }
    # 设置获取某个许可证的具体页面的参数
    FromData_2 = {
        'id': ""
    }
    # 设置路径
    PathJson = os.getcwd()
    PathJson = os.path.join(PathJson, 'Data')
    PathJson = os.path.join(PathJson, 'Cosmetic_production_license_China')
    PathJson = os.path.join(PathJson, 'JSON')
    # 爬取总览页面的数据，并存储到本地的json与csv文件中
    for i in range(1, 11):
        PageIndex = i
        FromData_1['page'] = str(PageIndex)
        # post
        # FromData_1_1 = json.dumps(FromData_1)
        if (PageIndex-1) % 2 == 0:
            BriefData = requests.post(post_url_1, FromData_1, headers=UAHeader_1, timeout=60)
        else:
            BriefData = requests.post(post_url_1, FromData_1, headers=UAHeader_2, timeout=60)
        BriefData = json.loads(BriefData.text)
        FileJson = f"BriefInfo_{(PageIndex-1)*15}_{PageIndex*15}.json"
        with open(os.path.join(PathJson, FileJson), 'w', encoding='utf-8') as fp:
            json.dump(BriefData, fp, ensure_ascii=False, indent=4)
        fp.close()
    # 批量读取PathTemp路径下的JSON文件，并将其本地化为CSV文件
    PathTemp = os.getcwd()
    PathTemp = os.path.join(PathTemp, 'Data')
    PathTemp = os.path.join(PathTemp, 'Cosmetic_production_license_China')
    PathTemp = os.path.join(PathTemp, 'JSON')
    JSON_2_CSV(PathTemp)
    # 根据存储的csv文件，获取某许可证编号的具体信息，并保存在ProInfo文件夹中（csv）
    # 获取文件地址
    PathTemp = os.getcwd()
    PathTemp = os.path.join(PathTemp, 'Data')
    PathTemp = os.path.join(PathTemp, 'Cosmetic_production_license_China')
    PathTemp = os.path.join(PathTemp, 'ProInfo')
    FileName = "ProInfo.csv"
    CSV_Path = os.getcwd()
    CSV_Path = os.path.join(CSV_Path, 'Data')
    CSV_Path = os.path.join(CSV_Path, 'Cosmetic_production_license_China')
    CSV_Path = os.path.join(CSV_Path, 'CSV')
    CSV_Path = os.path.join(CSV_Path, 'BriefInfo.csv')
    # 读取csv文件，并获取其中ID属性列的值
    csv_data = pd.read_csv(CSV_Path, usecols=['ID'])
    # 把dataframe转化为list
    csv_data = [x for x in csv_data['ID']]
    # 遍历csv_data根据id作为参数访问url_2
    Columns = ['序号', '企业名称', '许可证编号', '许可项目', '企业住所', '生产地址', '社会信用代码', '法人', '企业负责人',
               '质量负责人', '发证机关', '签发人', '日常监督管理机构', '日常监督管理人员', '有效期至', '发证日期', '是否进口']
    index = 0
    for x in csv_data:
        index += 1
        FromData_2['id'] = x
        ProData = requests.post(post_url_2, FromData_2, headers=UAHeader_1, timeout=60)
        ProData = json.loads(ProData.text)
        # 打开要存储的csv文件
        fp = open(os.path.join(PathTemp, FileName), 'a', encoding='utf-8', newline="")
        data = pd.DataFrame({
            '序号': str(index),    '企业名称': ProData['epsName'],
            '许可证编号': ProData['productSn'],  '许可项目': ProData['certStr'],
            '企业住所': ProData['epsAddress'],  '生产地址': ProData['epsProductAddress'],
            '社会信用代码': ProData['businessLicenseNumber'], '法人':ProData['legalPerson'],
            '企业负责人': ProData['businessPerson'], '质量负责人': ProData['qualityPerson'],
            '发证机关': ProData['qfManagerName'],   '签发人': ProData['xkName'],
            '日常监督管理机构': ProData['rcManagerDepartName'],
            '日常监督管理人员': ProData['rcManagerUser'],
            '有效期至': ProData['xkDate'],  '发证日期': ProData['xkDateStr'],
            '是否进口': ProData['isimport']
        }, columns=Columns, index=[0])
        if (index-1) != 0:
            data.to_csv(fp, encoding='UTF-8', header=False, index=False)
        else:
            data.to_csv(fp, encoding='UTF-8', header=True, index=False)
        fp.close()
    Fm.End_PG()
