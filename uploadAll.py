#coding=utf8
import os
import sys

import psutil
from datetime import datetime
from modules import ThreadUtils
from datetime import datetime,timedelta
from configparser import ConfigParser
from modules import FileUtils
from modules import RexUtils
import subprocess
# python /home/limin/Desktop/mygit/tools/oneShot_perday.py -d /home/limin/Desktop/logs_today/logs_today-2019-09-30 -i 10.141.209.138:6603 -u antivirus -s antivirus -b antivirus -t per_day_2019_09_30
def rexDir(rootDir):
    allDir = FileUtils.listDir(rootDir)
    myRex = r'todayApk-(\d+-\d+-\d+)' #todayApk-2019-07-29
    filterDir = {}
    for item in allDir:
        res = RexUtils.rexFind(myRex,item)
        if res:
            filterDir.update({res[0]:item})
    return filterDir

def getAllApkDict(malDirs):
	dirList = malDirs
	allFileList = []
	for mydir in dirList:
		allFileList = allFileList + FileUtils.listDirRecur(mydir)
	print(len(allFileList))
	rex = r'.*?\.apk'
	for item in allFileList:
		res = RexUtils.rexFind(rex, item)
		if not res:
			allFileList.remove(item)
	apkDict = {}
	rex = r'/([^/]*?\.apk)'
	for item in allFileList:
		res = RexUtils.rexFind(rex, item)
		if not res:
			print item
		else:
			bs = os.path.basename(item)
			apkDict[bs] = item
	return apkDict

if __name__ == "__main__":
    tracesHead = '/home/limin/Desktop/logs_today/'
    allDir = FileUtils.listDir(tracesHead)
    myRex = r'logs_today-(\d+-\d+-\d+)'
    filterDir = {}
    for item in allDir:
        res = RexUtils.rexFind(myRex,item)
        if res:
            filterDir.update({res[0]:item})
    print(len(filterDir))
    validDir = {}
    #筛选出含有trace的日期和文件夹
    for key in filterDir:
        value = filterDir[key]
        traceDir = os.path.join(value,'logs/traces')
        if os.path.exists(traceDir):
            tracesList = FileUtils.listDir(traceDir)
            if len(tracesList)>0:
                validDir.update({key:traceDir})
            else:
                print(traceDir+" is empty")
        else:
            print(traceDir+" not exists")
    #将所有trace都合并到同一个trace文件夹中
    newTracesDir = '/home/limin/Desktop/logs_today/traces_8-10'
    FileUtils.mkdir(newTracesDir)

    for key in validDir:
        value = validDir[key]
        print("start to copy {} to newdir".format(value))
        FileUtils.copytree(value,newTracesDir)

    

