#coding=utf-8
import os
import sys
from . import StrOp
from . import QueryOp
pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
ppwd = os.path.dirname(ppwd)
sys.path.append(ppwd)
from modules import InteractUtils

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
        if StrOp.IsSysClazzOrDeObfuscated(item, DeObfuscatedClazzSet):
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
        if StrOp.IsSysClazzOrDeObfuscated(retType[0], DeObfuscatedClazzSet):
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
    if StrOp.IsSysClazzOrDeObfuscated(className, DeObfuscatedClazzSet):
        IsSysOrDeOb = True
    unifiedParams = []
    idx = 0
    for item in params:
        idx+=1
        if StrOp.IsSysClazzOrDeObfuscated(item, DeObfuscatedClazzSet):
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
        if StrOp.IsSysClazzOrDeObfuscated(retType[0], DeObfuscatedClazzSet):
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

    classDict = QueryOp.getClass(packageDict, className)
    if not classDict:
        return res

    methodIdentifier = methodName+params
    methodDict = QueryOp.getMethod(classDict,methodIdentifier)
    
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
    classDict = QueryOp.getClass(packageDict, className)
    if not classDict:
        return res
    methodDict = QueryOp.getMethod(classDict,methodSig)
    
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
    clazz, _, _, methodIdentifier = StrOp.splitFullMethodName(fullName)
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

### 特征包的抽取，形成键值对的形式,返回这些键值对
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

