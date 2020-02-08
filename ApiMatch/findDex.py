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
def findMatchedPath(className,fileList):
    packages = className.split('.')
    res = []
    for file in fileList:
        catStr = '\\'.join(packages)+'.smali'
        if catStr in file:
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
    return (resPathList, myCacheFile)
def getInheritFromSmali(sPath):
    className = ""
    classModifier = ""
    superName = ""
    implementList = []
    fieldsDict = {}
    content = FileUtils.readFile(sPath)
    print("start to analyze {}".format(sPath))
    myRex = r'\.class(.*?)L(.*?);\n'
    res = RexUtils.rexFind(myRex,content)

    if len(res)>0:
        classModifier = res[0][0].strip()
        className = res[0][1].strip()
        className = '.'.join(className.split('/'))
        # print(classModifier,className)

    superRex = r'\.super.*?L(.*?);\n'
    res = RexUtils.rexFind(superRex,content)
    if len(res)>0:
        superName = res[0].strip()
        superName = '.'.join(superName.split('/'))
    
    implementRex = r'\.implements.*?L(.*?);\n'
    res = RexUtils.rexFind(implementRex, content)
    if len(res)>0:
        for item in res:
            implementList.append('.'.join(item.split('/')))
    importList = getImports(content)
    #todo 添加对类变量的处理
    staticFieldsDict, instanceFieldsDist = parseFields(content)
    fieldsDict['staticFields'] = staticFieldsDict
    fieldsDict['instanceFields'] = instanceFieldsDist
    # print(staticFieldsDict)
    # print(instanceFieldsDist)
    # input()
    methodsDict = parseMethods(content)
    # if 'z5\\\\a\\\\a.smali' in sPath:
    #     print(className,superName,implementList,implementList,fieldsDict,methodLists)
    return (className,sPath, classModifier, superName, implementList, importList, fieldsDict, methodsDict)

def getImports(content):
    importRex = r'(L[^(]*?;)'
    res = RexUtils.rexFind(importRex, content)
    res = set(res)
    res = [transClassName(i) for i in res if '\n' not in i]
    return res
    # input()

def parseFields(content):#一个变量包含修饰符，变量名，类型，初始值（如果是静态类型的话可能有）
    #处理每个类变量，返回两个字典，分别是static变量字典和instance变量字典，字典里面是表示每个变量的字典
    # 变量名:{修饰符：xxxx, 变量名：xxx，类型：xxx，初始值：xxx}
    # static fields 
    # instance fields
    staticFieldsDict = {}
    instanceFieldsDist = {}
    fieldRex = r'\.field .*?\n'
    res = RexUtils.rexFind(fieldRex, content)
    if res:
        for item in res:
            isStatic, fieldDict = parseField(item)
            if not fieldDict:
                return {},{}
            fieldName = fieldDict['name']
            if isStatic:
                staticFieldsDict[fieldName] = fieldDict
            else:
                instanceFieldsDist[fieldName] = fieldDict
    return staticFieldsDict, instanceFieldsDist

def parseField(fieldStr):
    fieldDict = {}
    fields = fieldStr.split('=')[0].strip().split()
    #如果有等于号，那么说明有初始值
    if len(fields)<2:
        print('field string is invalid0:{}'.format(fieldStr))
        input()
        return False,fieldDict
    initVal = ''
    nameAndType = ''
    modifier = []
    name = ''
    typeStr = ''
    #判断倒数第二个是'='
    if '=' in fieldStr:
        initVal = fieldStr.split('=')[1].strip()
        
    nameAndType = fields[-1].strip()
    modifier = fields[1:-1]
    if ':' in nameAndType:
        name = nameAndType.split(':')[0]
        typeStr = nameAndType.split(':')[1]
    else:
        print('field string is invalid1:{}'.format(fieldStr))
        input()
        return False, fieldDict
    typeStr = transClassName(typeStr)
    fieldDict['name'] = name
    fieldDict['modifier'] = modifier
    fieldDict['type'] = typeStr
    fieldDict['initVal'] = initVal
    # print("fieldstr:{} dict:{}".format(fieldStr,fieldDict))
    # input()
    if 'static' in modifier:
        return True,fieldDict
    else:
        return False,fieldDict



