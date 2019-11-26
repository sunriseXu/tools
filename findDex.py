#coding=utf-8
from modules import FileUtils
# from modules import CollectionUtils

from modules import RexUtils
from modules import AdbUtils
from modules import ApkUtils
from modules.FileUtils import EasyDir
# from modules import SpyderUtils
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
import argparse 
def findMatchedPath(className,fileList):
    packages = className.split('.')
    res = []
    for file in fileList:
        findFlag = True
        for package in packages:
            # for windows file seperator only
            package = '\\'+package
            if package not in file:
                findFlag = False
                break
        
        if findFlag and (packages[-1]+'.smali' in file):
            res.append(file)
    return res
def findDex(className, myDirs, cacheDir=''):
    '''
    className是要找的类的全称，myDir是解包后的目录，
    cacheDir是缓存目录（如果多次运行，那么直接从缓存中取结果）
    cache目录只缓存myDir对应的结果，并且一一对应
    myDir唯一的标准是创建时间，而非修改时间
    '''
    fileList = []
    for myDir in myDirs:
        tmpList = []
        #if cacheDir exist
        if cacheDir:
            dirName = os.path.basename(myDir)
            createTime = str(os.path.getctime(myDir))
            cacheName = dirName+'-'+createTime+'.txt'
            myCacheFile = os.path.join(cacheDir,cacheName)
            if os.path.exists(myCacheFile):
                # read txt file to list
                tmpList = FileUtils.readList(myCacheFile)
            else:
                tmpList = FileUtils.listDirRecur(myDir)
                #write to cache file
                FileUtils.writeList(tmpList, myCacheFile)
        else:
            tmpList = FileUtils.listDirRecur(myDir)
        fileList.extend(tmpList)
    # now fileList contains all path string
    resPathList = findMatchedPath(className,fileList)
    return resPathList

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="find dex!!")
    parser.add_argument('-n', '--classname', help='class name', nargs='?', default="") # ?-> 0个或多个参数 + ->1个或多个
    parser.add_argument('-d', '--dirname', nargs='+', help='dir name') #多个参数 默认放入list中 +表示至少一个 + 就放在list中
    parser.add_argument('-t', '--tmp', help='tmp dir', nargs='?',default="")
    args = parser.parse_args() 
    myDirs=args.dirname 
    className=args.classname
    cacheDir=args.tmp

    print("className: "+className)
    print("dexDirs: "+str(myDirs))
    print("cacheDir: "+cacheDir)
    res = findDex(className,myDirs,cacheDir)
    InteractUtils.showList(res)

