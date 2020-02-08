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


def findConstStr(packageDict,str):
    for clazz in packageDict:
        classDict = packageDict[clazz]
        methodDictList = classDict['methods']
        for methodIdentifer in methodDictList:
            methodDict = methodDictList[methodIdentifer]
            constStr = methodDict['constStr']
            for item in constStr:
                if str in item:
                    # print('found match constStr:{}'.format(methodDict))
                    pretyPrintMethodDict(clazz, methodDict)
                    break
def findMethod(packageDict,className, methodName):
    className = className.strip()
    methodName = methodName.strip()
    classDict = packageDict[className]
    methodDictList = classDict['methods']
    for methodIdentifer in methodDictList:
        methodDict = methodDictList[methodIdentifer]
        metName = methodDict['methodName']
        if metName in methodName:
            # finally we found matched methodDict, now it is time to prety print
            # print("match method dict:{}".format(methodDict))
            res = pretyPrintMethodDict(className, methodDict)
            print(res)
def findClass(packageDict, className):
    className = className.strip()
    classDict = packageDict[className]
    return classDict
def pretyPrintMethodDict(className, methodDict):
    modifier = methodDict['modifier']
    methodName = methodDict['methodName']
    params = methodDict['methodParams']
    callers = methodDict['caller']
    paramsStr = ''
    if params:
        paramsStr = ', '.join(params)
    retType = methodDict['retType']
    retStr = ''
    if retType:
        retStr = retType[0]
    invokeList = methodDict['invoke']
    constStrList = methodDict['constStr']
    methodHead = 'method: {} {} {}.{}({})'.format(modifier,retStr,className,methodName,paramsStr)
    methodConstStr = 'constStr: {}'.format(constStrList)
    # start print
    resStr = '{}\n{}\n'.format(methodHead,methodConstStr)
    # print('{}'.format(methodHead))
    # print('\t{}'.format(methodConstStr))
    for invokeDict in invokeList:
        invokeStr = pretyPrintInvoke(invokeDict)
        resStr += '{}\n'.format(invokeStr)
        # print('\t\t{}'.format(invokeStr))
    resStr += 'caller:{}'.format(callers)
    # print('caller:{}'.format(callers))
    return resStr

def pretyPrintInvoke(invokeDict):
    invokeType = invokeDict['invokeType']
    className = invokeDict['className']
    methodName = invokeDict['methodName']
    params = invokeDict['methodParams']
    paramsStr = ''
    if params:
        paramsStr = ', '.join(params)
    retType = invokeDict['retType']
    retStr = ''
    if retType:
        retStr = retType[0]
    invokeStr = '{} {} {}.{}({})'.format(invokeType,retStr, className[0],methodName,paramsStr)
    return invokeStr
def GetMethod(packageDict, className, methodDict):
    classDict = findClass(packageDict, className)
    modifier = methodDict['modifier']
    methodName = methodDict['methodName']
    params = methodDict['methodParams']
    retType = methodDict['retType']
    retStr = ''
    if retType:
        retStr = retType[0]
    invokeList = methodDict['invoke']
    constStrList = methodDict['constStr']
    #caller需要提前计算好，然后存起来避免再次计算，因为需要耗费大量时间，这个特征需要放在methodDict中，遍历所有方法
    methodNode = Method(modifier,methodName,params,retStr,constStrList,classDict,invokeList,callers)

def cmpList(alist, blist):
    sortedA = sorted(alist)
    sortedB = sorted(blist)
    equals = True
    if len(alist) != len(blist):
        return False
    for i in range(len(alist)):
        if sortedA[i] != sortedB[i]:
            equals = False
            break
    return equals
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
    # FileUtils.writeDict(packageDict,newDictPath)
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
def GenCallers(packageDict,androidCallerDict):
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
                    # print("{} {}".format(iclassName,invokeKey))
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
    FileUtils.writeList(exceptInfoList,"C:\\Users\\limin\\Desktop\\tmp\\error.txt")
    # print("notfound:{}".format(notfoundList))
    FileUtils.writeList(notfoundList,"C:\\Users\\limin\\Desktop\\tmp\\notfound.txt")
    print("{}".format(notfoundSet))
    print("foundcount:{} notfoundcount:{} foundinChild:{}".format(foundcount,notfoundcount,foundinChild))
    print("classcount:{}".format(len(packageDict)))
    print("methodcount:{}".format(methodCount))
    print("androidapiCallcount:{}".format(androidapiCallcount))
    FileUtils.writeDict(androidCallerDict,"C:\\Users\\limin\\Desktop\\tmp\\testAndroid.json")
