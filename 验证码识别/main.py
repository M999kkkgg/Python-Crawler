# -*- coding: utf-8 -*-
# written by msf
# main.py

import os
from OutputPackage import *
from TestPackage import *
from TTShiTu import *
from PIL import Image


def InitDataDir():
    path = os.getcwd()
    path = os.path.join(path, 'Data')
    if not os.path.exists(path):
        os.makedirs(path)
    else:
        pass


# 调用API示例
def Project_1():
    path = os.getcwd()
    path = os.path.join(path, '验证码测试图片')
    file_list = os.listdir(path)
    uname = 'msf1189'
    password = 'msf97347110'
    for x in file_list:
        filepath = os.path.join(path, x)
        img = Image.open(filepath)
        temp = stAPI.base64_api(uname, password, img, '3')
        print(f"图片\'{x}\'的识别结果: {temp}")


# 查询账户信息
def Project_2():
    uname = 'msf1189'
    password = 'msf97347110'
    stAPI.GetUInfo(uname, password)
    Fm.Newline()
    print("当前账户余额:", stAPI.GetBalance(uname, password))


def Project_3():
    log = LogGushiwen.LogGSW()
    log.InitDir()
    log.LinkLog_1()
    log.GetJPG()
    log.Distinguish()


if __name__ == '__main__':
    Fm.Start_PG()
    InitDataDir()
    # Project_1()
    # Project_2()
    Project_3()
    Fm.End_PG()
