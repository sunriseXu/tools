#coding=utf-8
import os
import sys
# pwd = os.path.dirname(os.path.realpath(__file__))
pwd = os.getcwd()
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)
from modules import FileUtils
from modules import CollectionUtils

from modules import RexUtils
from modules import AdbUtils
from modules import ApkUtils
from modules.FileUtils import EasyDir
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

class Method:
    def __init__(self, modifier, methodName, params, retType, constStrList,classDict,invokeList,callers):
        #修饰符，列表
        self.modifier = modifier
        #方法名，字符串
        self.methodName = methodName
        #参数，列表
        self.params = params
        #返回值，字符串
        self.retType = retType
        #常量字符串，列表
        self.constStrList = constStrList
        #类,类字典
        self.classDict = classDict
        #调用的java/android 方法,字符串列表，android/java/org
        self.invokeList = invokeList
        #调用的自定义方法，列表？表示方法的对象
        #调用这个方法的其他方法 列表 表示方法的对象
        self.callers = callers
        #方法内部的控制流图？图的表示 关键部分
        #方法内部的数据流图 图的表示 关键部分
        #这个方法出发的函数调用图 图的表示 关键部分



## 0层 简单的判断和字符串操作 简单的容器操作
def isBasicType(className):
    '''
    判断一个类是否是基本类型
    返回布尔值
    '''
    className = className.strip('[]')
    if className=='int' or className=='boolean' or className=='byte'\
        or className=='short' or className=='char' or className=='long'\
            or className=='float' or className=='double' or className=='void':
            return True
    else:
        return False
def IsSysClazzOrDeObfuscated(className, DeObfuscatedClazzSet):
    '''
    判断一个类是否是系统api
    返回布尔值
    '''
    if className in DeObfuscatedClazzSet or className.startswith('android.')\
         or className.startswith('java.') \
             or className.startswith('javax.') or isBasicType(className):
            return True
    else:
        return False
def isCostomerClazz(clazz):
    '''
    这里判断是否是app自定的方法，即非系统方法，由于发现app会对androidx，com.google包进行混淆
    '''
    if clazz.startswith('android.') or clazz.startswith('androidx.')\
            or clazz.startswith('com.google.') or clazz.startswith('com.facebook.')\
                or clazz.startswith('org.') or clazz.startswith('okhttp3.')\
                    or clazz.startswith('kotlin.') or clazz.startswith('addon.')\
                        or clazz.startswith('com.airbnb') or clazz.startswith('kotlinx.')\
                        	or clazz.startswith('net.') or clazz.startswith('kotlinx.')\
                        		or clazz.startswith('javax.') or clazz.startswith('com.ad'):
                                return False
    else:
        return True
### 0层 把参数列表转换成认为可读的字符串形式
def list2Str(myList):
    res = '('
    if len(myList) == 0:
        return '()'
    for idx in range(len(myList)):
        if idx != len(myList)-1:
            res += myList[idx]+','
        else:
            res += myList[idx]+')'
    return res
def calTopN(myList,N,newElem):
    for idx in range(0,N):
        if newElem[1]<myList[idx][1]:
            myInsert(myList,idx,newElem,N)
            break
def myInsert(myList,idx,value,N):
    assert(idx>=0 and idx<N)
    for i in range(N-1,-1,-1):
        if i == idx:
            break
        myList[i] = myList[i-1]
    myList[idx] = value
    return myList
### 0层 判断列表元素符合条件的个数
def sysClassNum(params):
    '''
    统计参数中包含的系统参数的数量，用于筛选一定长度的包含系统类的参数
    '''
    count = 0
    for item in params:
        if item.startswith('java.') or item.startswith('android.')\
            or item.startswith('javax.') or item.startswith('androidx.'):
            count+=1
    return count
def concatList(myList, sperator='##'):
    return sperator.join(myList)
def splitFullMethodName(item):
    '''
    基础重要方法，对完整方法名进行分离成 类名 方法名 参数
    输入：
        item：完整方法名
    输出：
        方法名的分解
    '''
    tmp = item.strip().split('(')
    fullName = tmp[0]
    params = '('+tmp[1]
    fullNameList = fullName.split('.')
    clazz = fullNameList[0:-1]
    clazzName = '.'.join(clazz)
    methodName = fullNameList[-1].strip()
    methodIdentifier = methodName+params
    return clazzName, methodName, params,methodIdentifier
## 算法层 简单算法
def jaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    if len(s1.union(s2)) == 0:
        return 1.0
    return len(s1.intersection(s2)) / len(s1.union(s2))
### 路径操作，在原路径中，对文件名添加后缀
def addExt2Path(oriPath, myExt):
    '''
    路径操作，在原路径中，对文件名添加后缀
    输入：
        oriPath：原始路径
        myExt：文件需要添加的后缀
    输出：
        添加完后缀的文件路径
    '''
    targetDir = os.path.dirname(oriPath)
    targetName = os.path.basename(oriPath)
    bsName = os.path.splitext(targetName)[0]
    if len(os.path.splitext(targetName))>1:
        ext = os.path.splitext(targetName)[1]
    else:
        ext = ''
    bsName = bsName+myExt+ext
    destPath = os.path.join(targetDir,bsName)
    return destPath

