#coding=utf-8
import argparse
import os
import sys
pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)
from modules import FileUtils
from modules import InteractUtils
from modules import RexUtils
def transMethod(methodString):
    #处理方法定义，返回方法名，参数类型 和 返回类型
    methodName = methodString.split('(')[0]
    # start to parse param
    paramRex = r'\((.*?)\)'
    params = RexUtils.rexFind(paramRex,methodString)[0].strip()
    paramTypeArr = []
    if params:
        paramsArr = params.split(';')
        if len(paramsArr)>1:
            for i in range(0,len(paramsArr)):
                if i < len(paramsArr)-1:
                    paramsArr[i] = paramsArr[i]+';'
        paramsArr = [i for i in paramsArr if i]
        for item in paramsArr:
            paramTypeArr.extend(transClassName(item))
    # parse param done! start to parse return type
    returnType = methodString.split(')')[-1].strip()
    returnType = transClassName(returnType)
    return methodName, paramTypeArr, returnType
        

def transClassName(name):
    #处理L开头的类型字符串，返回程序员可读的类型字符串
    paramTypes = []
    arrayFlag = False
    arrayCount = 0
    for i in name:
        if '[' in i:
            arrayCount+=1
            arrayFlag = True
            continue
        if 'L' in i:
            break
        tmp = parseBaseType(i)
        if arrayFlag:
            tmp = tmp+'[]'*arrayCount
        paramTypes.append(tmp)
        arrayCount = 0
        arrayFlag = False
    
    cRex = r'L(.*?);'
    res = RexUtils.rexFind(cRex,name.strip())
    if not res:
        return paramTypes
    res = res[0]
    tmp = '.'.join(res.split('/'))
    if arrayFlag:
        tmp = tmp + '[]'
    paramTypes.append(tmp)
    return paramTypes

def parseBaseType(name):
    #对基本类型字符串进行识别，返回可读的基本类型字符串表示
    name = name.strip()
    if name in 'V':
        return 'void'
    elif name in 'Z':
        return 'boolean'
    elif name in 'B':
        return 'byte'
    elif name in 'S':
        return 'short'
    elif name in 'C':
        return 'char'
    elif name in 'I':
        return 'int'
    elif name in 'J':
        return 'long'
    elif name in 'F':
        return 'float'
    elif name in 'D':
        return 'double'
    else: 
        return name

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
def isSysType(className, sysTypeList):
    # strip []
    className = className.split('[')[0]
    if className in sysTypeList or className.startswith('java.'):
        return True
    else:
        return False
def queryOri(classDict, obfusClass):
    if '[' in obfusClass:
        return ''
    for oriClass in classDict:
        detailDict = classDict[oriClass]
        obfuscateClass = detailDict['mapClass']
        if obfuscateClass == obfusClass:
            return oriClass
    return ""
def queryOriMethod(classDict, tarfuscateClass, obfuscateMethod, paramStr):
    # print(tarfuscateClass, obfuscateMethod, paramStr)
    # input()
    for originClass in classDict:
        detailDict = classDict[originClass]
        obfuscateClass = detailDict['mapClass']
        # print(obfuscateClass)
        if obfuscateClass == tarfuscateClass:
            # print("found")
            methodDict = detailDict['mapMethod']
            for oriMethod in methodDict:
                obMethod = methodDict[oriMethod]
                if obMethod == obfuscateMethod:
                    if paramStr in oriMethod:
                        return originClass, oriMethod

    return "",""
def checkType(retClass, sysTypeList, classDict):
    if isBasicType(retClass):
        return retClass
    elif isSysType(retClass,sysTypeList):
        return retClass
    elif queryOri(classDict, retClass):
        return queryOri(classDict, retClass)
    else:
        print(retClass)
        print("not found")
        input()
        return ""
if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="find dex!!")
    parser.add_argument('-p', '--mappath', help='map path', nargs='?', default="") # ?-> 0个或多个参数 + ->1个或多个
    parser.add_argument('-f', '--filterpath', help='map path', nargs='?', default="") # ?-> 0个或多个参数 + ->1个或多个

    args = parser.parse_args() 
    mapPath=args.mappath 
    obfuscPath = args.filterpath
    
    with open('android_class_names_api_27.txt','r') as file:
        sysTypeList = file.readlines()
    sysTypeList = [transClassName(i)[0] for i in sysTypeList]
    # print(sysTypeList)
    with open(mapPath,'r') as file:
        mapLines = file.readlines()
    classDict = {}
    originClass = ''
    jump = False
    for line in mapLines:
        first = line[0]
        first = first.strip()
        
        # print(line)
        if first:
            # is a class
            jump = False
            originClass = line.split('->')[0].strip()
            obfuscateClass = line.split('->')[1].split(':')[0].strip()
            if originClass == obfuscateClass or 'android.support' in originClass:
                jump = True
                continue
            #人要多么强大才不会受伤？
            detailDict = {}
            detailDict['mapClass'] = obfuscateClass
            detailDict['mapMethod'] = {}
            classDict[originClass] = detailDict
        else:
            if jump:
                continue
            if '(' in line and ')' in line:
                originMethod = line.split('->')[0].strip().split()[-1]
                obfuscateMethod = line.split('->')[1].strip()
                if 'init' in obfuscateMethod:
                    continue
                # print(originClass)
                classDict[originClass]['mapMethod'][originMethod] = obfuscateMethod
    
    fullMap = []
    for oriClass in classDict:
        detailDict = classDict[oriClass]
        obfuscateClass = detailDict['mapClass']
        methodDict = detailDict['mapMethod']
        if not methodDict:
            continue
        for originMethod in methodDict:
            obfuscateMethod = methodDict[originMethod]
            originFullMethod = '{}.{}'.format(oriClass, originMethod)
            obfuscateFullMethod = '{}.{}'.format(obfuscateClass, obfuscateMethod)
            fullMap.append((obfuscateFullMethod,originFullMethod))
    finalMapping = []
    # InteractUtils.showList(fullMap)
    with open(obfuscPath,'r') as file:
        obfuscList = file.readlines()
    for item in obfuscList:
        # print(item)
        className = item.split('->')[0]
        methodString = item.split('->')[1]
        className = transClassName(className)
        mN, mP, mR = transMethod(methodString)
        className = className[0]
        methodName = mN[0]
        parms = '('+','.join(mP)+')'
        retClass = mR[0]
        # print(retClass)
        oriParmArr = []
        for jtem in mP:
            oriClass = checkType(jtem, sysTypeList, classDict)
            oriParmArr.append(oriClass)
        oriParmStr = '('+','.join(oriParmArr)+')'
        
        oriClassName, oriMethoName = queryOriMethod(classDict,className, methodName, oriParmStr)
        if not oriClassName:
            print("not found")  
        oriSig = '{}.{}'.format(oriClassName, oriMethoName)
        obfSig = '{}.{}'.format(className, methodName+parms)
        finalMapping.append('{} {}'.format(obfSig,oriSig))
    FileUtils.writeList(finalMapping, "finalMapping.txt")        
        

        
            