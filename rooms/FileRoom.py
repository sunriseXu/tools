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


l = logging.getLogger("FileRoom")

def print_all(module_):
    modulelist = dir(module_)
    length = len(modulelist)
    for i in range(0,length,1):
        print getattr(module_,modulelist[i])

def randomCopy(srcDir,destDir,maxNum):
    '''
    randomly select maxNum files in srcDir, and copy them to destDir
    '''
    fileList = FileUtils.listDir(srcDir)
    randomList = random.sample(fileList, maxNum)
    FileUtils.mkdir(destDir)
    FileUtils.listCopy2(randomList,destDir)
    return

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
        srcpath=os.path.join(srcDir,i)
        ri = i.split('log_')[1]
        destpath=os.path.join(srcDir,ri)
        os.rename(srcpath,destpath)

def renamePkg2Hash(srcDir, destDir, apkInfoDictPath):
    '''
    rename all pkgname file in srcdir to hash name according to apkinfodict
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
    for pkg in fileList:
        if pkg in hashList:
            myHash = pkg
        else:
            myHash = CollectionUtils.queryValueOfDict(newdict,pkg)
        if not myHash:
            return 
        srcPath = os.path.join(srcDir, pkg+'.txt')
        destPath = os.path.join(destDir,myHash+'.txt')
        shutil.copy(srcPath, destPath)

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