from modules import FileUtils
from modules import CollectionUtils
from rooms import FileRoom
import os
import shutil
import random
if __name__ == "__main__":
    apkdictpath1='C:\\Users\\limin\\Desktop\\mal_filter\\pay_filter\\apkInfoDict.txt'
    apkdictpath2='C:\\Users\\limin\\Desktop\\mal_filter\\pay_filter\\apkInfoDict_2.txt'
    pathList = [apkdictpath1,apkdictpath2]
    newpath='C:\\Users\\limin\\Desktop\\mal_filter\\steal_filter\\apkInfoDict.txt'
    # mergedDict = FileRoom.mergeAndWriteDict(pathList,newpath)
   
    stealsrcDir = "C:\\Users\\limin\\Desktop\\mal_filter\\steal_filter\\steal_pass_hash"
    stealdestDir = 'C:\\Users\\limin\\Desktop\\mal_filter\\steal_filter\\steal_norule'
    paysrcDir = 'C:\\Users\\limin\\Desktop\\mal_filter\\pay_filter\\pay_ruled_hash'
    paydestDir='C:\\Users\\limin\\Desktop\\mal_filter\\pay_filter\\pay_norule'
    rogsrcDir ='C:\\Users\\limin\\Desktop\\mal_filter\\rog_filter\\rog_pass_hash'
    rogdestDir ='C:\\Users\\limin\\Desktop\\mal_filter\\rog_filter\\rog_norule'
    # FileRoom.trimAllPrefix(srcDir)
    # FileRoom.renamePkg2Hash(srcDir,destDir,newpath)
    norulepath='C:\\Users\\limin\\Desktop\\norule.txt'
    # norule = FileUtils.readList(norulepath)
    # FileUtils.listCut(norule,stealsrcDir,stealdestDir)
    payRuleDir='C:\\Users\\limin\\Desktop\\allMalFinal\\pay\\ruled'
    payTrainPathV2='C:\\Users\\limin\\Desktop\\allMalFinal\\pay\\v2_uploaded667.txt'
    payTestPathV2='C:\\Users\\limin\\Desktop\\allMalFinal\\pay\\v2_ruled_test167.txt'
    payTrainPathV1='C:\\Users\\limin\\Desktop\\allMalFinal\\pay\\v1_uploaded667.txt'
    payTestPathV1='C:\\Users\\limin\\Desktop\\allMalFinal\\pay\\v1_ruled_test167.txt'
    payTrainDirV1='C:\\Users\\limin\\Desktop\\allMalFinal\\pay\\v1_train667'
    payTestDirV1='C:\\Users\\limin\\Desktop\\allMalFinal\\pay\\v1_test167'

    rogRuleDir='C:\\Users\\limin\\Desktop\\allMalFinal\\rog\\ruled'
    rogTrainPathV2='C:\\Users\\limin\\Desktop\\allMalFinal\\rog\\v2_uploaded667.txt'
    rogTestPathV2='C:\\Users\\limin\\Desktop\\allMalFinal\\rog\\v2_ruled_test167.txt'
    rogTrainPathV1='C:\\Users\\limin\\Desktop\\allMalFinal\\rog\\v1_uploaded667.txt'
    rogTestPathV1='C:\\Users\\limin\\Desktop\\allMalFinal\\rog\\v1_ruled_test167.txt'
    rogTrainDirV1='C:\\Users\\limin\\Desktop\\allMalFinal\\rog\\v1_train667'
    rogTestDirV1='C:\\Users\\limin\\Desktop\\allMalFinal\\rog\\v1_test167'

    stealRuleDir='C:\\Users\\limin\\Desktop\\allMalFinal\\steal\\ruled'
    stealTrainPathV2='C:\\Users\\limin\\Desktop\\allMalFinal\\steal\\v2_uploaded667.txt'
    stealTestPathV2='C:\\Users\\limin\\Desktop\\allMalFinal\\steal\\v2_ruled_test167.txt'
    stealTrainPathV1='C:\\Users\\limin\\Desktop\\allMalFinal\\steal\\v1_uploaded667.txt'
    stealTestPathV1='C:\\Users\\limin\\Desktop\\allMalFinal\\steal\\v1_ruled_test167.txt'
    stealTrainDirV1='C:\\Users\\limin\\Desktop\\allMalFinal\\steal\\v1_train667'
    stealTestDirV1='C:\\Users\\limin\\Desktop\\allMalFinal\\steal\\v1_test167'

    alltrianV1='C:\\Users\\limin\\Desktop\\allMalFinal\\v1_train'
    alltestV1='C:\\Users\\limin\\Desktop\\allMalFinal\\v1_test'
    trainlist = FileUtils.listDir2(alltrianV1)
    testlist = FileUtils.listDir2(alltestV1)
    print len(trainlist)
    print len(testlist)
    print len(CollectionUtils.listIntersection(trainlist,testlist))