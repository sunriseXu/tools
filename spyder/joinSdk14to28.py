#coding=utf-8
import requests
import os
import sys
import re
import argparse
from datetime import datetime
import lxml
from lxml import etree
import logging
logging.basicConfig()
l = logging.getLogger("spyderAndroid")


pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules import SpyderUtils
from modules import FileUtils
from modules import CollectionUtils,RexUtils

#首先读取28的每一个json文件，与27的相同名字的json文件进行比较是否相等，这里仅仅比较api名字是否相同，如果27又多，那么加到总集中去。维护一个总集json文件的名字集合，并且与低级取差集，然后将差集并入总集合中。


destDir = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk_merged\\jsonRes'
FileUtils.mkdir(destDir)
# mergedFileName=[]
mergedFileDict = {}

# print(mergedFileName)

for i in range(0,15):
    dirPath = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk{}\\jsonRes'.format(28-i)

    dirItems = FileUtils.listDir2(dirPath)
    print(i)
    print(len(dirItems))
    intersecName = CollectionUtils.listIntersection(mergedFileDict.keys(), dirItems)
    diffName = CollectionUtils.listDifference(dirItems,mergedFileDict.keys())

    #处理差集
    for item in diffName:
        mergedFileDict[item] = FileUtils.readDict(os.path.join(dirPath, item))
    print('length of mergedfileDict:')
    print(len(mergedFileDict))
    # input()

    #处理交集
    #检查其中的api是否有增加的
    for item in intersecName:
        print(os.path.join(dirPath,item))
        lowerDict = FileUtils.readDict(os.path.join(dirPath,item))
        
        currentDict = mergedFileDict[item]
        currentFunctionDict = currentDict['Functions']
        lowerFunctionDict = lowerDict['Functions']
        diffFunctionList = CollectionUtils.listDifference(lowerFunctionDict.keys(),currentFunctionDict.keys())
        for diffFunc in diffFunctionList:
            if len(diffFunc)>50:
                continue
            print('diffFunc:'+diffFunc)
            currentFunctionDict[diffFunc] = lowerFunctionDict[diffFunc]
        mergedFileDict[item]['Functions'] = currentFunctionDict

for item in mergedFileDict:
    destPath = os.path.join(destDir, item)
    FileUtils.writeDict(mergedFileDict[item],destPath)
    