def parseMethods(content):
    methodsDict = {}
    methodRex = r'\.method .*?.end method'
    methodBodies = RexUtils.rexFind(methodRex, content)
    methodBodies = set(methodBodies)
    for methodBody in methodBodies:
        methodDict = {}
        modifier, mName, mParams, mRet = parseMethodHead(methodBody)
        if 'bridge' in modifier:
            #跳过桥接方法
            continue
        invokeLists,constStrList = parseMethodBody(methodBody)
        methodDict['modifier'] = modifier
        methodDict['methodName'] = mName
        methodDict['methodParams'] = mParams
        methodDict['retType'] = mRet
        methodDict['invoke'] = invokeLists
        methodDict['constStr'] = constStrList
        methodDict['caller'] = {}
        key = mName+list2Str(mParams)
        if key not in methodsDict:
            methodsDict[key] = methodDict
        else:#为什么会出现连个相同的方法呢？因为编译器会自动生成 synthetic 方法，对于这种情况，不能忽视
            #如果出现相同的方法，那应该是init方法，对于这种方法，如果有重复，那么我们选取非synthetic方法
            if '<init>' in mName and 'synthetic' in modifier:
                pass
            elif 'synthetic' not in modifier and 'synthetic' in methodsDict[key]['modifier']:#如果 synthetic 存在而且不是 init方法，那么可能是编译器生成的方法，应该存非 synthetic方法
                methodsDict[key] = methodDict
            else:
                print("multi method found:{} {}".format(modifier,key))
                # input()
    return methodsDict
    # input()
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
def parseMethodHead(content):
    #处理方法头部，返回方法的修饰符，方法名，参数类型 和 返回类型
    methodHeadRex = r'.method (.*?)\n'
    res = RexUtils.rexFind(methodHeadRex, content)
    if(len(res)==0):
        print("error, no method found!")
        return 
    resSplit = res[0].split()
    modifier = ' '.join(resSplit[0:-1])
    methodString = resSplit[-1].strip()
    mN,mParams,mRet = transMethod(methodString)#首先这个参数是列表，我需要将其转换成字符串形式：a(int,int,boolean)
    return modifier, mN, mParams, mRet

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

def parseMethodBody(content):
    #遍历方法中每一条指令，这里只识别conststring和invoke指令
    invokeLists = []
    constStrList = []
    instructions = content.split('\n')
    invokeRex = r'}, (.*?->.*?)$'
    count = 0
    for instr in instructions:
        invokeDict = {}
        if 'invoke-' in instr:
            invokeStr = RexUtils.rexFind(invokeRex, instr)
            # print(invokeStr)
            # input()
            invokeType = RexUtils.rexFind(r'invoke-(.*?) ', instr)
            if not invokeStr or not invokeType:
                print("error, no invoke found:{}".format(instr))
                input()
            else:
                count += 1
                invokeStr = invokeStr[0].strip()
                invokeType = invokeType[0].strip()
                className = invokeStr.split('->')[0]
                methodName = invokeStr.split('->')[1]
                className = transClassName(className)
                mN,mParams,mRet = transMethod(methodName)
                invokeDict['invokeType'] = invokeType
                invokeDict['className'] = className
                invokeDict['methodName'] = mN
                invokeDict['methodParams'] = mParams
                invokeDict['retType'] = mRet
                #生成key 需要生成key吗，好像不用
                # key = '{}.{}{}'.format(className, mN, list2Str(mParams))
                invokeLists.append(invokeDict)
                
        elif 'const-string' in instr:
            strRex = r'\"(.*?)\"'
            constStr = RexUtils.rexFind(strRex, instr)
            if constStr:
                constStrList.append(constStr[0])
                # print(constStrList)
                # input()
    return invokeLists, constStrList
                

def getInheritDict(pathList, outDictPath):
    idx = 0
    inheritDict = {}
    dictPath = outDictPath
    print("start to generate inherit dict")
    for sPath in pathList:
        idx += 1
        if idx%10000 == 0:
            FileUtils.writeDict(inheritDict, dictPath)
        sPathList = sPath.split('\\')
        sPath = '\\\\'.join(sPathList)
        if not sPath.endswith('.smali'):
            continue
        # print(sPath)
        # input()
        # if '\\\\android\\\\support' in sPath or '\\\\androidx\\\\' in sPath or \
        #     'com\\\\google\\\\' in sPath or 'com\\\\facebook\\\\' in sPath:
        #     continue
        # sPath = 'F:\\LINE_ALL_SMALI\\line-9-10-2\\smali_classes5\\jp\\naver\\b\\a\\b\\z.smali'
        clsName,clsPath, classModifier, supName, impList, importList,fieldsDict, methodLists = getInheritFromSmali(sPath)
        # print(clsName,clsPath,classModifier,supName,impList,importList,fieldsDict,methodLists)
        # input()
        if clsName not in inheritDict:
            inheritDict.update({clsName:{'clsPath':clsPath,'classModifier':classModifier,'super':supName,'implements':impList, 'imports':importList,'fields':fieldsDict,'methods':methodLists}})
        else:
            lastPath = inheritDict[clsName]['clsPath']
            print("duplicat clsName: {} {}".format(clsName,sPath))
            print("lastPath:{}".format(lastPath))
            input()
    FileUtils.writeDict(inheritDict, dictPath)
    print("done")
    return inheritDict
        



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="find dex!!")
    parser.add_argument('-n', '--classname', help='class name', nargs='?', default="") # ?-> 0个或多个参数 + ->1个或多个
    parser.add_argument('-d', '--dirname', nargs='+', help='dir name') #多个参数 默认放入list中 +表示至少一个 + 就放在list中
    parser.add_argument('-t', '--tmp', help='tmp dir', nargs='?',default="")
    parser.add_argument('-g', '--getdict', help='get all class dict', nargs='?',default="")
    args = parser.parse_args() 
    myDirs=args.dirname 
    className=args.classname
    cacheDir=args.tmp
    genDict = args.getdict


    print("className: "+className)
    print("dexDirs: "+str(myDirs))
    print("cacheDir: "+cacheDir)
    res,cacheFile = findDex(className,myDirs,cacheDir)
    InteractUtils.showList(res)
    if genDict:
        pathList = FileUtils.readList(cacheFile)
        getInheritDict(pathList,genDict)

    
