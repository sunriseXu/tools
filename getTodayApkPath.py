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
from modules import AdbUtils
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
def readXlsx(filePath):
    
if __name__ == "__main__":
    # rootDir = "/home/limin/Desktop/apks/huawei"
    # dirDict = rexDir(rootDir)
    # allDirs = dirDict.values()
    # resDict = getAllApkDict(allDirs)
    # print(resDict)
    # destPath = "/home/limin/Desktop/logs_today/allapkDict.json"
    # FileUtils.writeDict(resDict,destPath)
    rootDir = "/home/limin/Desktop/logs_today/allFp"
    apkPaths = FileUtils.listDir(rootDir)
    for apk in apkPaths:
        fileName = os.path.basename(apk).split('.')[0]
        apkName= AdbUtils.getApkInfo(apk,"label=")
        print  fileName,apkName
