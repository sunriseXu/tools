#coding=utf-8
import os
import sys
import subprocess
import random
import logging
import argparse
import shutil
logging.basicConfig()

pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules import FileUtils
from modules import CollectionUtils
from modules.FileUtils import EasyDir
from modules import RexUtils


l = logging.getLogger("FileRoom")

def print_all(module_):
    modulelist = dir(module_)
    length = len(modulelist)
    for i in range(0,length,1):
        print(getattr(module_,modulelist[i]))

def randomCopy(srcDir,destDir,maxNum):
    '''
    randomly select maxNum files in srcDir, and copy them to destDir
    '''
    fileList = FileUtils.listDir(srcDir)
    randomList = random.sample(fileList, maxNum)
    FileUtils.mkdir(destDir)
    FileUtils.listCopy2(randomList,destDir)
    return

def ruleStatistic(filteredPath, debug=False):
    noRuleList=[]
    ruledList=[]
    if not os.path.exists(filteredPath):
        l.warning('filteredPath not exists!')
        return ruledList, noRuleList
    resultPath = filteredPath   
    content=FileUtils.readFile(resultPath)

    rex=r'-----------------.*?.txt.*?-----------------------'
    mylist=RexUtils.rexSplit(rex,content)

    mydict={}
    lognamerex=r'----------------- (.*?) -'
    Rulerex=r'(Rule.*?\d+)'
    count=0
    for item in mylist:
        rules= RexUtils.rexFind(Rulerex,item)
        rules=list(set(rules))
        logName=RexUtils.rexFind(lognamerex,item)
        logName=logName[0]
        logName = logName.split('.')[0]
        if len(rules) > 0:
            count+=1
            ruledList.append(logName)
            for rule in rules:
                CollectionUtils.appendDict(mydict,rule,logName)
        else:
            if logName not in noRuleList:
                noRuleList.append(logName)
    if debug:
        print('pass:{} / total:{}'.format(count,len(mylist)))
        mykeys=sorted(mydict.keys())
        for key in mykeys:
            print('rule: '+key+'log_count: '+len(mydict[key]))
    return ruledList, noRuleList

def filterFileContent(filePath, splitStr):
    '''
    filter every line in file content, with a splitStr, specific list
    '''
    allLines=[]
    with open(filePath) as f:
        allLines=f.readlines()
    resList=[]
    for line in allLines:
        filtered=''
        line = line.strip()
        if not line:
            continue
        line=line.split(splitStr)[1]
        filtered=line.strip().split()[0]
        resList.append(filtered)
    return resList
def statisticLists(myDict):
    '''
    staticstic frequency in list<list>, {'a':[1,2],'b':[2,3]}=>{1:[1,['a']],2:[2,['a','b']],3:[1,['b']]}
    '''
    resDict={}
    for key,value in myDict.items():
        uniqList = list(set(value))
        for item in uniqList:
            if item not in resDict.keys():
                resDict.update({item:[1,[key]]})
            else:
                resDict[item][0] += 1
                resDict[item][1].append(key)
    return resDict

def mergeAndWriteDict(srcPathList,destPath):
    mergedDict = {}
    if len(srcPathList) == 0:
        return mergedDict
    for srcPath in srcPathList:
        srcDict = FileUtils.readDict(srcPath)
        mergedDict = CollectionUtils.dictMerge(srcDict, mergedDict)
    FileUtils.writeDict(mergedDict, destPath)
    return mergedDict
def trimAllPrefix(srcDir):
    mylist = FileUtils.listDir2(srcDir)
    for i in mylist:
        if 'log_' not in i:
            continue
        srcpath=os.path.join(srcDir,i)
        ri = i.split('log_')[1]
        destpath=os.path.join(srcDir,ri)
        os.rename(srcpath,destpath)

def renamePkg2Hash(srcDir, destDir, apkInfoDictPath):
    '''
    rename all pkgname file in srcdir to hash name according to apkinfoDict
    copy renamed file to destdir
    usage egg:
    renamePkg2Hash('./srcdir','./destdir','./allMalDict.txt')
    such as: com.example.pkg.txt -> 123456789.txt
    '''
    fileList = FileUtils.listDir2(srcDir)
    fileList = CollectionUtils.trimListItem(fileList,'','.txt')
    fileList = [str(i) for i in fileList]
    apkInfoDict = FileUtils.readDict(apkInfoDictPath)
    newdict = {}
    typeRes = CollectionUtils.typeof(apkInfoDict.values()[0])
    flag = False
    if typeRes in 'list':
        flag = True
    for key, value in apkInfoDict.items():
        if key not in newdict.keys():
            if flag:
                newdict.update({key:value[0]})
            else:
                newdict.update({key:value})
    hashList = newdict.keys()
    hashList = [str(i) for i in hashList]
    FileUtils.mkdir(destDir)
    newdict = dict(zip(newdict.values(), newdict.keys()))
    for pkg in fileList:
        if pkg in hashList:
            myHash = pkg
        else:
            myHash = newdict[pkg]
        if not myHash:
            print('error!')
            continue 
        srcPath = os.path.join(srcDir, pkg+'.txt')
        destPath = os.path.join(destDir,myHash+'.txt')
        shutil.copy(srcPath, destPath)

