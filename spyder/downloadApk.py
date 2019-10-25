#coding=utf-8
import urllib
import urllib.request
import io
import os
from lxml import etree
import re
import threading
import csv
from datetime import datetime,timedelta


class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

def downloadFile(dlink,savePath):
    resFlag = True
    try:
        urllib.request.urlretrieve(dlink, savePath)
    # print('downloaded')
    except:
    #     print('download faile')
        resFlag = False
    return resFlag

if __name__ == "__main__":
    debug = False
    yesterday = datetime.today() #+ timedelta(-1)
    currTime = yesterday.strftime('%Y-%m-%d')
    # currTime = currTime.strftime('%Y-%m-%d')
    apkDir = '/home/limin/Desktop/apks/huawei/todayApk-'+currTime
    if debug:
        apkDir = '/home/limin/Desktop/apks/huawei/testToday-'+currTime
    mkdir(apkDir)
    pwd = os.path.dirname(os.path.realpath(__file__))
    resPath = 'huawei-%s.csv' %currTime
    resPath = os.path.join(pwd,resPath)
    with open(resPath, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in spamreader:
            apkCode = row[0]
            dlink = row[11]
            print(apkCode+' '+dlink)
            savePath = os.path.join(apkDir, apkCode+'.apk')
            downloadFile(dlink, savePath)