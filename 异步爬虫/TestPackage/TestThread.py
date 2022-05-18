# -*- coding: utf-8 -*-
# written by msf

import time
import random
# 线程池
from multiprocessing import Pool

MaxLen = 5
NameList = [f"URL_{i:02d}" for i in range(1, MaxLen + 1, 1)]


def PrintTime(x, y):
    print(f"开始时间: {x}")
    print(f"结束时间: {y}")
    print(f"持续时间: {y-x}")


def GetPage(url: str):
    print(f"-*- 正在下载| {url} |", end="")
    time.sleep(random.randrange(0, 3))
    print(f"下载完成 -*-")
    return url


def Test_1():
    StartTime = time.time()
    # 单线程串行方式
    ReList = []
    print("(1) 单线程串行")
    for i in range(MaxLen):
        ReList.append(GetPage(NameList[i]))
    EndTime = time.time()
    print(f"获取的返回值列表: {ReList}")
    PrintTime(StartTime, EndTime)


def Test_2():
    StartTime = time.time()
    # 线程池方式
    ReList = []
    print("(2) 线程池")
    # 实例化线程池对象（参数表示开辟的线程数目）
    pool = Pool(5)
    # map 方法，返回值为列表
    ReList = pool.map(func=GetPage, iterable=NameList)
    EndTime = time.time()
    print(f"获取的返回值列表: {ReList}")
    PrintTime(StartTime, EndTime)
