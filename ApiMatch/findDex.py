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
import platform
import argparse 

archTec = platform.architecture()
def findMatchedPath(className,fileList):
    packages = className.split('.')
    res = []
    if 'WindowsPE' in archTec:
        splitStr = '\\'
    else:
        splitStr = '/'
    for file in fileList:
        catStr = splitStr.join(packages)+'.smali'
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
        # if idx%10000 == 0:
        #     FileUtils.writeDict(inheritDict, dictPath)
        if 'WindowsPE' in archTec:
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
    # FileUtils.writeDict(inheritDict, dictPath)
    print("done")
    return inheritDict
def traverseMethod(packageDict, iclassName, imethodName, iparams):
    ## invoke的函数如果在整个包中找到则返回其函数签名
    callerclassDict = packageDict[iclassName]
    cclassmethodDictList = callerclassDict['methods']
    superClass = callerclassDict['super']
    implementList = callerclassDict['implements']
    impList = []
    impList.extend(implementList)
    if superClass:
    #将接口和父类合在一起
        impList.append(superClass)
    
    foundFlag = False
    invokeKey = '{}{}'.format(imethodName,list2Str(iparams))
    
    if invokeKey in cclassmethodDictList:
        foundFlag = True
        print("found in super class:{} {}".format(iclassName,invokeKey))
        return (foundFlag, iclassName, invokeKey)

    if not foundFlag:
        #由于invoke-virtual 的关系，导致无法确定具体的对象类，所以需要在父类或者子类中找
        #首先在子类中找，但是子类可能很多，导致无法确定具体的子类，怎么办？
        #总之尝试在子类中找吧，但是遍历所有来来找子类是不可能的，只能生成
        #super 和 implement字段找到父类或者接口，然后在父类或者接口中添加字段
        #一直super回溯搜索好了
        for sup in impList:
            if sup not in packageDict:
                #这里需要筛选出java/android api
                continue
            tmp,retClazz, retKey = traverseMethod(packageDict, sup, imethodName, iparams)
            if tmp:
                return (tmp, retClazz, retKey)
    return (False,"","")        