### 1层 统计类
###1 层 对字典中的字段进行简单的统计
def getCalleeLen(methodDict):
    '''
    参数是代表方法的字典，返回这个方法invoke callee序列的长度
    '''
    invokeList = methodDict['invoke']
    return len(invokeList)
def tongjilei(packageDict):
    '''
    统计这个包下面类的数量，方法的数量，字段的数量
    '''
    clazzCount = len(packageDict)
    methodCount = 0
    fieldCount = 0
    for clazz in packageDict:
        classDict = packageDict[clazz]
        methodDictList = classDict['methods']
        methodCount+=len(methodDictList)
        fields = classDict['fields']
        fieldCount+= len(fields['staticFields'])
        fieldCount+= len(fields['instanceFields'])
    print("clazzCount:{}".format(clazzCount))
    print("methodCount:{}".format(methodCount))
    print("fieldCount:{}".format(fieldCount))
def sysApiNum(invokeList):
    '''
    统计invokelist中包含的系统api的数量，用于筛选一定长度的syscallee函数
    '''
    count = 0
    for invokeDict in invokeList:
        className = invokeDict['className'][0]
        if className.startswith('java.') or className.startswith('android.')\
            or className.startswith('javax.') or className.startswith('androidx.'):
            count+=1
    return count

### 对字典字段的简单查询
def getCaller(basePackageDict, fullName):
    '''
    打印一个函数所有的caller信息
    输入：
        basePackageDict：app包
        fullName：函数的完整签名
    输出：
        caller信息
    '''
    className, _, _, methodIdentifier = splitFullMethodName(fullName)
    classDict = getClass(basePackageDict, className)
    res = ''
    if not classDict:
        return res
    methodDict = getMethod(classDict,methodIdentifier)
    if 'caller' in methodDict:
        callers = methodDict['caller']
        print(callers)
    else:
        print("no caller found")

### 查询类 返回类字典
def getClass(packageDict, className):
    if className in packageDict:
        return packageDict[className]
    return {}

### 查询方法 返回方法字典
def getMethod(classDict,methodIdentifier):
    '''
    在类字典中根据方法签名获取方法字典
    输入：
        classDict：类字典
        methodIdentifier：方法签名 去类
    输出：
        方法字典
    '''
    methodDictList = classDict['methods']
    if methodIdentifier in methodDictList:
        return methodDictList[methodIdentifier]
    else:
        print("no method found in this classDict! {}".format(methodIdentifier))
        return {}

### 通过callee长度和参数长度 筛选出符合条件的方法列表 
def SelectAPI(packageDict, paramMin=2, sysParmMin=2, calleeMin=10, sysApiRotio=0.4):
    '''
    从app包中筛选出包含一定参数、callee符合指定长度的方法列表
    返回合格的方法列表
    '''
    resList = []
    for clazz in packageDict:
        if not isCostomerClazz(clazz):
            continue
        classDict = packageDict[clazz]
        methodDictList = classDict['methods']
        for methodIdentifer in methodDictList:
            #取出这个类中的所有方法
            key = "{}.{}".format(clazz, methodIdentifer)
            methodDict = methodDictList[methodIdentifer]
            params = methodDict['methodParams']
            invokeList = methodDict['invoke']
            if len(params)>paramMin and sysApiNum(invokeList)>=5:
                resList.append(key)
    return resList

### 打印类中所有方法的签名 简单的字典查询
def printClazzMethodIdenti(packageDict,clazz):
    classDict = getClass(packageDict,clazz)
    methodDictList = classDict['methods']
    identifierList = methodDictList.keys()
    InteractUtils.showList(identifierList)
    return identifierList
#列举出每一个类中的常量字符串
def getClazzConstStr(packageDict,clazz):
    classDict = getClass(packageDict,clazz)
    if not classDict:
        print("not class found!")
        return
    print("class found!!!!")
    methodDictList = classDict['methods']
    allConstStr = set()
    for methodIdentifier in methodDictList:
        methodDict = methodDictList[methodIdentifier]
        constStr = methodDict['constStr']
        allConstStr=allConstStr.union(set(constStr))
    InteractUtils.showList(allConstStr)
### 对结果字典进行格式化打印
def GetMatchedResult(resDict):
    '''
    打印匹配的结果
    '''
    ## 有这种情况 那就是调用runThread函数，一个是用java方法调用的，另一个是用自己实现的方法调用
    ## 这种情况下callee匹配不会准确的 除非将callee中的自定义方法都修改成父类java/安卓方法
    minCalleeLen = 3
    minSimilarity = 0.2
    idx = 0
    for clazz in resDict:
        methodDict = resDict[clazz]
        if clazz.startswith('androidx.') or clazz.startswith('org.') or clazz.startswith('com.ad'):
            continue
        for methodIdentifier in methodDict:
            idx+=1
            matchRes = methodDict[methodIdentifier]
            topN = matchRes['topN']
            callee = matchRes['callee']
            calleeLen = len(callee)
            if topN:
                if calleeLen<minCalleeLen or topN[0][1]['r']>minSimilarity:
                    continue
                
                print("line0:{}.{}".format(clazz,methodIdentifier))
                print("line1:{}.{}".format(clazz,topN[0][0]))
                print("similarity:{}".format(topN[0][1]['r']))
                print()
    print('methodNumber:{}'.format(idx))

