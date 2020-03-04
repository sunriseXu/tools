#coding=utf-8
import os
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
def calTopMin(myList,N,newElem):
    for idx in range(0,N):
        if newElem[1]<myList[idx][1]:
            myInsert(myList,idx,newElem,N)
            break
def calTopMax(myList,N,newElem):
    for idx in range(0,N):
        if newElem[1]>myList[idx][1]:
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


### 修改后的jaccard算法 分母为基础的list 而非并集
def myjaccard_similarity(list1, list2):
    s1 = set(list1)
    s2 = set(list2)
    if len(s1.union(s2)) == 0:
        return 1.0
    return len(s1.intersection(s2)) / len(s1)
