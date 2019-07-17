#coding=utf-8
from modules import FileUtils
from modules import CollectionUtils
from rooms import FileRoom
from modules import RexUtils
from modules import AdbUtils
import os
import shutil
import random
class EasyDir:
    def __init__(self, myDir):
        self.currentDir = myDir
        self.fileNameList = FileUtils.listDir2(myDir)
        self.absPathDict = {}
        for fileName in self.fileNameList:
            absPath = os.path.join(myDir, fileName)
            self.absPathDict.update({fileName:absPath})
    def getFileAbsPath(self, fileName):
        if fileName not in self.absPathDict:
            return ''
        return self.absPathDict[fileName]
    def getAbsPathDict(self):
        return self.absPathDict
    def rexFindPath(self, myRex):
        resDict = {}
        for key,value in self.absPathDict.items():
            if len(RexUtils.rexFind(myRex, key))>0:
                resDict.update({key:value})
        return resDict
    
    def getCatPath(self, fileName):
        return os.path.join(self.currentDir,fileName)

def mergeAllDict(myDir, myRex):
    norDir = EasyDir(myDir)
    norDictPath =norDir.rexFindPath(myRex)
    norList = []
    for i in norDictPath.values():
        norList.append(FileUtils.readDict(i))
    print len(norList)
    norMerged = CollectionUtils.dictMerge(*norList)
    norpkg ={}
    for key, value in norMerged.items():
        pkg=''
        if CollectionUtils.typeof(value) in 'list':
            pkg = value[0]
        else:
            pkg = value
        norpkg.update({key:pkg})
    return norpkg

def pkg2Hash(pkgList, pkgNameDict):
    '''
    replace all pkgName in pkgList to its hash according to pkgName-Hash Dict
    return a hash list
    '''
    if len(pkgList)==0:
        return
    resList = []
    hashList = pkgNameDict.values()
    for pkg in pkgList:
        if pkg in hashList:
            resList.append(pkg)
            continue       
        try:
            myHash = pkgNameDict[pkg]
        except KeyError:
            print 'searching %s error!' %pkg
            continue
        resList.append(myHash)
    return resList

def pkg2HashInDir(myDir, pkgFileRex, malFlag):
    pkgDir = EasyDir(myDir)
    absDict = pkgDir.getAbsPathDict()
    
    fileNameRex = pkgFileRex
    myFileDict = pkgDir.rexFindPath(fileNameRex)

    malDict = FileUtils.readDict(absDict['allMalDict.txt'])
    norDict = FileUtils.readDict(absDict['allNorDict.txt'])

    malDict = dict(zip(malDict.values(), malDict.keys()))
    norDict = dict(zip(norDict.values(), norDict.keys()))
    selectDict = norDict
    if malFlag:
        selectDict = malDict
    for key,value in myFileDict.items():
        print key,value
        pkgList = FileUtils.readList(value)
        print len(pkgList)
        hashList = pkg2Hash(pkgList,selectDict)
        if not hashList:
            print 'error******'
            continue
        print len(hashList)
        FileUtils.writeList(hashList,pkgDir.getCatPath(key+'_hash'))

def getHashPkgDict(myDir):
    allApkPathList = FileUtils.listDir(myDir)
    hashPkgDict = {}
    idx = 0
    for apkPath in allApkPathList:
        idx += 1
        print idx
        apkHash = FileUtils.getFileName(apkPath)
        packageName=AdbUtils.getApkInfo(apkPath,"package: name=")
        print apkHash,packageName
        if packageName:
            hashPkgDict.update({apkHash:packageName})
    return hashPkgDict

def splitMalware():
    return
import sys
if __name__ == "__main__":
    
    # testalllist = FileUtils.readList(testallpath)

    # test5List = FileUtils.readList(test5Path)
    # logsPathList =[logsdir1,logsdir2,logsdir3,logsdir4,logsdir5,logsdir6,logsdir7,logsdir8,logsdir9]
    
    # LList = []
    # for logpath in logsPathList:
    #     mylist = FileUtils.listDir3(logpath)
    #     if mylist:
    #         LList.extend(mylist)
    # LList.extend(test5List)
    # print len(LList)
    # LList = list(set(LList))
    # print len(LList)
    # print len(testalllist)
    # restalllist = CollectionUtils.listDifference(testalllist, LList)
    # print len(restalllist)

    # restallpath='C:\\Users\\limin\\Desktop\\allnor\\restall.txt'
    # FileUtils.writeList(restalllist,restallpath)
    # 一个类，表示一个目录，只要一个文件名就能够获取文件的路径，basename和去后缀的basename
    # 我已经受够了无限的windows路径
    pkgDir = EasyDir('C:\\Users\\limin\\Desktop\\v1pkg')
    pkgPathDict = pkgDir.getAbsPathDict()

    # pkg2HashInDir('C:\\Users\\limin\\Desktop\\v1pkg',r'v1_train_nor',False)
    # # pkg2HashInDir('C:\\Users\\limin\\Desktop\\v1pkg',r'v1.*?mal',True)
    
    # sys.exit()
    v1TrainMal = FileUtils.readList(pkgPathDict['v1_train_mal_hash'])
    v1TestMal = FileUtils.readList(pkgPathDict['v1_test_mal_hash'])
    v1TrainNor = FileUtils.readList(pkgPathDict['v1_train_nor_hash'])
    v1TestNor = FileUtils.readList(pkgPathDict['v1_test_nor'])

    v2TrainMal = FileUtils.readList(pkgPathDict['v2_train_mal'])
    v2TestMal = FileUtils.readList(pkgPathDict['v2_test_mal'])
    v2TrainNor = FileUtils.readList(pkgPathDict['v2_train_nor'])
    v2TestNor = FileUtils.readList(pkgPathDict['v2_test_nor'])

    test1 = v2TrainNor
    test2 =  v2TestNor


    mydir = 'C:\\Users\\limin\\Desktop\\allMalDict'
    malDictDir = EasyDir(mydir)
    malDict = malDictDir.getAbsPathDict()

    payDict = FileUtils.readDict(malDict['payAllDict.txt'])
    rogDict = FileUtils.readDict(malDict['rogAllDict.txt'])
    stealDict = FileUtils.readDict(malDict['stealAllDict.txt'])

    paylist = FileUtils.listDir3("C:\\Users\\limin\\Desktop\\malware_test\\logs_rog\\rog_ruled")
    

    payList = []
    rogList = []
    stealList = []
    for apkhash in paylist:
        if apkhash in payDict:
            payList.append(apkhash)
        elif apkhash in rogDict:
            rogList.append(apkhash)
        elif apkhash in stealDict:
            stealList.append(apkhash)
        else:
            print '%s dont match any one' %apkhash
    print len(payList)
    print len(rogList)
    print len(stealList)
    