### 2 查询字典，并且做计算 生成新的字段 例如特征生成
### 获取方法的特征向量，基础中基础，这是统一封装的接口
def getMethodFeature(className, methodDict, DeObfuscatedClazzSet=set(),useReplace=True):
    '''
    输入：
        className: 这个方法的类名
        methodDict:这个方法的包
    输出：
        这个方法的 签名特征字符串 callee特征字符串 和 常量字符串
    '''
    # 这里是查询是否有methodFeature字段，用于已经缓存过特征向量的字典
    res = getMethodFeature2(methodDict)
    if res:
        return res
    modifier = methodDict['modifier']
    methodName = methodDict['methodName']
    params = methodDict['methodParams']
    callers = methodDict['caller']
    # 对方法的参数归一化处理
    unifiedParams = []
    idx = 0
    for item in params:
        idx+=1
        if IsSysClazzOrDeObfuscated(item, DeObfuscatedClazzSet):
            unifiedParams.append(item)
        else:
            if useReplace:
                unifiedParams.append('x{}'.format(idx))
            else:
                unifiedParams.append(item)
    paramsStr = ''
    if unifiedParams:
        paramsStr = ', '.join(unifiedParams)
    retType = methodDict['retType']
    retStr = ''
    if retType:
        if IsSysClazzOrDeObfuscated(retType[0], DeObfuscatedClazzSet):
            retStr = retType[0]
        else:
            if useReplace:
                retStr = 'RET'
            else:
                retStr = retType[0]
    invokeList = methodDict['invoke']
    constStrList = methodDict['constStr']

    AllCallee = []
    sysAndDeObCallee = []
    ObfuscatedCallee = []
    for invokeDict in invokeList:
        isSysOrDeOb,invokeStr = getInvokeFeature(invokeDict, DeObfuscatedClazzSet,useReplace)
        AllCallee.append(invokeStr)
        if isSysOrDeOb or not useReplace:
            sysAndDeObCallee.append(invokeStr)
        else:
            ObfuscatedCallee.append(invokeStr)
    clazzParts = className.split('.')
    if '$' in clazzParts[-1]:
        clazzParts[-1] = 'c$c'
    else:
        clazzParts[-1] = 'c'
    for idx in range(len(clazzParts)-1):
        clazzParts[idx] = 'c'
    className = '.'.join(clazzParts)
    methodHeader = '{} {} {}.{}({})'.format(modifier, retStr, className,methodName,paramsStr)
    return methodHeader, constStrList, AllCallee, sysAndDeObCallee, ObfuscatedCallee
### 如果有特征字段，那么直接返回
def getMethodFeature2(methodDict):
    if 'methodFeature' not in methodDict:
        return ''
    else: 
        return methodDict['methodFeature']
### 获取callee特征，基础中的基础
def getInvokeFeature(invokeDict, DeObfuscatedClazzSet,useReplace=True):
    '''
    获取callee序列的特征
    输入：
        invokeDict:方法的callee字典
        DeObfuscatedClazzSet：两个版本共同的类交集，预设是没有混淆的类
        useReplace：对自定义且混淆的累是否采用x替换策略
    输入：
        方法的callee序列，syscallee序列，非syscallee序列
    '''
    invokeType = invokeDict['invokeType']
    className = invokeDict['className'][0]
    methodName = invokeDict['methodName']
    params = invokeDict['methodParams']
    IsSysOrDeOb = False
    if IsSysClazzOrDeObfuscated(className, DeObfuscatedClazzSet):
        IsSysOrDeOb = True
    unifiedParams = []
    idx = 0
    for item in params:
        idx+=1
        if IsSysClazzOrDeObfuscated(item, DeObfuscatedClazzSet):
            unifiedParams.append(item)
        else:
            if useReplace:
                unifiedParams.append('x{}'.format(idx))
            else:
                unifiedParams.append(item)
    paramsStr = ''
    if unifiedParams:
        paramsStr = ', '.join(unifiedParams)
    
    retType = invokeDict['retType']
    retStr = ''
    if retType:
        if IsSysClazzOrDeObfuscated(retType[0], DeObfuscatedClazzSet):
            retStr = retType[0]
        else:
            if useReplace:
                retStr = 'RET'
            else:
                retStr = retType[0]
    invokeStr = '{} {} {}.{}({})'.format(invokeType,retStr, className,methodName,paramsStr)
    return IsSysOrDeOb,invokeStr
### 查询或者计算方法的特征向量，根据packageDict的是否包含特征字段来区分 废弃
def findMethod(packageDict,className, methodName, params,intersecSet,useReplace=True):
    '''
    废弃方法，通过类名，方法名和参数来获得方法的特征向量
    '''
    res = ''
    className = className.strip()
    methodName = methodName.strip()

    classDict = getClass(packageDict, className)
    if not classDict:
        return res

    methodIdentifier = methodName+params
    methodDict = getMethod(classDict,methodIdentifier)
    
    if methodDict:
        res = getMethodFeature(className, methodDict,intersecSet,useReplace) 
    return res
