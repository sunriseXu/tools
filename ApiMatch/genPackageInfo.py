#coding=utf-8
import os
import sys
pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)
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
from zss import simple_distance, Node


def genPackageInfo(root, destDictPath):
    resDict = {}
    ChildInst = FileUtils.EasyDir(root)
    childDict = ChildInst.getAbsPathDict()
    # print(childDict)
    hasPackage = False
    hasClazz = False
    for key in childDict:
        value = childDict[key]
        if os.path.isdir(value):
            #如果这是一个文件夹的话
            hasPackage = True
            tmp = genPackageInfo(value,destDictPath)
            if 'package' not in resDict:
                resDict['package'] = {key:tmp}
            else:
                resDict['package'][key] = tmp
        else:
            if '.smali' in key:
                hasClazz = True
                tmp = key.split('.smali')[0].strip()
                if not tmp:
                    assert(0 == 1)
                if 'class' not in resDict:
                    resDict['class'] = [tmp]
                else:
                    resDict['class'].append(tmp)
            else:
                assert(0 == 1)
    if not hasPackage:
        resDict['package']={}
    if not hasClazz:
        resDict['class']=[]
    return resDict
def jaccard_similarity(list1, list2):
        s1 = set(list1)
        s2 = set(list2)
        if len(s1.union(s2)) == 0:
            return 1.0
        return len(s1.intersection(s2)) / len(s1.union(s2))
if __name__ == "__main__":
    root = 'F:\\LINE_ALL_SMALI\\line-9-21-1-merge\\smali'
    # tmp = genPackageInfo(root,"")
    # FileUtils.writeDict(tmp,"line-9-21-1.json")
    # print('done')
    # input()
    # 首先处理明显未混淆的包，找到两个line中相同的类
    unobfusedList = ['addon','android','androidx',
                'com','ezvcard','io','jp','kotlin','kotlinx',
                'net','okhttp3','org',
                ]
    baseDict = FileUtils.readDict("line-9-21-1.json")
    targetDict = FileUtils.readDict("line-9-22-2.json")
    basePackageDict = baseDict['package']
    targetPackageDict = targetDict['package']
    # 如果明显看不出来，那只能用树的编辑距离来进行匹配
    def packageMatchN(basePackageDict, key):

        root = Node('a')
        basePackageSet = basePackageDict[key]['package'].keys()
        # print(basePackageSet)
        baseClazzSet = basePackageDict[key]['class']

        # 添加所有的类
        for clazz in baseClazzSet:
            root.addkid(Node('a'))
        
        for ckey in basePackageSet:
            childNode = packageMatchN(basePackageDict[key]['package'],ckey)
            root.addkid(childNode)
        return root
    for basekey in basePackageDict:
        if basekey in unobfusedList:
            continue
        print("***********start to compare {}**********".format(basekey))
        baseTree = packageMatchN(basePackageDict, basekey)

        for item in targetPackageDict:
            if item in unobfusedList:
                continue
            print("deal with:{}".format(item))
            targetTree = packageMatchN(targetPackageDict, item)
            print("get tree done!")
            res = simple_distance(baseTree, targetTree)
            print('item dist {}:{}'.format(item,res)) 



    #这个函数要返回一个置信度
    def packageMatch(basePackageDict, targetPackageDict):
        for key in basePackageDict:
            print('start to deal package:{}'.format(key))
            
            basePackageSet = basePackageDict[key]['package'].keys()
            print(basePackageSet)
            baseClazzSet = basePackageDict[key]['class']
            if key in targetPackageDict:
                ##优先对相同的报名进行比较 第一层比较
                targetPackageSet = targetPackageDict[key]['package'].keys()
                print(targetPackageSet)
                targetClazzSet = targetPackageDict[key]['class']
                packageSimilarity = jaccard_similarity(basePackageSet, targetPackageSet)
                clazzSimilarity = jaccard_similarity(baseClazzSet, targetClazzSet)
                print('packageSimilarity with {}:{}'.format(key,packageSimilarity))
                print('clazzSimilarity with {}:{}'.format(key,clazzSimilarity))
                ## todo 继续第二层匹配
                packageMatch(basePackageDict[key]['package'],targetPackageDict[key]['package'] )
                # input()
            # else:
            for tkey in targetPackageDict:
                if key == tkey:
                    continue
                targetPackageSet = targetPackageDict[tkey]['package'].keys()
                print(targetPackageSet)
                targetClazzSet = targetPackageDict[tkey]['class']
                packageSimilarity = jaccard_similarity(basePackageSet, targetPackageSet)
                clazzSimilarity = jaccard_similarity(baseClazzSet, targetClazzSet)
                print('packageSimilarity with {}:{}'.format(tkey,packageSimilarity))
                print('clazzSimilarity with {}:{}'.format(tkey,clazzSimilarity))
                packageMatch(basePackageDict[key]['package'],targetPackageDict[tkey]['package'] )
                # input()

    # packageMatch(basePackageDict, targetPackageDict)