def GenCallers(packageDict):
    androidCallerDict={}
    #遍历每一个方法，根据这个方法再计算对其的交叉引用，这个计算过程是巨大的假设有10 0000个方法，每个方
    #法需要遍历10 0000次，所以时间复杂度 是 10^10， 而我的电脑是2.5GHz 每秒2.5*10^9时钟周期，一次遍历需要5s，
    #那么一共需要多少秒呢？5*10^5 = 500000s = 13h 不可能缓存的好吧 只能用服务器的机器来跑，但是可以这样来减少
    #计算时间，那就是在每次正向计算的时候存下调用自己的方法不久行了吗，可以的，就这样算
    #所以遍历每个方法的invoke函数，每个invoke函数记录下自己的caller，问题来了，需要记录安卓函数的父类吗
    #感觉是可以的，相当于我自己在计算callgraph，java中有多态的invoke吗
    #那么对象也存在交叉引用啊，这涉及到数据流怎么构建的问题了，总之 这个dict需要不断地更新，所以按道理只要遍历一次
    #那么是否需要用额外的数据结构来存储callgraph，有必要,需要标记这个调用的属性，即direct / virtual
    #那么这个数据结构怎么表示呢？ classname:{methodnameA:{direct:[{classname:methodname},pb],virtual:[va,vb]},methodnameB:{}}
    #想了一下，还是觉得没有必要新建数据结构，直接增加到原来的字典中
    #新的问题出现了 
    exceptInfoList = []
    notfoundList = []
    foundcount = 0
    notfoundcount = 0
    notfoundSet = {}
    methodCount = 0
    androidapiCallcount=0
    foundinChild = 0
    #取出每一个类
    for clazz in packageDict:
        classDict = packageDict[clazz]
        cPath = classDict['clsPath']
        methodDictList = classDict['methods']
        methodCount += len(methodDictList)
        for methodIdentifer in methodDictList:
            #取出这个类中的所有方法
            methodDict = methodDictList[methodIdentifer]
            modifier = methodDict['modifier']
            methodName = methodDict['methodName']
            params = methodDict['methodParams']
            retType = methodDict['retType']
            invokeList = methodDict['invoke']
            callerKey = '{}{}'.format(methodName,list2Str(params))
            #对这个方法中的所有函数调用进行遍历
            for invokeDict in invokeList:
                invokeType = invokeDict['invokeType']
                iclassName = invokeDict['className'][0]
                # 如果调用的是java/android方法，那么跳过
                # 获取这个方法的指纹信息
                imethodName = invokeDict['methodName']
                iparams = invokeDict['methodParams']
                invokeKey = '{}{}'.format(imethodName,list2Str(iparams))
                #开始找caller
                # try: 
                if iclassName.startswith('java.') or iclassName.startswith('android.') \
                    or iclassName.startswith('androidx.') \
                        or iclassName.startswith('javax.') or 'dalvik' in iclassName:#'dalvik.system.DexClassLoader com.linecorp.linepay.biz.googlepay.a' 'com.samsung.android.sep.camera.SemCameraCaptureProcessor$CaptureParameter'
                    androidapiCallcount+=1
                    #这个点的调用占用到了一半以上，这是图的sink，所以很重要可以从这里开始分析
                    # print("{}.{}".format(iclassName,invokeKey))
                    # input() #这里需要对android/java api进行caller字典生成，暂时生成一个新的字典存放
                    # {classname:{methods:{methodkey:{caller:{cclazzname:{cmethod:invoketype}}}}}}
                    if iclassName not in androidCallerDict:
                        androidCallerDict[iclassName]= {'methods':{invokeKey:{'caller':{clazz:{callerKey:invokeType}}}}}
                    else:
                        if 'methods' not in androidCallerDict[iclassName]:
                            androidCallerDict[iclassName]['methods']= {invokeKey:{'caller':{clazz:{callerKey:invokeType}}}}
                        else:
                            if invokeKey not in androidCallerDict[iclassName]['methods']:
                                androidCallerDict[iclassName]['methods'][invokeKey] = {'caller':{clazz:{callerKey:invokeType}}}
                            else:
                                if clazz not in androidCallerDict[iclassName]['methods'][invokeKey]['caller']:
                                    androidCallerDict[iclassName]['methods'][invokeKey]['caller'][clazz] = {callerKey:invokeType}
                                else:
                                    androidCallerDict[iclassName]['methods'][invokeKey]['caller'][clazz].update({callerKey:invokeType})
                    
                    continue
                if iclassName not in packageDict: # 包含[] 数组方法
                    continue                 
                # 获取invoke方法的类，尝试找到这个invoke方法
                callerclassDict = packageDict[iclassName]
                #这个类找不到的原因有： 这个类是数组
                cclassmethodDictList = callerclassDict['methods']
                #获取这个类的父类，接口等
                foundFlag = False
                if invokeKey in cclassmethodDictList:
                    foundcount += 1
                    foundFlag = True
                    cmethodDict = cclassmethodDictList[invokeKey]
                    callerDict = cmethodDict['caller']
                    #添加caller信息
                    if clazz in callerDict:
                        cclazzDict = callerDict[clazz]
                        cclazzDict.update({callerKey:invokeType})
                    else:
                        callerDict[clazz] = {callerKey:invokeType}
                        #这里我们找到了直接调用的方法，为了构建callgraph，并且便于索引，需要在目标方法中添加caller字段
                        # caller字段是一个dict {invoke-type:类名，现在最恶心的是，方法是一个list，不能够直接索引}
                        # 明天要重构字典，修改所有方法为字典访问，键是什么呢？方法名+参数 可行！
                        # 重构完成后需要抛出一个dict大概需要1个小时
                        # 跑完后需要重新修改所有方法的访问，改成以字典访问
                        # 最后构建每个方法字典的caller字段
                        # caller字段构建后，应该可以完成大部分callgraph的生成，
                        # 打印某些方法的callgraph进行验证，注意需要处理android/java方法的callgraph
                        # 然后是匹配，匹配是最难处理的一步，callgraph上每个节点都是一个方法，匹配需要方法的指纹，然后再说整个图的匹配
                        # 这里需要用到图的匹配算法，所以需要进行调研
                        # 调用完成后实现算法的匹配，说实话，这里不能保证可用
                        # 完成这些需要大概一周的时间
                        # break
                if not foundFlag:
                    #由于invoke-virtual 的关系，导致无法确定具体的对象类，所以需要在父类或者子类中找
                    #首先在子类中找，但是子类可能很多，导致无法确定具体的子类，怎么办？
                    #总之尝试在子类中找吧，但是遍历所有来来找子类是不可能的，只能生成
                    #super 和 implement字段找到父类或者接口，然后在父类或者接口中添加字段
                    #一直super回溯搜索好了 如果这个方法死活找不到，有两种可能性
                    #
                    superClass = callerclassDict['super']
                    implementList = callerclassDict['implements']
                    impList = []
                    impList.extend(implementList)
                    if superClass:
                    #将接口和父类合在一起
                        impList.append(superClass)
                    notfoundList.append("{} {} {} {} {} {}".format(iclassName,imethodName,iparams,clazz,methodName,cPath))
                    print("current cls not found:\n\tclassName:{} methodName:{}({}) location: {}.{} {}".format(iclassName,imethodName,iparams,clazz,methodName,cPath))
                    #遍历父类，在父类方法中匹配
                    # print(implementList)
                    foundFlag = False
                    for sup in impList:
                        print("try super:{}".format(sup))
                        if sup not in packageDict:
                            continue
                        tmp, retClazz, retKey = traverseMethod(packageDict, sup, imethodName, iparams)
                        if tmp:
                            foundcount+=1
                            foundFlag = True
                            foundinChild +=1
                            callerDict = packageDict[retClazz]['methods'][retKey]['caller']
                            #添加caller信息
                            if clazz in callerDict:
                                cclazzDict = callerDict[clazz]
                                cclazzDict.update({callerKey:invokeType+'-child'})
                            else:
                                callerDict[clazz] = {callerKey:invokeType+'-child'}
                            break
                    if not foundFlag:
                        notfoundcount+=1
                        # notfoundSet.add(imethodName)
                        if imethodName in notfoundSet:
                            notfoundSet[imethodName] += 1
                        else:
                            notfoundSet[imethodName] = 0
                        print("not found method")
                        # input()
                    else:
                        ## todo 这里我们找到了invoke的父类方法，这里的方法是父类方法
                        pass
                # input()
                # except KeyError as err:
                #     exceptInfoList.append('{}'.format(err))
                #     pass
                        # input()
    # print("error:{}".format(exceptInfoList))
    FileUtils.writeList(exceptInfoList,"./error.txt")
    # print("notfound:{}".format(notfoundList))
    FileUtils.writeList(notfoundList,"./notfound.txt")
    print("{}".format(notfoundSet))
    print("foundcount:{} notfoundcount:{} foundinChild:{}".format(foundcount,notfoundcount,foundinChild))
    print("classcount:{}".format(len(packageDict)))
    print("methodcount:{}".format(methodCount))
    print("androidapiCallcount:{}".format(androidapiCallcount))
    # FileUtils.writeDict(androidCallerDict,'./androidcaller.json')
    # FileUtils.writeDict(packageDict,callerPath)
    return packageDict, androidCallerDict