### 查询或者计算方法的特征向量，根据packageDict的是否包含特征字段来区分
def findMethod2(packageDict, className, methodSig, intersecSet, useReplace=True):
    '''
    通过类名和方法签名获取方法的特征向量
    输入：
        packageDict：方法所在的包
        className:方法名
        methodSig：方法签名 除去类
    '''
    res = ''
    classDict = getClass(packageDict, className)
    if not classDict:
        return res
    methodDict = getMethod(classDict,methodSig)
    
    if methodDict:
        res = getMethodFeature(className, methodDict,intersecSet,useReplace)
    return res

### 打印一个方法的特征向量,对字典的简单查询，可能涉及到特征向量的计算
def printMethodFeature(basePackageDict, fullName, intersecSet, useReplace=True):
    '''
    打印一个方法的特征向量
    输入：
        basePackageDict：app包
        fullName：方法的完整签名
    输出：
        这个方法的callee列表，可以拓展成完整签名
    '''
    clazz, _, _, methodIdentifier = splitFullMethodName(fullName)
    baseMethodFeature = findMethod2(basePackageDict, clazz,methodIdentifier, intersecSet, useReplace)
    InteractUtils.showList(baseMethodFeature[2])
    return baseMethodFeature

# 关于解耦，参数尽量传元素而非列表，如下面，sameClazz是sameClazzList 元素
def getClazzMethodFeature(classDict, clazz,intersecSet, useReplace):
    '''
    获取这个class中所有方法的方法特征向量
    输入：
        ClassDict：这个类字典
        clazz：这个类名，比较冗余
    输出：
        所有方法签名及其对应的方法特征向量
    '''
    methodFeatureDict = {}
    methodDictList = classDict['methods']
    for methodIdentifer in methodDictList:
        #取出这个类中的所有方法
        methodDict = methodDictList[methodIdentifer]
        methodFeature = getMethodFeature(clazz, methodDict,intersecSet,useReplace)
        methodFeatureDict[methodIdentifer] = methodFeature
    return methodFeatureDict

### 生成类字段特征
def genFieldFeature(fieldsDict):
    staticFields = fieldsDict['staticFields']
    instanceFields = fieldsDict['instanceFields']
    staticTypeList = []
    instanceTypeList = []
    for item in staticFields:
        staticTypeList.append(staticFields[item]['type'][0])
    for item in instanceFields:
        instanceTypeList.append(instanceFields[item]['type'][0])
    return staticTypeList, instanceTypeList
### 生成class特征
def genClazzFeature(packageDict,clazz):
    classDict = packageDict[clazz]
    _genClazzFeature(classDict)
def _genClazzFeature(classDict):
    #'classModifier':classModifier,'super':supName,'implements':impList, 'imports':importList,'fields':fieldsDict,'methods':methodLists
    modifier = classDict['classModifier']
    supName = classDict['super']
    imports = classDict['imports']

    #修正import问题
    importList = []
    for item in imports:
        item = item[0]
        if ':L' in item:
            item = item.split(':L')[-1].strip('[')
        elif '[L' in item:
            item = item.split('[L')[-1]
        if item not in importList:
            importList.append(item)
    
    fieldsDict = classDict['fields']
    staticTypeList, instanceTypeList = genFieldFeature(fieldsDict)
    methodList = classDict['methods']
    methodIdentifiers = methodList.keys()
    for methodkey in methodList:
        methodDict = methodList[methodkey]
        
    print(modifier)
    print(supName)
    print(importList)
    print(staticTypeList)
    print(instanceTypeList)
    print(methodIdentifiers)

### 包生成，添加childClass字段，生成每个类的继承关系
def GenInherit(packageDict,newDictPath):
    for clazz in packageDict:
        classDict = packageDict[clazz]
        superCls = classDict['super']
        implementList = classDict['implements']
        if superCls and not superCls.startswith('java.') and not superCls.startswith('android.')\
            and not superCls.startswith('androidx.') and not superCls.startswith('org.')\
                and not superCls.startswith('javax.') and not superCls.startswith('com.google.')\
                and not superCls.startswith('com.samsung.android.sep')\
                    and not superCls.startswith('com.facebook.'):
            superClsDict = packageDict[superCls] #父类字典
            if 'childClass' in superClsDict:
                superClsDict['childClass'].append(clazz)
            else:
                superClsDict.update({'childClass':[clazz]})
        if implementList:
            for impl in implementList:
                if not impl.startswith('java.') and not impl.startswith('android.')\
                    and not impl.startswith('androidx.') and not impl.startswith('org.')\
                        and not impl.startswith('javax.')and not impl.startswith('com.google.')\
                            and not impl.startswith('com.facebook.'):#'jp.naver.line.android.b.e$d'
                    superClsDict = packageDict[impl] #接口字典
                    if 'childClass' in superClsDict:
                        superClsDict['childClass'].append(clazz)
                    else:
                        superClsDict.update({'childClass':[clazz]})
    FileUtils.writeDict(packageDict, newDictPath)

