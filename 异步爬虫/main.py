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
    path = os.getcwd()
    path = os.path.join(path, 'Notes')
    if not os.path.exists(path):
        os.makedirs(path)


def Project_1():
    TestThread.Test_1()
    TestThread.Test_2()
    pass


def Project_2():
    video = GetLivideo.GetVideo()
    video.InitDir()
    video.Link_1()


if __name__ == '__main__':
    Fm.Start_PG()
    InitDataDir()
    # Project_1()
    Project_2()
    Fm.End_PG()