def splitMalware(mergedList):
    '''
    描述：将总hashList分类成三类恶意样本的lists
    1. mydir 存放所有三类恶意样本的hash-pkgName字典文件，每类大概三千多个（不到四千）
    2. mydir固定为C:\\Users\\limin\\Desktop\\allHashDict\\allMalDict
    '''
    mydir = 'C:\\Users\\limin\\Desktop\\allHashDict\\allMalDict'
    #读取三类样本字典
    malDictDir = EasyDir(mydir)
    malDict = malDictDir.getAbsPathDict()
    payDict = FileUtils.readDict(malDict['payAllDict.txt'])
    rogDict = FileUtils.readDict(malDict['rogAllDict.txt'])
    stealDict = FileUtils.readDict(malDict['stealAllDict.txt'])

    payList = []
    rogList = []
    stealList = []
    noMatch = []
    #匹配
    for apkhash in mergedList:
        if apkhash in payDict:
            payList.append(apkhash)
        elif apkhash in rogDict:
            rogList.append(apkhash)
        elif apkhash in stealDict:
            stealList.append(apkhash)
        else:
            # print '%s dont match any one' %apkhash
            noMatch.append(apkhash)
    # todo 可以将结果写入文件
    return len(payList),len(rogList),len(stealList)

def pkg2Hash(pkgList, pkgNameDict):
    '''
    replace all pkgName in pkgList to its hash according to pkgName-Hash Dict(not hash-pkgName dict!)
    so you need to reverse dict, dict(zip(malDict.values(), malDict.keys()))
    return a hash list
    '''
    if len(pkgList)==0:
        return
    resList = []
    # get all hash name 
    hashList = pkgNameDict.values()
    for pkg in pkgList:
        # if the pkg is already a hash name, just append it 
        if pkg in hashList:
            resList.append(pkg)
            continue       
        try:
            # else find its hash in pkgName-hash dict
            myHash = pkgNameDict[pkg]
        except KeyError:
            l.error('searching %s key error!',pkg)
            continue
        resList.append(myHash)
    return resList


def pkg2HashInDir(myDir, pkgFileRex, malFlag):
    '''
    描述：将存放包名list的文件根据hash-pkg字典转换成hashList的文件
    1.存放allMalDict.txt allNorDict.txt和pgk列表文件的文件夹myDir，其中dict={hash:pkg}
    2.需要替换成hash列表的pkg的正则匹配式pkgFileRex
    3.替换过程中需要查询的dict种类，标记malflag为真，那么查询maldict，反之
    4.替换成hash名的列表写入相应文件的_hash新文件中
    '''
    pkgDir = EasyDir(myDir)
    absDict = pkgDir.getAbsPathDict()
    # get all matched listFile paths
    fileNameRex = pkgFileRex
    myFileDict = pkgDir.rexFindPath(fileNameRex)

    malDict = FileUtils.readDict(absDict['allMalDict.txt'])
    norDict = FileUtils.readDict(absDict['allNorDict.txt'])
    # reverse dicts 
    malDict = dict(zip(malDict.values(), malDict.keys()))
    norDict = dict(zip(norDict.values(), norDict.keys()))
    # choose a dict to query
    selectDict = norDict
    if malFlag:
        selectDict = malDict
    for key,value in myFileDict.items():
        # key is listfile name, value is its AbsPath
        # now read the matched listFile one by one
        pkgList = FileUtils.readList(value)
        # print len(pkgList)
        # print len(pkgList[0])
        hashList = pkg2Hash(pkgList,selectDict)
        if not hashList:
            l.warning('deal %s error!',key)
            continue
        # write hashList to hashFile in pkgDir
        newNameList = os.path.splitext(key)
        newName  = newNameList[0]
        extendName = ''
        if len(newNameList)>1:
            extendName = newNameList[1]
        newName = newName+'_hash'+extendName
        FileUtils.writeList(hashList,pkgDir.getCatPath(newName))

def mergeAllDict(myDir, myRex):
    '''
    desc: merge all apkInfoDicts into pkgNameDict
    1. myDir reserve all dict files you need to merge
    2. use myRex to match the dict file names you want to merge
    3. convert merged dict value to str type when its value is list type
    4. return merged and converted dict
    '''
    # create a obj to store dir info
    norDir = EasyDir(myDir)
    # find all dicts match the myRex, return a dict {dictfileName:dictAbsPath}
    norDictPath =norDir.rexFindPath(myRex)
    # reading all matched dictFiles and append them to a list
    norList = []
    for i in norDictPath.values():
        norList.append(FileUtils.readDict(i))
    # dict merge operation
    norMerged = CollectionUtils.dictMerge(*norList)
    # convert value list in merged dict to str type
    norpkg ={}
    for key, value in norMerged.items():
        pkg=''
        if CollectionUtils.typeof(value) in 'list':
            pkg = value[0]
        else:
            pkg = value
        norpkg.update({key:pkg})
    return norpkg

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument('-s', '--src', help='app name', nargs='?', default="")
    parser.add_argument('-d', '--dest', help='app name', nargs='?', default="")
    parser.add_argument('-i', '--num', help='test time', nargs='?',type=int, default=10)
    args = parser.parse_args()
    srcDir=args.src
    copyNum=args.num
    destDir = args.dest

    # srcDir = 'C:\\Users\\limin\\Desktop\\normal5000_filter\\normal_test_5000'
    # destDir = 'C:\\Users\\limin\\Desktop\\tmp'
    randomCopy(srcDir, destDir, copyNum)
    # testDict = {'a':[1,2],'b':[2,3]}
    # res = statisticLists(testDict)
    # print res