# -*- coding: UTF-8 -*-
# 查询江苏各个城市的KFC餐厅信息

from OutputPackage import *
import requests
import os
import json
import pandas as pd


# 用户选择查询城市
def SelectCity(CityList):
    print("江苏的可选择城市如下: ")
    flag = False
    for j in range(len(CityList)):
        print(f"\t{CityList[j]}", end="")
        if (j + 1) % 8 == 0:
            Fm.Newline()
        else:
            flag = True
            continue
    if flag:
        Fm.Newline()
    while True:
        x = input("请选择你要查询的城市: ")
        if x in CityList:
            break
        else:
            continue
    return x


# 主函数
if __name__ == "__main__":
    Fm.Start_PG()
    # url
    PostUrl = "http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname"
    # UA
    UAHeaders = {
        'User-Agent': "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36",
        'Cookie': "route-cell=ksa; Hm_lvt_1039f1218e57655b6677f30913227148=1600065495; Hm_lpvt_1039f1218e57655b6677f30913227148=1600065598; ASP.NET_SessionId=3yo4cavvmn2zyqged2hjceh0; SERVERID=7b3e64f36ab4d9bcdfe1a64340ce30e8|1600065930|1600065494"
    }
    City_Su_List = [
        '常州', '常熟', '丹阳', '高邮', '句容', '淮安', '海门',
        '江都', '金坛', '江阴', '姜堰', '靖江', '昆山', '无锡',
        '南京', '溧阳', '邳州', '南通', '邳州', '启东', '如东',
        '如皋', '宿迁', '苏州', '太仓', '通州', '泰兴', '泰州',
        '吴江', '徐州', '新沂', '兴化', '扬州', '仪征', '盐城',
        '扬中', '宜兴', '镇江', '张家港'
    ]
    # 确定cname值
    CName = SelectCity(City_Su_List)
    # 确定其他属性值
    FromData = {
        'cname': CName,
        'pid': "",
        'pageIndex': '0',
        'pageSize': '10'
    }
    # 设置保存路径
    Path: str = os.getcwd() + f'\\Data\\KFC_Info\\{CName}\\JSON'
    # 判断某文件是否存在
    if not os.path.exists(Path):
        os.makedirs(Path)
    # 利用while与访问获得的条目数据进行循环访问，获得所有数据，并生成json文件
    while True:
        temp = int(FromData['pageIndex'])
        FromData['pageIndex'] = str(temp + 1)   # 页号加一
        # Post请求
        response = requests.post(url=PostUrl, data=FromData, headers=UAHeaders)
        DataJson = response.json()
        # 检测到无数据后就退出循环
        if len(DataJson['Table1']) != 0:
            # 设置文件名
            FileName = f"{CName}_Page{temp +1 :02d}.json"
            FilePath = os.path.join(Path, FileName)
            with open(FilePath, 'w', encoding='utf-8') as fp:
                json.dump(DataJson, fp, ensure_ascii=False, indent=4)
            fp.close()
        else:
            break
    del temp
    # 将保存的JSON文件转换为CSV文件
    Path_csv = os.getcwd() + f'\\Data\\KFC_Info\\{CName}'
    FileName_csv = f"{CName}_KFCInfo.csv"
    # 判断是否有旧的csv文件存在
    if os.path.exists(os.path.join(Path_csv, FileName_csv)):
        os.remove(os.path.join(Path_csv, FileName_csv))  # 有的话就删除
    Path_list = os.listdir(Path)
    Columns = ['序号', '餐厅名称', '餐厅地址', '详情信息']
    for i in range(len(Path_list)):
        temp = Path_list[i]
        fp_json = open(os.path.join(Path, temp), 'r', encoding='utf-8')
        fp_csv = open(os.path.join(Path_csv, FileName_csv), 'a', encoding='utf-8', newline='')  # 解决写入csv出现的多余换行
        DataTemp = json.load(fp_json)['Table1']
        data = pd.DataFrame({
            '序号': [DataTemp[i]['rownum'] for i in range(len(DataTemp))],
            '餐厅名称': [DataTemp[i]['storeName'] for i in range(len(DataTemp))],
            '餐厅地址': [DataTemp[i]['addressDetail'] for i in range(len(DataTemp))],
            '详情信息': [DataTemp[i]['pro'] for i in range(len(DataTemp))]
        }, columns=Columns)
        if i != 0:
            data.to_csv(fp_csv, encoding='UTF-8', header=False, index=False)
        else:
            data.to_csv(fp_csv, encoding='UTF-8', header=True, index=False)
        fp_csv.close()
        fp_json.close()
    Fm.End_PG()