### 特征包的抽取，形成键值对的形式 其输出供traverseClazzMethod3使用
def extractAllMethodFeature(packageDict,intersecSet,useReplace):
    '''
    生成特征字典：
    提取出所有方法特征，用 方法签名:特征向量 的字典来存放，字典需要存起来
    packageDict: 目标app包结构
    intersecSet：如果动态生成的话需要这个结构，否则不用
    useReplace:动态生成的情况下是否需要替换自定义参数为 x
    '''
    resDict = {}
    for clazz in packageDict:
        classDict = packageDict[clazz]
        methodDictList = classDict['methods']
        for methodIdentifer in methodDictList:
            methodDict = methodDictList[methodIdentifer]
            targetMethodFeature = getMethodFeature(clazz, methodDict,intersecSet,useReplace)
            key = '{}.{}'.format(clazz,methodIdentifer)
            resDict[key] = targetMethodFeature
    return resDict
### 特征包的预计算，并且记录到字典，其输出供extractAllMethodFeature使用
def genAllClazzMethodFeature(packageDict, intersecSet,useReplace):
    '''
    生成一个app包下面所有方法的特征，并且存在每个方法字典的 methodFeature字段
    packageDict: 目标app包
    intersecSet：特征需要引入两个app之间的交集类
    useReplace：是否在生成特征的时候用x来替换自定义参数类
    '''
    idx = 0
    for clazz in packageDict:
        classDict = packageDict[clazz]
        methodDictList = classDict['methods']
        for methodIdentifer in methodDictList:
            idx +=1
            print(idx)
            #取出这个类中的所有方法
            key = "{}.{}".format(clazz, methodIdentifer)
            methodDict = methodDictList[methodIdentifer]
            # 首先看这个
            targetMethodFeature = getMethodFeature(clazz, methodDict,intersecSet,useReplace)
            methodDict['methodFeature'] = targetMethodFeature


### 3 高层算法 即新的字段参与的计算
## 匹配核心方法 计算两个特征向量之间的距离
def calFeatureSimilarity(baseMethodFeature, targetMethodFeature, useDebug=False):
    '''
    计算两个特征之间的距离，分别是第一个特征和第二个特征，useDebug会打印计算的距离值
    '''
    baseMethodHeader = str(baseMethodFeature[0])
    baseConstList = str(concatList(baseMethodFeature[1]))
    baseCallee = str(concatList(baseMethodFeature[2]))
    baseSysOrDeCallee = str(concatList(baseMethodFeature[3]))
    baseObfuscCallee = concatList(baseMethodFeature[4])

    baseMethodHeaderLen = float(len(baseMethodHeader))
    baseCalleeLen = float(len(baseCallee))
    baseSysOrDeCalleeLen = float(len(baseSysOrDeCallee))
    baseObfuscCalleeLen = float(len(baseObfuscCallee))

    targetMethodHeader = str(targetMethodFeature[0])
    targetConstList = str(concatList(targetMethodFeature[1]))
    targetCallee = str(concatList(targetMethodFeature[2]))
    targetSysOrDeCallee = str(concatList(targetMethodFeature[3]))
    targetObfuscCallee = concatList(targetMethodFeature[4])

    ## 对方法名进行相似度计算
    # print(baseMethodHeader,targetMethodHeader)
    # input()
    dist1 = Levenshtein.distance(baseMethodHeader,targetMethodHeader)
    partitionR1 = dist1/baseMethodHeaderLen
    # if partitionR1>1:
    #     partitionR1 = 1
    # partitionR1 = 1 - partitionR1
    
    # 对callee计算相似度
    if baseSysOrDeCallee:
        dist2 = Levenshtein.distance(baseSysOrDeCallee,targetSysOrDeCallee)
        partitionR2 = dist2/baseSysOrDeCalleeLen
        # if partitionR2>1:
        #     partitionR2 = 1
        # partitionR2 = jaccard_similarity(baseMethodFeature[3],targetMethodFeature[3])
        # print('baseSysOrDeCallee:\n{}\ntargetSysOrDeCallee:\n{}'.format(baseSysOrDeCallee,targetSysOrDeCallee))            
    else:
        dist2 = Levenshtein.distance(baseCallee,targetCallee)
        if not baseCallee and not targetCallee:
            partitionR2 = 0
        elif not baseCallee:
            partitionR2 = 1
        else:
            tmp = dist2/baseCalleeLen
            if tmp>1:
                partitionR2 = 1
            else:
                partitionR2 = tmp
    # partitionR2 = 1 - partitionR2

    useLevens = False
    partitionR3 = 0
    # 对常量字符串计算相似度
    if baseConstList:
        if useLevens:
            dist3 = Levenshtein.distance(baseConstList,targetConstList)
            partitionR3 = dist3/float(len(baseConstList))
            # print('baseConstList:{}\n\ntargetConstList:{}'.format(baseConstList,targetConstList))
        else:
            partitionR3 = jaccard_similarity(baseMethodFeature[1], targetMethodFeature[1])
            # print('baseConstList:{}\n\ntargetConstList:{}'.format(baseFeature[1],targetFeature[1]))     
            partitionR3 = 1-partitionR3
    if useDebug:
        print('basekey:{}\ntargetKey:{} \ndist:{} ratio:{}'.format(baseMethodHeader,targetMethodHeader,dist1,partitionR1))
        InteractUtils.showList(baseMethodFeature[3])
        print()
        InteractUtils.showList(targetMethodFeature[3])
        print('SysOrDeCallee ratio:{}'.format(partitionR2))
        print()
        print(baseMethodFeature[1])
        print()
        print(targetMethodFeature[1])
        print('constStr ratio:{}'.format(partitionR3))
        print('all ratio:{}'.format(partitionR1+partitionR2+partitionR3))
    return partitionR1, partitionR2, partitionR3, partitionR1+partitionR2

