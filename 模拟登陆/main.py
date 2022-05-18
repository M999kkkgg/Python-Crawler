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
    log = LogGushiwen.LogGSW()
    log.InitDir()
    log.LinkLog_1()
    log.GetJPG()
    log.Distinguish()
    log.LinkLog_2()
    log.GetUserData()


if __name__ == '__main__':
    Fm.Start_PG()
    InitDataDir()
    Project_1()
    Fm.End_PG()