def traverseMethod(packageDict, iclassName, imethodName, iparams):
    # if iclassName not in packageDict:
    #     #如果父类不在字典中，说明回溯已经到头了 返回
    #     print('no super class found! back')
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
    # for cmethodDict in cclassmethodList:
    #     cmetName = cmethodDict['methodName']
    #     cparams = cmethodDict['methodParams']
    #     if cmetName == imethodName and cmpList(cparams,iparams):
    #         print("found: {} {} {}".format(iclassName,cmetName,cparams))
    #         foundFlag = True
    #         # input()
    #         return foundFlag
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
    # input()
def traverseClazzMethod(packageDict,baseStr):
    a = 0.6
    low = 1-a
    high = 1+a
    resDict = {}
    sortedList = []
    baseLen = len(baseStr)+0.0
    #取出每一个类
    idx = 0
    for clazz in packageDict:
        classDict = packageDict[clazz]
        cPath = classDict['clsPath']
        methodDictList = classDict['methods']
        # methodCount += len(methodDictList)
        for methodIdentifer in methodDictList:
            idx +=1
            #取出这个类中的所有方法
            key = "{}.{}".format(clazz, methodIdentifer)
            methodDict = methodDictList[methodIdentifer]
            modifier = methodDict['modifier']
            methodName = methodDict['methodName']
            params = methodDict['methodParams']
            retType = methodDict['retType']
            invokeList = methodDict['invoke']
            callerKey = '{}{}'.format(methodName,list2Str(params))
            resStr = pretyPrintMethodDict(clazz, methodDict)
            if len(resStr)>baseLen*low and len(resStr)<baseLen*high:
                dist = Levenshtein.distance(baseStr,resStr)
                partition = dist/baseLen
                resDict.update({key:partition})
                print(idx)
                print(partition)
    sortedList = sorted(resDict.items(), key=lambda x:x[1])
    FileUtils.writeList(sortedList,"alltmp2.txt")
import Levenshtein
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="find dex!!")
    parser.add_argument('-d', '--dictpath', nargs='?',default="") #多个参数 默认放入list中 +表示至少一个 + 就放在list中
    parser.add_argument('-t', '--tmp', help='tmp dir', nargs='?',default="")
    parser.add_argument('-g', '--getdict', help='get all class dict', nargs='?',default="")
    args = parser.parse_args() 
    myDictPath=args.dictpath
    
    packageDict = FileUtils.readDict(myDictPath)
    className = 'jp.naver.line.android.am.a.d' #j.a.a.a.b2.e.h jp.naver.line.android.obs.net.s
    methodName = 'a'
    tmp1 = FileUtils.readFile('tmp2.txt')
    traverseClazzMethod(packageDict,tmp1)
    # findMethod(packageDict,className,methodName)
    # findConstStr(packageDict,"X-Line-Access")
    # findClass(packageDict,className)
    # androidCallerDict = {}
    # GenCallers(packageDict,androidCallerDict)
    # FileUtils.writeDict(packageDict,"C:\\Users\\limin\\Desktop\\tmp\\line-9-22-2-addCaller.json")
    # FileUtils.writeDict(androidCallerDict,"C:\\Users\\limin\\Desktop\\tmp\\line-9-22-2-androidCallerDict.json")
    # print(packageDict['okhttp3.internal.platform.Platform'])
    # GenInherit(packageDict,'')
    # for clazz in packageDict:
    #     classDict = packageDict[clazz]
        # if 'childClass' in classDict:
        #     childClass = classDict['childClass']
        #     print('classname:{} childclass:{}'.format(clazz, childClass))
        #     input()
        # methodDicts = classDict['methods']
        # for key in methodDicts:
        #     methodDict = methodDicts[key]
        #     callers = methodDict['caller']
        #     if callers:
        #         # print("caller:{} callee:{}".format(callers,clazz+'.'+key))
        #         for cc in callers:
        #             value = callers[cc]
        #             for i,j in value.items():
        #                 if 'child' in j:
                            # print(i,j)
                            # input()
                

    # clzDict = packageDict['c.a']
    # super = clzDict['super']
    # implist = clzDict['implements']
    # print("{} {}".format(super, implist))
    
    # tmp2 = FileUtils.readFile('tmp3.txt')

    # dist=Levenshtein.distance(tmp2,tmp1)
    # print("levendist:{} tmp1:{} tmp2:{}".format(dist,len(tmp1),len(tmp2)))
    