### 单方法匹配，低效，考虑废弃
def traverseClazzMethod(packageDict,baseMethodFeature, intersecSet,useReplace):
    '''
    单个方法的匹配，这个函数可以获取所有匹配距离，暂时还有用
    输入：
        packageDict: 需要全方法搜索的app包
        baseMethodFeature:目标方法的特征向量
    输出：
        这个方法的所有匹配结果排序列表，按距离从小到大排序
    '''
    sortedList = _traverseClazzMethod(packageDict, baseMethodFeature, intersecSet, useReplace)
    return sortedList
def _traverseClazzMethod(packageDict, baseMethodFeature, intersecSet,useReplace):
    a = 0.6
    low = 1-a
    high = 1+a
    resDict = {}
    sortedList = []
    baseLen = len(baseMethodFeature[2])+0.0
    #取出每一个类
    idx = 0
    for clazz in packageDict:
        classDict = packageDict[clazz]
        methodDictList = classDict['methods']
        for methodIdentifer in methodDictList:
            idx +=1
            #取出这个类中的所有方法
            key = "{}.{}".format(clazz, methodIdentifer)
            methodDict = methodDictList[methodIdentifer]
            # 首先看这个
            targetCalleeLen = getCalleeLen(methodDict)
            if targetCalleeLen>baseLen*low and targetCalleeLen<baseLen*high:
                targetMethodFeature = getMethodFeature(clazz, methodDict,intersecSet,useReplace)
                r1,r2,r3,rT = calFeatureSimilarity(baseMethodFeature, targetMethodFeature)
                resDict.update({key:rT})
                print(idx)
                print(methodIdentifer)
                print("similarity:{}".format(rT))
    sortedList = sorted(resDict.items(), key=lambda x:x[1])
    return sortedList
### 多方法同时匹配，低效，考虑废弃
def traverseClazzMethod2(packageDict, baseMethodFeatureDict, intersecSet,useReplace):
    '''
    实时生成方法的特征向量，效率过于低下，考虑废弃
    输入：
        packageDict:需要进行全方法遍历的包，原始包，不包含方法特征向量字段
        baseMethodFeatureDict:包含需要进行匹配的方法及其特征向量字典
    输出：
        baseMethodFeatureDict中的方法的匹配结果，其返回结果写入baseMethodFeatureDict字典中
    '''
    a = 0.6
    low = 1-a
    high = 1+a
    N = 3
    #取出每一个类
    idx = 0
    for key in baseMethodFeatureDict:
        cachedDict = baseMethodFeatureDict[key]
        if 'topN' not in cachedDict:
            cachedDict['topN'] = [('',100),('',100),('',100),('',100)]
    
    for clazz in packageDict:
        if not isCostomerClazz(clazz):
            continue
        classDict = packageDict[clazz]
        methodDictList = classDict['methods']
        for methodIdentifer in methodDictList:
            idx +=1
            #取出这个类中的所有方法
            key = "{}.{}".format(clazz, methodIdentifer)
            methodDict = methodDictList[methodIdentifer]
            # 首先看这个
            targetCalleeLen = getCalleeLen(methodDict)
            for baseKey in baseMethodFeatureDict:
                cachedDict = baseMethodFeatureDict[baseKey]
                baseMethodFeature = cachedDict['Feature']
                
                baseLen = len(baseMethodFeature[2])+0.0
                if targetCalleeLen>baseLen*low and targetCalleeLen<baseLen*high:
                    targetMethodFeature = getMethodFeature(clazz, methodDict,intersecSet,useReplace)

                    r1,r2,r3,rT = calFeatureSimilarity(baseMethodFeature, targetMethodFeature)
                    # middleResDict[baseKey].update({key:rT})
                    calTopN(cachedDict['topN'],N,(key,rT))
                    print(idx)
                    print(methodIdentifer)
                    print("similarity:{}".format(rT))
    return baseMethodFeatureDict
