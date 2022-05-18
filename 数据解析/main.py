# -*- coding: utf-8 -*-
# written by msf

from OutputPackage import *
from TestPackage import *


# 实现第一个项目
def Project_1():
    for index in range(1, 14):
        GetPicture.InitDir(index)
        Jpgs = GetPicture.GetJPG(index)
        Jpgs.SendGet()
        Jpgs.GetData()
        Jpgs.DataAnalysis()
        Jpgs.SaveCSV()
        Jpgs.SaveJPG()


# 实现第二个项目
def Project_2():
    SanGuo.InitDir()
    book = SanGuo.GetSanguo()
    book.LinkGet()
    book.ReadData()
    book.ReadChapter()


# 实现第三个项目
def Project_3():
    citys = list(WuBaHouse.CityDict.keys())
    print("当前可支持的检索城市:")
    for i in range(len(citys)):
        print(f"\t{citys[i]}", end="")
        if (i+1) % 5 == 0:
            Fm.Newline()
    city = input("请输入你想检索的城市名称: ")
    page = input("请输入你想检索的页码: ")
    wu_ba = WuBaHouse.GetWuBa(page, city)
    wu_ba.InitDir()
    wu_ba.LinkURL()
    wu_ba.GetData()
    wu_ba.SaveCSV()


# 实现第四个项目
def Project_4():
    # Jpg = GetGaoqing.Get4k('1', '动漫')
    # Jpg.InitDir()
    # Jpg.LinkURL()
    # Jpg.GetData()
    # Jpg.SaveJPG()
    print("当前支持的图片种类")
    index = 0
    for x in list(GetGaoqing.ClassDict.keys()):
        print(f"\t{x}", end="")
        if (index+1) % 3 == 0:
            Fm.Newline()
        index += 1
    while True:
        Type = input("请输入你要检索的种类: ")
        if Type in GetGaoqing.ClassDict:
            break
    Jpg = GetGaoqing.Get4k('1', Type)
    Jpg.InitDir()
    Jpg.LinkURL()
    Jpg.GetData()
    Jpg.SaveJPG()
    print(f"共{Jpg.ReturnPageNum()}页")
    while True:
        temp = input("是否退出？（Y/N）: ")
        if temp == 'Y' or temp == 'y':
            return
        else:
            while True:
                temp = input(f"请输入继续检索 {Type} 类图片的页码（1-{Jpg.ReturnPageNum()}）: ")
                temp = int(temp)
                if temp <= 0 or temp > Jpg.ReturnPageNum():
                    continue
                else:
                    break
            Jpg = GetGaoqing.Get4k(str(temp), Type)
            Jpg.InitDir()
            Jpg.LinkURL()
            Jpg.GetData()
            Jpg.SaveJPG()


def Project_5():
    city = GetCityName.GetCity()
    city.InitDir()
    city.LinkURL()
    city.ReadData()
    city.SaveTXT()


def Project_6():
    pass


# 主函数
if __name__ == '__main__':
    Fm.Start_PG()
    # Project_1()
    # Project_2()
    # Project_3()
    # Project_4()
    # Project_5()
    Project_6()
    Fm.End_PG()
