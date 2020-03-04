#coding=utf-8
from . import StrOp
from . import QueryOp
from . import CreationOp
from modules import InteractUtils

### 3 高层算法 即新的字段参与的计算
## 匹配核心方法 计算两个特征向量之间的距离
def calFeatureSimilarity(baseMethodFeature, targetMethodFeature, useDebug=False):
    '''
    计算两个特征之间的距离，分别是第一个特征和第二个特征，useDebug会打印计算的距离值
    '''
    baseMethodHeader = str(baseMethodFeature[0])
    baseConstList = str(StrOp.concatList(baseMethodFeature[1]))
    baseCallee = str(StrOp.concatList(baseMethodFeature[2]))
    baseSysOrDeCallee = str(StrOp.concatList(baseMethodFeature[3]))
    baseObfuscCallee = StrOp.concatList(baseMethodFeature[4])

    baseMethodHeaderLen = float(len(baseMethodHeader))
    baseCalleeLen = float(len(baseCallee))
    baseSysOrDeCalleeLen = float(len(baseSysOrDeCallee))
    baseObfuscCalleeLen = float(len(baseObfuscCallee))

    targetMethodHeader = str(targetMethodFeature[0])
    targetConstList = str(StrOp.concatList(targetMethodFeature[1]))
    targetCallee = str(StrOp.concatList(targetMethodFeature[2]))
    targetSysOrDeCallee = str(StrOp.concatList(targetMethodFeature[3]))
    targetObfuscCallee = StrOp.concatList(targetMethodFeature[4])

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
            partitionR3 = StrOp.jaccard_similarity(baseMethodFeature[1], targetMethodFeature[1])
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
            targetCalleeLen = QueryOp.getCalleeLen(methodDict)
            if targetCalleeLen>baseLen*low and targetCalleeLen<baseLen*high:
                targetMethodFeature = CreationOp.getMethodFeature(clazz, methodDict,intersecSet,useReplace)
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
        if not StrOp.isCostomerClazz(clazz):
            continue
        classDict = packageDict[clazz]
        methodDictList = classDict['methods']
        for methodIdentifer in methodDictList:
            idx +=1
            #取出这个类中的所有方法
            key = "{}.{}".format(clazz, methodIdentifer)
            methodDict = methodDictList[methodIdentifer]
            # 首先看这个
            targetCalleeLen = QueryOp.getCalleeLen(methodDict)
            for baseKey in baseMethodFeatureDict:
                cachedDict = baseMethodFeatureDict[baseKey]
                baseMethodFeature = cachedDict['Feature']
                
                baseLen = len(baseMethodFeature[2])+0.0
                if targetCalleeLen>baseLen*low and targetCalleeLen<baseLen*high:
                    targetMethodFeature = CreationOp.getMethodFeature(clazz, methodDict,intersecSet,useReplace)

                    r1,r2,r3,rT = calFeatureSimilarity(baseMethodFeature, targetMethodFeature)
                    # middleResDict[baseKey].update({key:rT})
                    StrOp.calTopN(cachedDict['topN'],N,(key,rT))
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
        clazz,_,_,_= StrOp.splitFullMethodName(fullName)
        if not StrOp.isCostomerClazz(clazz):
            continue
        targetMethodFeature = packageDict[fullName]
        targetCalleeLen = len(targetMethodFeature[2])
        
        
        for baseKey in baseMethodFeatureDict:
            cachedDict = baseMethodFeatureDict[baseKey]
            baseMethodFeature = cachedDict['Feature']
            
            baseLen = len(baseMethodFeature[2])+0.0
            if targetCalleeLen>baseLen*low and targetCalleeLen<baseLen*high:
                r1,r2,r3,rT = calFeatureSimilarity(baseMethodFeature, targetMethodFeature)
                
                StrOp.calTopMin(cachedDict['topN'],N,(fullName,rT))
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
    baseFeatureDict = CreationOp.getClazzMethodFeature(classDict, sameClazz,intersecSet,useReplace)

    targetClassDict = targetDict[sameClazz]
    targetFeatureDict = CreationOp.getClazzMethodFeature(targetClassDict, sameClazz,intersecSet,useReplace)
    resDict = {}
    for basekey in baseFeatureDict:
        baseFeature = baseFeatureDict[basekey]
        baseMethodHeader = baseFeature[0]
        baseConstList = StrOp.concatList(baseFeature[1])
        baseCallee = StrOp.concatList(baseFeature[2])
        baseSysOrDeCallee = StrOp.concatList(baseFeature[3])
        baseObfuscCallee = StrOp.concatList(baseFeature[4])

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
            targetConstList = StrOp.concatList(targetFeature[1])
            targetCallee = StrOp.concatList(targetFeature[2])
            targetSysOrDeCallee = StrOp.concatList(targetFeature[3])
            targetObfuscCallee = StrOp.concatList(targetFeature[4])
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
                    partitionR3 = StrOp.jaccard_similarity(baseFeature[1], targetFeature[1])
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
    clazz, _, _, methodIdentifier = StrOp.splitFullMethodName(fullName)
    baseMethodFeature = CreationOp.findMethod2(basePackageDict, clazz,methodIdentifier, intersecSet, useReplace)
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
    clazz, _, _, methodIdentifier = StrOp.splitFullMethodName(fullName)
    baseMethodFeature = CreationOp.findMethod2(basePackageDict, clazz,methodIdentifier, intersecSet, useReplace)

    clazz2, _, _, methodIdentifier2 = StrOp.splitFullMethodName(fullName2)
    targetMethodFeature = CreationOp.findMethod2(tarPackageDict, clazz2,methodIdentifier2, intersecSet, useReplace)
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
        clazz, methodName, params, methodIdentifier = StrOp.splitFullMethodName(item)
        baseMethodFeature = CreationOp.findMethod2(basePackageDict, clazz,methodIdentifier, intersecSet, useReplace=True)

        item2 = accessmentList2[idx]
        clazz, methodName, params, methodIdentifier = StrOp.splitFullMethodName(item2)
        targetMethodFeature = CreationOp.findMethod2(tarPackageDict, clazz,methodIdentifier, intersecSet, useReplace=True)
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
        clazz, _, _, methodIdentifier = StrOp.splitFullMethodName(item)
        baseMethodFeature = CreationOp.findMethod2(basePackageDict, clazz,methodIdentifier, intersecSet, useReplace=True)
        resDict[item]['Feature'] = baseMethodFeature
    traverseClazzMethod3(tarPackageDict,resDict,intersecSet,useReplace)
    return resDict
##现在的情况是大概有60%的函数能够精确地被找到，那么这些函数怎么办呢 首先把它们的混淆都收集起来
##混淆收集起来对混淆进行还原

### 收集一个类所有的常量字符串 在另一个包中全局搜索
def calClazzConstStrSimilarity(basePackageDict, baseClazz, targetPackageDict,topN, debug=False):
    N = topN
    baseStrList = QueryOp.getClazzConstStr(basePackageDict, baseClazz)
    if not baseStrList:
        print('base class const str is null')
        return []
    resDict = []
    for i in range(N+1):
        resDict.append(('',0))
    for targetClass in targetPackageDict:
        classDict = targetPackageDict[targetClass]
        targetStrList = QueryOp.getClazzConstStr(targetPackageDict, targetClass)
        if not targetStrList:
            continue
        strSimi = StrOp.myjaccard_similarity(baseStrList, targetStrList)
        StrOp.calTopMax(resDict, N, (targetClass, strSimi))
        if debug:
            print('{} {}'.format(strSimi, targetClass))
    return resDict