### 多方法同时匹配，高效
def traverseClazzMethod3(packageDict, baseMethodFeatureDict, intersecSet,useReplace):
    '''
    对特征向量列表进行全局搜索匹配
    输入：
        packageDict：目标app包的特征向量键值对
        baseMethodFeatureDict：目标特征向量列表
    输出：
        目标特征向量的topN匹配结果
    '''
    a = 0.6
    low = 1-a
    high = 1+a
    N = 3
    #取出每一个类
    idx = 0
    for key in baseMethodFeatureDict:
        cachedDict = baseMethodFeatureDict[key]
        if 'topN' not in cachedDict:
            cachedDict['topN'] = [('',100),('',100),('',100),('',100)]
        if 'length' not in cachedDict:
            cachedDict['length'] = 0
    
    for fullName in packageDict:
        idx+=1
        clazz,_,_,_=splitFullMethodName(fullName)
        if not isCostomerClazz(clazz):
            continue
        targetMethodFeature = packageDict[fullName]
        targetCalleeLen = len(targetMethodFeature[2])
        
        
        for baseKey in baseMethodFeatureDict:
            cachedDict = baseMethodFeatureDict[baseKey]
            baseMethodFeature = cachedDict['Feature']
            
            baseLen = len(baseMethodFeature[2])+0.0
            if targetCalleeLen>baseLen*low and targetCalleeLen<baseLen*high:
                r1,r2,r3,rT = calFeatureSimilarity(baseMethodFeature, targetMethodFeature)
                
                calTopN(cachedDict['topN'],N,(fullName,rT))
                cachedDict['length'] += 1
                print(idx)
                print(fullName)
                print("similarity:{}".format(rT))
    return baseMethodFeatureDict

### 鸡肋方法，对交集类之间进行匹配
def MatchSameClazz(baseDict, targetDict, sameClazz,intersecSet,useReplace):
    '''
    对两个包中的相同类的方法进行匹配，匹配范围仅限相同类，这个方法很鸡肋
    输入：
        baseDict：第一个app包
        targetDict：待匹配的app包
        sameClazz：相同的类名，即交集类
    输出：
        所有相同类中方法的匹配结果，存于字典中
    '''
    a = 0.8
    topN = 3
    classDict = baseDict[sameClazz]
    baseFeatureDict = getClazzMethodFeature(classDict, sameClazz,intersecSet,useReplace)

    targetClassDict = targetDict[sameClazz]
    targetFeatureDict = getClazzMethodFeature(targetClassDict, sameClazz,intersecSet,useReplace)
    resDict = {}
    for basekey in baseFeatureDict:
        baseFeature = baseFeatureDict[basekey]
        baseMethodHeader = baseFeature[0]
        baseConstList = concatList(baseFeature[1])
        baseCallee = concatList(baseFeature[2])
        baseSysOrDeCallee = concatList(baseFeature[3])
        baseObfuscCallee = concatList(baseFeature[4])

        baseMethodHeaderLen = float(len(baseMethodHeader))
        baseCalleeLen = float(len(baseCallee))
        baseSysOrDeCalleeLen = float(len(baseSysOrDeCallee))

        resDict[basekey] = {}
        resDict[basekey]['methodHeader'] = baseMethodHeader
        resDict[basekey]['const'] = baseFeature[1]
        resDict[basekey]['callee'] = baseFeature[2]
        
        matchingRes = {}
        matchingTopN = []
        for tkey in targetFeatureDict:
            targetFeature = targetFeatureDict[tkey]
            targetMethodHeader = targetFeature[0]
            targetConstList = concatList(targetFeature[1])
            targetCallee = concatList(targetFeature[2])
            targetSysOrDeCallee = concatList(targetFeature[3])
            targetObfuscCallee = concatList(targetFeature[4])
            matchingRes[tkey] = {}
            matchingRes[tkey]['methodHeader'] = targetMethodHeader
            matchingRes[tkey]['const'] = targetFeature[1]
            matchingRes[tkey]['callee'] = targetFeature[2]
            ## 对方法名进行相似度计算
            dist = Levenshtein.distance(baseMethodHeader,targetMethodHeader)
            partitionR1 = dist/baseMethodHeaderLen
            print('basekey:{}\ntargetKey:{} \ndist:{} ratio:{}'.format(baseMethodHeader,targetMethodHeader,dist,partitionR1))
            matchingRes[tkey]['r1'] = partitionR1
            # 对callee计算相似度
            if baseSysOrDeCallee:
                dist = Levenshtein.distance(baseSysOrDeCallee,targetSysOrDeCallee)
                partitionR2 = dist/baseSysOrDeCalleeLen
                # print('baseSysOrDeCallee:\n{}\ntargetSysOrDeCallee:\n{}'.format(baseSysOrDeCallee,targetSysOrDeCallee))
                print('SysOrDeCallee dist:{} ratio:{}'.format(dist,partitionR2))
            else:
                dist = Levenshtein.distance(baseCallee,targetCallee)
                if not baseCallee and not targetCallee:
                    partitionR2 = 0
                elif not baseCallee:
                    partitionR2 = 2
                else:
                    partitionR2 = dist/baseCalleeLen
                print('SysOrDeCallee dist:{} ratio:{}'.format(dist,partitionR2))
            matchingRes[tkey]['r2'] = partitionR2
            useLevens = False
            partitionR3 = 0
            # 对常量字符串计算相似度
            if baseConstList:
                if useLevens:
                    dist = Levenshtein.distance(baseConstList,targetConstList)
                    partitionR3 = dist/float(len(baseConstList))
                    # print('baseConstList:{}\n\ntargetConstList:{}'.format(baseConstList,targetConstList))
                    print('baseConstList Levenshtein dist:{} ratio:{}'.format(dist,partitionR3))
                else:
                    partitionR3 = jaccard_similarity(baseFeature[1], targetFeature[1])
                    # print('baseConstList:{}\n\ntargetConstList:{}'.format(baseFeature[1],targetFeature[1]))
                    print('jaccard_similarity dist:{} ratio:{}'.format(dist,partitionR3))
                partitionR3 = 1-partitionR3
            matchingRes[tkey]['r3'] = partitionR3
            matchingRes[tkey]['r'] = partitionR1+partitionR2+partitionR3
        sortedList = sorted(matchingRes.items(), key=lambda x:x[1]['r'])
        idx = 0
        for item in sortedList:
            idx += 1
            matchingTopN.append(item)
            if idx >= topN:
                break
        resDict[basekey]['topN'] = matchingTopN
    return resDict

