#coding=utf-8
from modules import FileUtils
from modules import CollectionUtils

from modules import RexUtils
from modules import AdbUtils
from modules import ApkUtils
from modules import FileUtils
from modules.FileUtils import EasyDir
from modules import SpyderUtils
from modules import InteractUtils
from modules import ThreadUtils
from rooms import FileRoom
import os
import shutil
import random
import logging
import sys
import time
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Pool

def chooseDevice():
    adbCmd="adb devices"
    res =os.popen(adbCmd).read()
    res = res.strip().split('\n')
    res = [i.strip().split()[0:2] for i in res]
    res = [i[0] for i in res if "device" in i]
    res1=[]
    for item in res:
        if item not in res1:
            res1.append(item)
    res=res1
    return res
def muteMusic(selectedDevId):
    cmd = 'adb -s {} shell media volume --set 0'.format(selectedDevId)
    print(cmd)
    res = os.popen(cmd).read()
    return res
# def queryMusic(selectedDevId):
#     cmd = 'adb {} shell media volume '
if __name__ == "__main__":
    
    
    deviceList = chooseDevice()
    while(True):
        for devicdId in deviceList:
            muteMusic(devicdId)
        time.sleep(5)