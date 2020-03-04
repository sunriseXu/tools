#coding=utf-8
from . import StrOp
import os
import sys
pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
ppwd = os.path.dirname(ppwd)
sys.path.append(ppwd)
from modules import InteractUtils
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
    className, _, _, methodIdentifier = StrOp.splitFullMethodName(fullName)
    classDict = getClass(basePackageDict, className)
    res = ''
    if not classDict:
        return res
    methodDict = getMethod(classDict,methodIdentifier)
    callers = methodDict['caller']
    print(callers)

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
        if not StrOp.isCostomerClazz(clazz):
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
    methodDictList = classDict['methods']
    allConstStr = set()
    for methodIdentifier in methodDictList:
        methodDict = methodDictList[methodIdentifier]
        constStr = methodDict['constStr']
        allConstStr=allConstStr.union(set(constStr))
    # InteractUtils.showList(allConstStr)
    return allConstStr
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