### 对单个函数的全局搜索匹配 低效
def compareAll(basePackageDict, fullName, tarPackageDict,intersecSet,useReplace=True):
    '''
    对单个函数的全局搜索匹配 低效
    输入：
        basePackageDict：目标函数所在的app包
        fullName：目标函数的完整签名
        tarPackageDict：需要进行全局搜索的函数
    输出：
        这个函数的匹配所有匹配结果，排序
    '''
    clazz, _, _, methodIdentifier = splitFullMethodName(fullName)
    baseMethodFeature = findMethod2(basePackageDict, clazz,methodIdentifier, intersecSet, useReplace)
    print(fullName)
    resList = traverseClazzMethod(tarPackageDict, baseMethodFeature, intersecSet,useReplace)
    return resList

### 对一对函数进行匹配计算，多用于调试
def compareTwo(basePackageDict, fullName, tarPackageDict,fullName2,intersecSet,useReplace=True):
    '''
    对一对函数进行匹配计算，多用于调试
    输入：
        basePackageDict:第一个函数所在的app包
        fullName：第一个函数完整签名
        tarPackageDict：第二个函数所在的app包
        fullName2：第二个函数完整签名
    输出：
        特征向量之间的匹配结果，debug开启会打印出来
    '''
    clazz, _, _, methodIdentifier = splitFullMethodName(fullName)
    baseMethodFeature = findMethod2(basePackageDict, clazz,methodIdentifier, intersecSet, useReplace)

    clazz2, _, _, methodIdentifier2 = splitFullMethodName(fullName2)
    targetMethodFeature = findMethod2(tarPackageDict, clazz2,methodIdentifier2, intersecSet, useReplace)
    calFeatureSimilarity(baseMethodFeature,targetMethodFeature,True)

### 对两个列表的函数进行匹配 鸡肋
def getAccessment(basePackageDict, accessmentList, tarPackageDict, accessmentList2):
    '''
    对两个列表的函数进行匹配 鸡肋 两个列表需要在两个app包中一一对应
    输入：
        basePackageDict：第一个函数列表所在的app包
        accessmentList：第一个函数列表
    输出：
        函数列表的相互比较结果，是compareTwo的拓展
    '''
    tmpList = []
    idx = 0
    for item in accessmentList:
        clazz, methodName, params, methodIdentifier = splitFullMethodName(item)
        baseMethodFeature = findMethod2(basePackageDict, clazz,methodIdentifier, intersecSet, useReplace=True)

        item2 = accessmentList2[idx]
        clazz, methodName, params, methodIdentifier = splitFullMethodName(item2)
        targetMethodFeature = findMethod2(tarPackageDict, clazz,methodIdentifier, intersecSet, useReplace=True)
        partitionR1, partitionR2, partitionR3, rT=calFeatureSimilarity(baseMethodFeature,targetMethodFeature,True)

        tmpList.append('{}\t{}\t{}\t{}\t{}'.format(item,round(partitionR1,3),round(partitionR2,3),round(partitionR3,3),round(rT,3)))
        idx+=1
    return tmpList

### 实际的高效的方法列表全局搜索匹配算法
def doEvaluation(basePackageDict,filteredMethodList,tarPackageDict,intersecSet,useReplace=True):
    '''
    输入：
        basePackageDict：需要匹配的方法所在的app包
        filteredMethodList 需要进行特征匹配的方法签名序列
        tarPackageDict：特征向量键值对
    输出：
        每一个方法topN匹配结果，resDict
    对列表中的所有方法进行全app内方法匹配 全包一共有30万方法，100个方法进行匹配的时间大概是1h，2700个方法要27h
    注意tarPackageDict是cache过的特征dict
    '''
    resDict = {}
    for item in filteredMethodList:
        resDict[item] = {}
        ##求特征
        clazz, _, _, methodIdentifier = splitFullMethodName(item)
        baseMethodFeature = findMethod2(basePackageDict, clazz,methodIdentifier, intersecSet, useReplace=True)
        resDict[item]['Feature'] = baseMethodFeature
    traverseClazzMethod3(tarPackageDict,resDict,intersecSet,useReplace)
    return resDict
##现在的情况是大概有60%的函数能够精确地被找到，那么这些函数怎么办呢 首先把它们的混淆都收集起来
##混淆收集起来对混淆进行还原

### 0 字符串 容器 低级算法接口
### 1 查询字段 不做任何筛选等操作 包含统计信息 或者做一下筛选
### 2 查询字典，筛选并且计算新字段
### 3 匹配算法

### 首先为了加快寻找过程 我需要进行全局的字符串匹配

# getClazzConstStr(packageDict,clazz)




