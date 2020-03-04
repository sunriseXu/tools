#coding=utf-8
import os
import sys
pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)
from modules import FileUtils
from modules import CollectionUtils

from modules import RexUtils
from modules import AdbUtils
from modules import ApkUtils
from modules.FileUtils import EasyDir
# from modules import SpyderUtils
from modules import InteractUtils
from modules import ThreadUtils
import os
import shutil
import random
import logging
import sys
import time
from datetime import datetime
import argparse 
from modules import InteractUtils
import Levenshtein
import random
import itertools
def isBasicType(className):
    className = className.strip('[]')
    if className=='int' or className=='boolean' or className=='byte'\
        or className=='short' or className=='char' or className=='long'\
            or className=='float' or className=='double' or className=='void':
            return True
    else:
        return False
def IsSysClazzOrDeObfuscated(className, DeObfuscatedClazzSet=[]):
    if className in DeObfuscatedClazzSet or className.startswith('android.')\
         or className.startswith('java.') \
             or className.startswith('javax.') or isBasicType(className):
            return True
    else:
        return False
def obfuscateClazz(className,sperator='.'):
    clazzParts = className.split(sperator)
    if '$' in clazzParts[-1]:
        clazzParts[-1] = obfuscateClazz(clazzParts[-1],'$')
    else:
        clazzParts[-1] = 'c'
    for idx in range(len(clazzParts)-1):
        clazzParts[idx] = 'c'
    className = sperator.join(clazzParts)
    return className
def obfuscateMethod(fullName):
    clazzNameOri,methodName,params = splitFullMethodName(fullName)
    commonLenList = []
    
    clazzName = obfuscateClazz(clazzNameOri)
    if '<init>' not in methodName:
        methodName = 'm'
    obfuParams = []
    newParams = []
    for param in params:
        if IsSysClazzOrDeObfuscated(param):
            newParams.append(param)
        else:
            obfuParams.append(param)
            newParams.append(obfuscateClazz(param))
    paramStr = ','.join(newParams)
    if obfuParams:
        obfuParams.append(clazzNameOri)
        commonLenList = commonLenMatrix(obfuParams)
        #这里想要计算每个参数之间的公共最长前缀，但是发现有问题
        #因为一个包下面有些类会被混淆，有些类则不会

    return '{}.{}({})'.format(clazzName, methodName, paramStr),commonLenList
#对解混淆的尝试
def findExactMacthing(matchingDict):
    for methodIdentifier in matchingDict:

        methodIdentifierOb, commonLenListBase = obfuscateMethod(methodIdentifier)
        
        topDict = matchingDict[methodIdentifier]['topN']
        topMethod = topDict[0]
        topMethodIdenti = topMethod[0]
        topRatio = topMethod[1]

        topMethodIdentiOb, commonLenListTar = obfuscateMethod(topMethodIdenti)

        if methodIdentifierOb == topMethodIdentiOb:# and 'com.linecorp.line.story.viewer.c.a.k.a' in methodIdentifier:
            print(methodIdentifier)
            print(topMethodIdenti)
            print(topRatio)

            print(commonLenListBase)
            print(commonLenListTar)
            matrixEqual = compareTwoDemenMatrix(commonLenListBase, commonLenListTar)
            print("equal:{}".format(matrixEqual))
            print()
            #两种情况 包结构改变了 或者参数部分参数混淆 而部分没有
            # 出现这种情况的原因是什么？ 把类名和包名进行比较了 类名之间不能比较
            input()
def splitFullMethodName(item):
    tmp = item.strip().split('(')
    fullName = tmp[0]
    params = tmp[1].strip(')').split(',')
    fullNameList = fullName.split('.')
    clazz = fullNameList[0:-1]
    clazzName = '.'.join(clazz)
    methodName = fullNameList[-1].strip()
    return clazzName, methodName, params
def compareTwoClazz(clazz1, clazz2):
    clazzList1 = clazz1.split('.')
    clazzList2 = clazz2.split('.')
    commonLen = 0
    minLen = min(len(clazzList1), len(clazzList2))
    if 0 < minLen and len(clazzList1)!=len(clazzList2):
        minLen = minLen - 1 #去除类的比较
    diffFlag = False
    idx = 0
    for idx in range(0,minLen):
        if clazzList1[idx] == clazzList2[idx]:
            # print('{} and {} equal'.format(clazzList1[idx],clazzList2[idx]))
            continue
        else:
            commonLen = idx 
            diffFlag = True
            break
    if commonLen == 0 and not diffFlag:
        commonLen = minLen
    return commonLen
def commonLenMatrix(classNameList):
    resList = []
    for i in range(0,len(classNameList)):
        baseClazz = classNameList[i]
        tmpList = []
        for j in range(0,len(classNameList)):
            tarClazz = classNameList[j]
            commonLen = compareTwoClazz(baseClazz, tarClazz)
            tmpList.append(commonLen)
        resList.append(tmpList)
    return resList
def compareTwoDemenMatrix(matrix1, matrix2):
    if len(matrix1)!=len(matrix2):
        return False
    for i in range(len(matrix1)):
        for j in range(len(matrix1)):
            if matrix1[i][j] != matrix2[i][j]:
                return False
    return True
if __name__ == "__main__":
    
    matchingDict = FileUtils.readDict('do2000Evaluation.json')
    findExactMacthing(matchingDict)
    