def GenInherit(packageDict,newDictPath):
    for clazz in packageDict:
        classDict = packageDict[clazz]
        superCls = classDict['super']
        implementList = classDict['implements']
        if superCls and not superCls.startswith('java.') and not superCls.startswith('android.')\
            and not superCls.startswith('androidx.') and not superCls.startswith('org.')\
                and not superCls.startswith('javax.') and not superCls.startswith('com.google.')\
                and not superCls.startswith('com.samsung.')\
                    and not superCls.startswith('com.facebook.') and not superCls.startswith('dalvik.system'):
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
                            and not impl.startswith('com.facebook.' ) and not impl.startswith('com.samsung' ):#'jp.naver.line.android.b.e$d'
                    superClsDict = packageDict[impl] #接口字典
                    if 'childClass' in superClsDict:
                        superClsDict['childClass'].append(clazz)
                    else:
                        superClsDict.update({'childClass':[clazz]})
    FileUtils.writeDict(packageDict, newDictPath)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="find dex!!")
    parser.add_argument('-n', '--classname', help='class name', nargs='?', default="") # ?-> 0个或多个参数 + ->1个或多个
    parser.add_argument('-d', '--dirname', nargs='+', help='dir name') #多个参数 默认放入list中 +表示至少一个 + 就放在list中
    parser.add_argument('-t', '--tmp', help='tmp dir', nargs='?',default="")
    parser.add_argument('-g', '--getdict', help='get all class dict', nargs='?',default="")
    # parser.add_argument('-c', '--getcaller', help='get all class dict', nargs='?',default="")

    args = parser.parse_args() 
    myDirs=args.dirname 
    className=args.classname
    cacheDir=args.tmp
    genDict = args.getdict
    # callerDictPath = args.getcaller


    print("className: "+className)
    print("dexDirs: "+str(myDirs))
    print("cacheDir: "+cacheDir)
    res,cacheFile = findDex(className,myDirs,cacheDir)
    InteractUtils.showList(res)
        
    if genDict:
        pathList = FileUtils.readList(cacheFile)
        basePackageDict = getInheritDict(pathList,genDict)
        # basePackageDict = FileUtils.readDict(genDict)
        addcallerDict, _ = GenCallers(basePackageDict)
        GenInherit(addcallerDict, genDict)

    
