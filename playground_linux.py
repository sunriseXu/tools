#coding=utf-8
from modules import FileUtils
from modules import CollectionUtils

from modules import RexUtils
from modules import AdbUtils
from modules import ApkUtils
from modules.FileUtils import EasyDir
from modules import SpyderUtils
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
logging.basicConfig()
l = logging.getLogger("playground")



if __name__ == "__main__":
    # # 对目标目录下的pkgList文件通过hash-pkg字典进行转换，变成对应的hashList文件，写入目标目录，两个字典文件也需要在目标目录下
    # pkg2HashInDir('C:\\Users\\limin\\Desktop\\v1pkg',r'v1_train_nor20000.txt',False)
    # pkg2HashInDir('C:\\Users\\limin\\Desktop\\v1pkg',r'v1.*?mal',True)
    
    # 读取目标目录下的所有hashList文件，并且计算list之间的交集 并集 差集
    # pkgDir = EasyDir('C:\\Users\\limin\\Desktop\\v1pkg')
    # pkgPathDict = pkgDir.getAbsPathDict()
    # v1TrainMal = FileUtils.readList(pkgPathDict['v1_train_mal_hash'])
    # v1TestMal = FileUtils.readList(pkgPathDict['v1_test_mal_hash'])
    # v1TrainNor = FileUtils.readList(pkgPathDict['v1_train_nor_hash'])
    # v1TestNor = FileUtils.readList(pkgPathDict['v1_test_nor'])
    # v2TrainMal = FileUtils.readList(pkgPathDict['v2_train_mal'])
    # v2TestMal = FileUtils.readList(pkgPathDict['v2testMal.txt'])
    # v2TrainNor = FileUtils.readList(pkgPathDict['v2_train_nor'])
    # v2TestNor = FileUtils.readList(pkgPathDict['v2_test_nor'])
    # test1 = v1TrainMal+v1TestMal
    # print len(test1)
    # test2 =  v2TrainMal+v2TestMal
    # print len(test2)
    # print len(CollectionUtils.listIntersection(test1,test2))
    # splitMalware(v2TestMal)
    
    # # 首先对源目录下的log文件去掉log_前缀，然后根据hash-pkg字典对目录下所有以包名命名的log文件重命名成hash命名的文件
    # srcdir = 'C:\\Users\\limin\\Desktop\\malfromHR\\testmalicious'
    # FileRoom.trimAllPrefix(srcdir)
    # destdir = 'C:\\Users\\limin\\Desktop\\malfromHR\\testmalicious_hash'
    # FileRoom.renamePkg2Hash(srcdir,destdir,'C:\\Users\\limin\\Desktop\\allMalDict\\allMalDict.txt')
    
    # # 读取文件夹下的logList，进行3种分类
    # malList = FileUtils.listDir3('C:\\Users\\limin\\Desktop\\allMal\\malAllRuled\\v1Test500')
    # splitMalware(malList)

    # # 对不同文件夹下的文件进行读取，批量处理多个文件夹的文件
    # # 1. 现在分出新的v1集合，首先从v2中读取已经分出来的列表，从目录获取文件，然后与list文件进行验证 
    # # 2. 读取ruled文件夹下的list，同样和list进行验证
    # # 3. 验证通过后 取差集，然后random选择 667 ， 再次取差集 random选择167 形成相应list，写入文件，然后根据list写入v1 train和test文件夹下
    # pdirnameList = ['malSteal','malPay','malRog']
    # for pdirname in pdirnameList:
    #     srcDir = 'C:\\Users\\limin\\Desktop\\allMal\\malAllRuled\\%s' %pdirname
    #     mysrcDir = EasyDir(srcDir)
    #     childPathDict = mysrcDir.getAbsPathDict()
    #     v2_train_list = FileUtils.readList(childPathDict['uploaded667.txt'])
    #     v2_test_list = FileUtils.readList(childPathDict['ruled_test167.txt'])

    #     v1_train_list = FileUtils.readList(childPathDict['v1Train667.txt'])
    #     v1_test_list = FileUtils.readList(childPathDict['v1Test167.txt'])
        
    #     v1_train_dir_list = FileUtils.listDir3(childPathDict['v1Train667'])
    #     v1_test_dir_list  = FileUtils.listDir3(childPathDict['v1Test167'])
    #     all_ruled_dir_list = FileUtils.listDir3(childPathDict['ruled'])
    #     # check valid
    #     test1 = v1_test_list
    #     test2 = v1_train_list
    #     print len(test1)
    #     print len(test2)
    #     print len(CollectionUtils.listIntersection(test1,test2))
    
    # FileUtils.writeList(mylist, '/home/limin/Desktop/logs_more1w3/part2/logs/traces/lastTest.txt')

    # # 对文件夹下的所有log文件的log_前缀去掉,重命名
    # srcDir = '/home/limin/Desktop/norAll/total/traces'
    # trimAllPrefix(srcDir)

    # # 根据abandon文件,将不符合的log剪切到指定文件夹下
    # abandonPath = '/home/limin/Desktop/abandon.txt'
    # abandonList = FileUtils.readList(abandonPath)
    # mySrc = '/home/limin/Desktop/norAll/total/traces'
    # abandonDir = '/home/limin/Desktop/norAll/total/abandon'
    # FileUtils.listCut(abandonList, mySrc, abandonDir)

    # # 在所有normal trace的文件夹下, 包含v1 所有上传到数据库的列表, 筛选出v2列表和文件夹
    # myDir = EasyDir('/home/limin/Desktop/allHashInDb')
    # dirDict = myDir.getAbsPathDict()
    # v1_test_mal = FileUtils.readList(dirDict['v1_test_malicious500_201907221211.csv'])
    # v1_test_nor = FileUtils.readList(dirDict['v1_test_normal5000_201907221220.csv'])
    # v1_train_mal = FileUtils.readList(dirDict['v1_train_malicious2000_201907221216.csv'])
    # v1_train_nor = FileUtils.readList(dirDict['v1_train_nor_Hash.csv'])
    # v2_test_mal = FileUtils.readList(dirDict['v2_test_malicious500_201907220955.csv'])
    # v2_test_nor = FileUtils.readList(dirDict['v2_test_normal5000_2_201907220950.csv'])
    # v2_train_mal = FileUtils.readList(dirDict['v2_train_malicious2000_201907220955.csv'])
    # v2_train_nor = FileUtils.readList(dirDict['v2_train_normal20000_2_201907220953.csv'])
    # all_list = [v1_test_mal,v1_test_nor,v1_train_mal,v1_train_nor,v2_test_mal,v2_test_nor,v2_train_mal,v2_train_nor]
    # # print all_list[2]
    # for i in range(0,len(all_list)):
    #     all_list[i] = [item.strip('"') for item in all_list[i]]
    #     print len(all_list[i])
    # all_mal_dict = FileUtils.readDict(dirDict['allNorDict.txt'])
    # all_mal_dict=dict(zip(all_mal_dict.values(), all_mal_dict.keys()))
    # v1_train_nor = pkg2Hash(all_list[3],all_mal_dict)
    # all_list[3]  = v1_train_nor
    # FileUtils.writeList(v1_train_nor, myDir.getCatPath('v1_train_nor_Hash.csv'))
    # v1_test_mal = all_list[0]
    # v1_test_nor = all_list[1]
    # v1_train_mal = all_list[2]
    # v1_train_nor = all_list[3]
    # v2_test_mal = all_list[4]
    # v2_test_nor = all_list[5]
    # v2_train_mal = all_list[6]
    # v2_train_nor = all_list[7]
    
    # v1_mal_list = v1_train_mal + v1_test_mal
    # v2_mal_list = v2_train_mal + v2_test_mal

    # FileUtils.writeList(v1_mal_list, myDir.getCatPath('v1_mal.txt'))
    # FileUtils.writeList(v2_mal_list, myDir.getCatPath('v2_mal.txt'))

    # for i in range(0,len(all_list)):
    #     for j in range(0, len(all_list)):
    #         if i!=j:
    #             print len(CollectionUtils.listIntersection(all_list[i],all_list[j]))

    # with open("repeatlist", "w") as f:
    #     tmp = [val for val in v1_train_nor if val in v1_test_nor]
    #     f.write("v1_train_nor v1_test_nor: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")

    #     tmp = [val for val in v1_train_nor if val in v2_train_nor]
    #     f.write("v1_train_nor v2_train_nor: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")

    #     tmp = [val for val in v1_train_nor if val in v2_test_nor]
    #     f.write("v1_train_nor v2_test_nor: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")

    #     tmp = [val for val in v1_test_nor if val in v2_train_nor]
    #     f.write("v1_test_nor v2_train_nor: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")

    #     tmp = [val for val in v1_test_nor if val in v2_test_nor]
    #     f.write("v1_test_nor v2_test_nor: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")

    #     tmp = [val for val in v2_train_nor if val in v2_test_nor]
    #     f.write("v2_train_nor v2_test_nor: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")


    #     tmp = [val for val in v1_train_mal if val in v1_test_mal]
    #     f.write("v1_train_mal v1_test_mal: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")

    #     tmp = [val for val in v1_train_mal if val in v2_train_mal]
    #     f.write("v1_train_mal v2_train_mal: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")

    #     tmp = [val for val in v1_train_mal if val in v2_test_mal]
    #     f.write("v1_train_mal v2_test_mal: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")

    #     tmp = [val for val in v1_test_mal if val in v2_train_mal]
    #     f.write("v1_test_mal v2_train_mal: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")

    #     tmp = [val for val in v1_test_mal if val in v2_test_mal]
    #     f.write("v1_test_mal v2_test_mal: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")

    #     tmp = [val for val in v2_train_mal if val in v2_test_mal]
    #     f.write("v2_train_mal v2_test_mal: {:d}\n".format(len(tmp)))
    #     for i in tmp:
    #         f.write(i+"\n")
    #testing
    # print len(v1_train_list)
    # print len(v1_test_list)
    # print len(CollectionUtils.listIntersection(v1_train_list,v1_test_list))

    # v1_list = v1_train_list+v1_test_list
    # print len(v1_list)

    # all_list = FileUtils.listDir3(dirDict['traces'])
    # # print len(nor_rest_list)
    # # print nor_rest_list[0]

    # rest_list = CollectionUtils.listDifference(all_list, v1_list)
    # # print len(rest_list)
    # #print len(CollectionUtils.listIntersection(rest_list, v1_list))

    # v2_train_20000 = random.sample(rest_list, 20000)
    
    # rest_list = CollectionUtils.listDifference(rest_list, v2_train_20000)
    # v2_test_5000 = random.sample(rest_list, 5000)
    
    # print len(CollectionUtils.listIntersection(v2_test_5000,v2_train_20000))

    # # FileUtils.writeList(v2_train_20000, myDir.getCatPath('v2Train20000.txt'))
    # # FileUtils.writeList(v2_test_5000, myDir.getCatPath('v2Test5000.txt'))

    # v2_train_20000 = CollectionUtils.graftListItem(v2_train_20000, '','.txt')
    # v2_test_5000 = CollectionUtils.graftListItem(v2_test_5000, '','.txt')

    # v2_train_20000 = FileUtils.readList(dirDict['v2Train20000.txt'])
    # v2_test_5000 = FileUtils.readList(dirDict['v2Test5000.txt'])

    # v2_train_2 = FileUtils.listDir3(dirDict['v2Train'])
    # v2_test_2 = FileUtils.listDir3(dirDict['v2Test'])

    # print len(CollectionUtils.listIntersection(v2_train_2, v2_train_20000))
    # print len(CollectionUtils.listIntersection(v2_test_2, v2_test_5000))
    # # FileUtils.listCopy(v2_train_20000,dirDict['traces'],myDir.getCatPath('v2Train'))
    # # FileUtils.listCopy(v2_test_5000, dirDict['traces'], myDir.getCatPath('v2Test'))

    # 读取目标目录下的所有hashList文件，并且计算list之间的交集 并集 差集
    # pkgDir = EasyDir('C:\\Users\\limin\\Desktop\\v1pkg')
    # pkgPathDict = pkgDir.getAbsPathDict()
    # v1TrainMal = FileUtils.readList(pkgPathDict['v1_train_mal_hash'])
    # v1TestMal = FileUtils.readList(pkgPathDict['v1_test_mal_hash'])
    # v1_all = list(set(v1TrainMal+v1TestMal))
    # splitMalware(v1_all)
    # print '\n'
    
    # v2TrainMal = FileUtils.readList(pkgPathDict['v2_train_mal'])
    # v2TestMal = FileUtils.readList(pkgPathDict['v2testMal.txt'])
    # v2_all = list(set(v2TrainMal+v2TestMal))
    # splitMalware(v2_all)
    # print '\n'
    # print len(CollectionUtils.listIntersection(v1_all,v2_all))
    
    
    # allMal = list(set(v1TestMal+v1TrainMal+v2TrainMal+v2TestMal))
    
    # splitMalware(allMal)
    
    # 统计v1_old 和 v2 恶意软件列表， 并且与新的v1进行交叉比较
    # pkgDir = EasyDir('C:\\Users\\limin\\Desktop\\v1pkg')
    # pkgPathDict = pkgDir.getAbsPathDict()
    # v1TrainMal = FileUtils.readList(pkgPathDict['v1_train_mal_hash'])
    # v1TestMal = FileUtils.readList(pkgPathDict['v1_test_mal_hash'])
    # v2TestMal = FileUtils.readList(pkgPathDict['v2_test_mal'])
    # v2TrainMal = FileUtils.readList(pkgPathDict['v2_train_mal'])
    # v1_all = list(set(v1TrainMal+v1TestMal))
    # v2_all = list(set(v2TestMal+v2TrainMal))
    # v1_all = list(set(v1_all + v2_all))
    # pdirnameList = ['malPay','malRog','malSteal']
    # for pdirname in pdirnameList:
    #     srcDir = 'C:\\Users\\limin\\Desktop\\allMal\\malAllRuled\\%s' %pdirname
    #     mysrcDir = EasyDir(srcDir)
    #     childPathDict = mysrcDir.getAbsPathDict()
    #     all_ruled_dir_list = FileUtils.listDir3(childPathDict['ruled'])
    #     print '\n'
    #     # print len(all_ruled_dir_list)
    #     new_rule_167 = FileUtils.readList(childPathDict['new_rule_167.txt'])
    #     new_667 = FileUtils.readList(childPathDict['new_667.txt'])
    #     new_667  = [i.upper() for i in new_667]
    #     new_all = new_rule_167 + new_667

    #     new_667_dirlist = FileUtils.listDir3(childPathDict['new_667'])
    #     new_667_dirlist = [i.upper() for i in new_667_dirlist]
    #     new_167_dirlist = FileUtils.listDir3(childPathDict['new_167'])
    #     new_all_dirlist = new_667_dirlist + new_167_dirlist

    #     print 'train667 && test167'
    #     print len(CollectionUtils.listIntersection(new_rule_167, new_667))
    #     # print len(CollectionUtils.listIntersection(new_667_dirlist, new_167_dirlist))


    #     # print len(CollectionUtils.listDifference(new_667_dirlist, new_167_dirlist))
    #     # print len(CollectionUtils.listDifference(new_667, new_rule_167))
    #     # print len(CollectionUtils.listDifference(new_all, new_all_dirlist))
    #     print 'test167 && (v1_old+v2)'
    #     print len(CollectionUtils.listIntersection(new_rule_167, v1_all))
    #     print 'train667 && (v1_old+v2)'
    #     print len(CollectionUtils.listIntersection(new_667, v1_all))

    #     print 'train:'
    #     splitMalware(new_667)
    #     print '\ntest:'
    #     splitMalware(new_rule_167)




    # steal 类的分类 和 筛选
    # srcDir = 'C:\\Users\\limin\\Desktop\\allMal\\malAllRuled\\malSteal'
    # mysrcDir = EasyDir(srcDir)
    # childPathDict = mysrcDir.getAbsPathDict()
    # all_ruled_dir_list = FileUtils.listDir3(childPathDict['ruled'])
    # print len(all_ruled_dir_list)
    # new_rule_167 = FileUtils.readList(childPathDict['new_rule_167.txt'])
    # rest_ruled = CollectionUtils.listDifference(all_ruled_dir_list, new_rule_167)
    # print len(rest_ruled)
    # new_rule_667  = random.sample(rest_ruled, 667)
    # FileUtils.writeList(new_rule_667, mysrcDir.getCatPath('new_667.txt'))
    # new_rule_667 = CollectionUtils.graftListItem(new_rule_667, '','.txt')
    # FileUtils.listCopy(new_rule_667, childPathDict['ruled'], mysrcDir.getCatPath('new_667'))


    # 打开json文件，然后搜索关键字，包含超过spy>5的就是信息窃取软件
    # 如果符合条件，记录文件hash生成列表文件 起码要2000个起步
    # 从数据库中拷贝2000个spy软件，跑一分钟
    # jsonDir = 'C:\\Users\\limin\\Desktop\\VirusShare_Android_reports'
    # fileList = FileUtils.listDir(jsonDir)
    # resList = []
    # idx = 0
    # for item in fileList:
    #     idx += 1
    #     # if idx > 10000:
    #     #     break
    #     fileName = FileUtils.getFileName(item)
    #     fileContent = FileUtils.readFile(item)
        
    #     spyRex = r'spy|Spy'
    #     foundgroup = RexUtils.rexFind(spyRex,fileContent)
    #     if len(foundgroup)>9:
    #         resList.append(fileName)
    #         print fileName
    # FileUtils.writeList(resList,'C:\\Users\\limin\\Desktop\\stealFoundList_9spy.txt')

    # 对找到的spy list与安天提供的spylist取交集，不重复测试
    # spyList = FileUtils.readList('C:\\Users\\limin\\Desktop\\stealFoundList.txt')
    # spyList  = [i.upper() for i in spyList]
    
    # antianDict = FileUtils.readDict('C:\\Users\\limin\\Desktop\\allHashDict\\allMalDict\\stealAllDict.txt')
    # antianList = antianDict.keys()
    # antianList = [str(i) for i in antianList]
    # diffList = CollectionUtils.listIntersection(spyList,antianList)
    # print len(diffList)

    # spyList = FileUtils.readList('C:\\Users\\limin\\Desktop\\stealFoundList.txt')

    # toTestList = random.sample(spyList, 600)
    # FileUtils.writeList(toTestList, 'C:\\Users\\limin\\Desktop\\toText_spy.txt')
    # FileUtils.mkdir('./apkTotest')
    # toTest = FileUtils.readList('./toTest.txt')
    # apkdirList = ['/mnt/VirusShare/VirusShare_Android_2013',
    #               '/mnt/VirusShare/VirusShare_Android_2014',
    #               '/mnt/VirusShare/VirusShare_Android_2015',
    #               '/mnt/VirusShare/VirusShare_Android_2016',
    #               '/mnt/VirusShare/VirusShare_Android_2017',
    #               '/mnt/VirusShare/VirusShare_Android_2018',
    #                 ]
    
    
    #筛选出 除去原v1和v2的 新v1的spy类
    # pkgDir = EasyDir('C:\\Users\\limin\\Desktop\\v1pkg')
    # pkgPathDict = pkgDir.getAbsPathDict()
    # v1TrainMal = FileUtils.readList(pkgPathDict['v1_train_mal_hash'])
    # v1TestMal = FileUtils.readList(pkgPathDict['v1_test_mal_hash'])
    # v2TestMal = FileUtils.readList(pkgPathDict['v2_test_mal'])
    # v2TrainMal = FileUtils.readList(pkgPathDict['v2_train_mal'])
    # v1_all = list(set(v1TrainMal+v1TestMal))
    # v2_all = list(set(v2TestMal+v2TrainMal))
    # v1_all = v1_all + v2_all
    # srcDir = 'C:\\Users\\limin\\Desktop\\allMal\\malAllRuled\\malSteal'
    # mysrcDir = EasyDir(srcDir)
    # childPathDict = mysrcDir.getAbsPathDict()
    # all_ruled_dir_list = FileUtils.listDir3(childPathDict['ruled'])
    # new_rule_167 = FileUtils.readList(childPathDict['new_rule_167.txt'])
    # rest_ruled = CollectionUtils.listDifference(all_ruled_dir_list, new_rule_167)
    # rest_ruled = CollectionUtils.listDifference(rest_ruled, v1_all)
    # new_rule_667  = random.sample(rest_ruled, 667)
    # FileUtils.writeList(new_rule_667, mysrcDir.getCatPath('new_667.txt'))
    # new_rule_667 = CollectionUtils.graftListItem(new_rule_667, '','.txt')
    # FileUtils.listCopy(new_rule_667, childPathDict['ruled'], mysrcDir.getCatPath('new_667'))

    #从ruled.txt中拷贝对应log
    # ruledPath = 'C:\\Users\\limin\\Desktop\\ruled.txt'
    # srcdir = 'C:\\Users\\limin\\Desktop\\traces_enRog\\traces'
    # destdir = 'C:\\Users\\limin\\Desktop\\traces_enRog\\traces_ruled'
    # FileUtils.listCopy3(ruledPath, srcdir, destdir)

    #从abandon.txt中剪切对应log
    # ruledPath = 'C:\\Users\\limin\\Desktop\\abandon.txt'
    # srcdir = 'C:\\Users\\limin\\Desktop\\traces_enRog\\traces'
    # destdir = 'C:\\Users\\limin\\Desktop\\traces_enRog\\traces_cut'
    # FileUtils.listCut2(ruledPath, srcdir, destdir)

    # 挑选规则：
    # 1. 首先将符合rule的挑选出来 （避免在第二步将其筛掉）
    # 2. 然后筛除了log小于4，和startlock多于9条的log
    # 3. 将剩余的和ruled合并

    # 对3类总集进行统计和重复计算
    # srcDir = 'C:\\Users\\limin\\Desktop\\allMal\\malAllRuled\\v1FinalMalTrain2000'
    # srcDir2 = 'C:\\Users\\limin\\Desktop\\allMal\\malAllRuled\\v1FinalMalTest500'
    # malTrain2000 =  FileUtils.listDir3(srcDir)
    # malTest500 = FileUtils.listDir3(srcDir2)
    # malTrain2000 = [i.upper() for i in malTrain2000]
    # malTrain2000 = list(set(malTrain2000))

    # print len(CollectionUtils.listIntersection(malTrain2000, malTest500))
    # splitMalware(malTrain2000)
    # splitMalware(malTest500)
    # print len(CollectionUtils.listIntersection(malTrain2000+malTest500,v1_all))

    # 对数据库抓取的列表于本地文件夹列表进行比较确定无误
    # dbpath = 'C:\\Users\\limin\\Desktop\\v1pkg\\v1TrainMal2000.txt'
    # srcDir2 = 'C:\\Users\\limin\\Desktop\\allMal\\malAllRuled\\v1FinalMalTrain2000'
    # malTest500 = FileUtils.listDir3(srcDir2)
    # dblist = FileUtils.readList(dbpath)
    # print len(CollectionUtils.listIntersection(dblist,malTest500))

    # 首先读取所有hash文件，由zm提供，读取其成为dict
    # 为什么要读取hash文件呢，直接读取json文件就行了，哦，因为hash文件有正常样本与hash的映射，所以只要读取正常样本的json文件就行了，到时候和文件名做一个映射关系就行了
    # hashListPath = '/mnt/apk/huawei/md5_malware.log'
    # hashList = FileUtils.readList(hashListPath)
    # print len(hashList)
    

    # targetDir = '/mnt/apk/huawei/reports_malware'
    # positiveDictPath = './positiveDict.json'
    # positiveDict = {}
    # for myHash in hashList:
    #     apkHash = myHash.lower().strip('\r')
    #     jsonName = apkHash+'.json'
    #     jsonPath = os.path.join(targetDir, jsonName)
    #     positivesCount = -1
    #     firstSeen = ''
    #     if os.path.exists(jsonPath):
    #         jsonDict = FileUtils.readDict(jsonPath)
    #         positivesCount = jsonDict['positives']
    #         firstSeen = jsonDict['first_seen']
    #     if apkHash not in positiveDict:
    #         positiveDict.update({apkHash:[positivesCount, firstSeen]})
    # FileUtils.writeDict(positiveDict, positiveDictPath)
    
    # 对normal的vt报告进行统计
    # hashListPath1 = '/mnt/apk/huawei/md5_201902.log'
    # hashListPath2 = '/mnt/apk/huawei/md5_201905.log'
    # reportsDir = '/mnt/apk/huawei/reports_normal'
    # hashApkNameDictPath = './norhashApkNameDict.txt'
    # positiveDictPath = './positiveDictNor.json'

    # hashList1 = FileUtils.readList(hashListPath1)
    # hashList2 = FileUtils.readList(hashListPath2)
    # print len(hashList1)
    # print len(hashList2)
    # print len(hashList1)+len(hashList2)
    # hashList = list(set(hashList1 + hashList2))
    # print len(hashList)
    # hashApkNameDict = {}
    # positiveDict={}

    # for item in hashList:
    #     itemList = item.split()
    #     myHash = itemList[0].strip()
    #     apkName = itemList[1].strip().strip('\r')
    #     apkName = os.path.splitext(apkName)[0]
    #     print myHash,apkName
    #     if myHash not in hashApkNameDict:
    #         hashApkNameDict.update({myHash:apkName})
    # FileUtils.writeDict(hashApkNameDict, hashApkNameDictPath)
    # print 'write hashapkName done!'
    # for key, value in hashApkNameDict.items():
    #     apkHash = key
    #     jsonName = key+'.json'
    #     jsonPath = os.path.join(reportsDir,jsonName)
    #     print jsonPath
    #     positivesCount = -1
    #     firstSeen = ''
    #     if os.path.exists(jsonPath):
    #         jsonDict = FileUtils.readDict(jsonPath)
    #         positivesCount = jsonDict['positives']
    #         firstSeen = jsonDict['first_seen']
    #     if apkHash not in positiveDict:
    #         positiveDict.update({apkHash:[positivesCount, firstSeen]})
    # FileUtils.writeDict(positiveDict, positiveDictPath)

    # 统计数量信息
    # dirPath = 'C:\\Users\\limin\\Desktop\\vTInfo'
    # myDir = EasyDir(dirPath)
    # pathDict = myDir.getAbsPathDict()
    # myDict = FileUtils.readDict(pathDict['positiveDictMal.json'])
    # print len(myDict)
    # resDict = {}
    # for key,value in myDict.items():
    #     countEngine = value[0]
    #     if countEngine in resDict:
    #         resDict[countEngine] += 1
    #     else:
    #         resDict.update({countEngine:1})
    # print resDict
    # resDictPath = myDir.getCatPath('norVtCount.json')
    # FileUtils.writeDict(resDict, resDictPath)

    # dirPath = 'C:\\Users\\limin\\Desktop\\vTInfo'
    # myDir = EasyDir(dirPath)
    # pathDict = myDir.getAbsPathDict()

    # mydict = FileUtils.readDict(pathDict['malVtCount.json'])
    
    # keyList = mydict.keys()
    # keyList  = [int(i) for i in keyList]
    # keyList.sort()
    # for key  in keyList:
    #     print '%d\t%s' %(key, mydict[str(key)])
    
    # 读取v1 v2所有训练集和测试集 list，包括正常的和恶意的,还有的问题是v1maltrain有近300个vt上的
    # 恶意样本提取hash值， 正常样本提取pkgName，与zm给的dict转换成hash值
    # 昨天晚上获取的dict可以进行以上信息统计
    # 对每个hash值找到其对应的count计数，并且形成计数dict
    # 对极端的count值找到对应的hash，人工确定极端情况

    # pkgDir = EasyDir('C:\\Users\\limin\\Desktop\\v1pkg')
    # pkgPathDict = pkgDir.getAbsPathDict()
    # v1MalTrain  =FileUtils.readList(pkgPathDict['v1TrainMal2000.txt'])
    # v1MalTest  = FileUtils.readList(pkgPathDict['v1TestMal500.txt'])
    # v1NorTrain = FileUtils.readList(pkgPathDict['v1NorTrainHash.txt'])
    # v1NorTest = FileUtils.readList(pkgPathDict['v1NorTestHash.txt'])

    # v1_all = v1MalTrain+v1MalTest+v1NorTrain+v1NorTest

    # v2MalTrain  = FileUtils.readList(pkgPathDict['v2_train_mal'])
    # v2MalTest  = FileUtils.readList(pkgPathDict['v2_test_mal'])
    # v2NorTrain = FileUtils.readList(pkgPathDict['v2NorTrainHash.txt'])
    # v2NorTest = FileUtils.readList(pkgPathDict['v2NorTestHash.txt'])

    # v2_all = v2MalTrain+v2MalTest+v2NorTrain+v2NorTest
    # print len(CollectionUtils.listIntersection(v1_all,v2_all))

    # nor_all = v1NorTest+v1NorTrain+v2NorTest+v2NorTrain
    # mal_all = v1MalTest+v1MalTrain+v2MalTest+v2MalTrain

    # dirPath = 'C:\\Users\\limin\\Desktop\\vTInfo'
    # vtPath = EasyDir(dirPath)
    # vtPathDict = vtPath.getAbsPathDict()

    # # norpkgHash = FileUtils.readDict(vtPathDict['norApkNameHashDict.json'])
    # # v1NorTest = CollectionUtils.key2Valuelist(v1NorTest, norpkgHash)
    # # FileUtils.writeList(v1NorTest,pkgDir.getCatPath('v1NorTestHash.txt'))
    

    # pCountMal = FileUtils.readDict(vtPathDict['positiveDictMal.json'])
    # pCountNor = FileUtils.readDict(vtPathDict['positiveDictNor.json'])


    # print len(pCountMal)
    # print len(pCountNor)

    # noRuledList = FileUtils.listDir3('C:\\Users\\limin\\Desktop\\allMal\\noruled')
    

    # resDict = {}
    # minCount = 8
    # maxCount = 15
    # dirtyCase = []
    # myList =CollectionUtils.listLower(noRuledList)
    # myDict = pCountMal
    # for key,value in myDict.items():
    #     if key not in myList:
    #         continue
    #     countEngine = value[0]
    #     # if (countEngine<=minCount) and (countEngine!=-1):
    #     #     dirtyCase.append(key)
    #     if countEngine>=maxCount:
    #         dirtyCase.append(key)
    #     if countEngine in resDict:
    #         resDict[countEngine] += 1
    #     else:
    #         resDict.update({countEngine:1})

    # reslist = CollectionUtils.dict2List(resDict)
    # # print len(dirtyCase)
    # FileUtils.writeList(reslist,vtPath.getCatPath('res/noruleMalAll.csv'))
    
    # 统计所有出现的权限api
    # dirname = 'C:\\Users\\limin\\androidSdkInAll\\Desktop\\androidOnline\\sdk24'
    # # dirname = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk24\\jsonRes'
    # pathList = FileUtils.listDir(dirname)
    # functionCount = []
    # for myPath in pathList:
    #     jsonDict = FileUtils.readDict(myPath)
    #     className = jsonDict['ClassName']
    #     functionDict = jsonDict['Functions']
    #     # print myPath
    #     for key,value in functionDict.items():
    #         if value['Permissions']:
    #             fullName = key
    #             perms = value['Permissions']
    #             for perm in perms:
    #                 # print fullName
    #                 # print perm
    #                 perm = perm.split('#')
    #                 if len(perm)==1:
    #                     continue
    #                 perm = perm[1]
    #                 functionCount.append((className,fullName,perm))

    #             # print key,value['Permissions']
    # print len(functionCount)
    # resDict = {}
    # permissionlist = []
    # classList = []
    # functionList = []
    # for function in functionCount:
    #     className = function[0]
    #     functionName = function[1]
    #     permission = function[2]
    #     if permission not in permissionlist:
    #         permissionlist.append(permission)
    #     if className not in classList:
    #         classList.append(className)

    #     if permission not in resDict:
    #         subDict = {className:[functionName]}
    #         resDict.update({permission:subDict})
    #     elif className not in resDict[permission]:
    #         subDict = {className:[functionName]}
    #         resDict[permission].update(subDict)
    #     else:
    #         resDict[permission][className].append(functionName)
    # FileUtils.writeDict(resDict,'./res.json')
    # print 'permission length:'
    # print len(permissionlist)
    # InteractUtils.showList(permissionlist)
    # FileUtils.writeList(permissionlist,'tmpOutO24.txt')
    # print 'class length'
    # print len(classList)
    # allDict = FileUtils.readDict('D:\\androidsdkdoc\\permission24.json')
    
    # partList = FileUtils.readList('tmpOutO24.txt')
    # resList = []
    # for permission in partList:
    #     tmp = ''
    #     for key,value in allDict.items():
    #         if permission in value:
    #             tmp = key+'\t'+permission +'\t' +' '.join(resDict[permission].keys())
    #             resList.append(tmp)
    # resList = sorted(resList)
    # FileUtils.writeList(resList, 'tmpOutOnline24.txt')

    # list1 = FileUtils.readList('tmpOut.txt')
    # list2 = FileUtils.readList('tmpOutO24.txt')
    # print len(CollectionUtils.listIntersection(list1,list2))
    # res = CollectionUtils.listDifference(list2,list1)
    # InteractUtils.showList(res)
    #需要从normal中选出2000+200,从malware中选出500+50
    #v1 normal选一半

    # allHash = EasyDir('/home/limin/Desktop/allHashInDb')
    # hashPathD = allHash.getAbsPathDict()
    # v1_nor_train = FileUtils.readList(hashPathD['v1_train_nor_Hash.csv'])
    # print(len(v1_nor_train))
    # v1_nor_test = FileUtils.readList(hashPathD['v1_test_normal5000_201907221220.csv'])
    # v1_nor_test = [i.strip('"') for i in v1_nor_test]
    # print(len(v1_nor_test))
    # v1_mal_train = FileUtils.readList(hashPathD['v1_train_malicious2000_201907221216.csv'])
    # print(len(v1_mal_train))
    # v1_mal_test = FileUtils.readList(hashPathD['v1_test_malicious500_201907221211.csv'])
    # print(len(v1_mal_test))
    #
    # v2_nor_train = FileUtils.readList(hashPathD['v2_train_normal20000_2_201907220953.csv'])
    # v2_nor_train = [i.strip('"') for i in v2_nor_train]
    # print(len(v2_nor_train))
    # v2_nor_test = FileUtils.readList(hashPathD['v2_test_normal5000_2_201907220950.csv'])
    # v2_nor_test = [i.strip('"') for i in v2_nor_test]
    # print(len(v2_nor_test))
    # v2_mal_train = FileUtils.readList(hashPathD['v2_train_malicious2000_201907220955.csv'])
    # print(len(v2_mal_train))
    # v2_mal_test = FileUtils.readList(hashPathD['v2_test_malicious500_201907220955.csv'])
    # print(len(v2_mal_test))
    #
    # # 首先需要
    # v3_1000_1 = random.sample(v1_nor_train,1100)
    # v3_1000_2 = random.sample(v2_nor_train,1100)
    # print("v3_1000_1 && v3_1000_2")
    # print(len(CollectionUtils.listIntersection(v3_1000_2,v3_1000_1)))
    # v3_2200 = v3_1000_1+v3_1000_2
    # print("v3_2200:")
    # print(len(v3_2200))
    #
    # v3_250_1 = random.sample(v1_nor_test, 300)
    # v3_250_2 = random.sample(v2_nor_test, 300)
    # print("v3_250_1 && v3_250_2")
    # print(len(CollectionUtils.listIntersection(v3_250_1, v3_250_2)))
    # v3_600 = v3_250_1 + v3_250_2
    # print("v3_600:")
    # print(len(v3_600))
    #
    # print('v3_2200 && v3_600')
    # print(len(CollectionUtils.listIntersection(v3_2200,v3_600)))
    #
    # v3Dir = EasyDir('./totest/v3')
    # v3Dict = v3Dir.getAbsPathDict()
    #
    # FileUtils.writeList(v3_2200, v3Dir.getCatPath('v3_nor_train'))
    # FileUtils.writeList(v3_600, v3Dir.getCatPath('v3_nor_test'))

    # 每类200 => 167  一共501
    # 每类30 =>  17
    def listInStr(myList, myStr):
        myStr = myStr.lower()
        for item in myList:
            if item not in myStr:
                # print('%s not in %s' %(item,myStr))
                return False
        # print('tags in %s' %(myStr))
        return True


    def uploadTracesDB(myDir, dbName, upDBbin, debug=False):

        upCmd = 'java -jar %s -f %s -d %s' % (upDBbin, myDir, dbName)
        l.warning('uploadCmd: %s', upCmd)
        res = ThreadUtils.execute_command(upCmd)
        print('uploading thread done ..')
        if debug:
            print(res)


    filterRuleBin = '/home/limin/Desktop/v3_log/FeatureEngineeringTest.jar'
    upDBbin = '/home/limin/Desktop/v3_log/logUpload.jar'
    wkDir = EasyDir('/home/limin/Desktop/logs_v3')
    # 0. 列出文件夹，指定文件夹的类型，合并part的文件夹，合并后在part同级目录下面
    # 0.1. 指定目标文件夹，和 normalTrain，normaltest大小，maltrain和maltest大小
    # 1. 首先需要将相关的dir进行合并处理，因为测试的时候会有分part的情况，还是手动分配好一点，因为识别起来有点难可能
    # 2. 对normal文件夹下的trace进行筛选，将abandon剔除到同级目录下面，如何筛选，能够通过rule的，和size过短的，失效的
    # 3. 剩余的normal合法trace放入保留在trace文件夹下
    # 4. 验证3类恶意样本交集情况，train和test，保证唯一性，如何验证，首先3类训练样本和测试样本应该分开测试，
    # 分别是pay-train steal-train rog-train pay-test steal-test rog-test 用random筛选出来，确保三类是三类
    # 如何保证？之前写了一个脚本区分三类啊,验证3类是3类后，才能进行下一步，否者退出，手动排查。然后将train的三类合并，test的三类合并，再进行合并后的大小检查，如果合并后的大小等于三类相加，那么说明没有重合，进行下一步，否者退出检查。合并后train和test进行唯一性检查，如果有重合，打印重合list，退出检查。否者进行下一步。
    # 开始写入
    # 5.将合并后的train list和test list（三类分开的，与合并的写入目标文件夹，并且建立文件夹，将三类合并后的trace拷贝进入train和test文件夹

    # 6. 将normal的train test考入目标文件夹
    # 完成
    malTrainAmount = 500
    singleMalTrainAmount = malTrainAmount / 3 + 1
    malTestAmount = 50
    singleMalTestAmount = malTestAmount / 3 + 1
    norTrainAmount = 2000
    norTestAmount = 500
    dbMalTrain = 'test'
    dbMalTest = 'test'
    dbNorTrain = 'test'
    dbNorTest = 'test'
    configDict = {
        'norTrain': {'path': '', 'dbName': '', 'merge': False, 'amount': norTrainAmount, 'tag': ['nor', 'train']},
        'norTest': {'path': '', 'dbName': '', 'merge': False, 'amount': norTestAmount, 'tag': ['nor', 'test']},
        'malPayTrain': {'path': '', 'dbName': '', 'merge': False, 'amount': singleMalTrainAmount,
                        'tag': ['mal', 'train', 'pay']},
        'malPayTest': {'path': '', 'dbName': '', 'merge': False, 'amount': singleMalTestAmount,
                       'tag': ['mal', 'test', 'pay']},
        'malRogTrain': {'path': '', 'dbName': '', 'merge': False, 'amount': singleMalTrainAmount,
                        'tag': ['mal', 'train', 'rog']},
        'malRogTest': {'path': '', 'dbName': '', 'merge': False, 'amount': singleMalTestAmount,
                       'tag': ['mal', 'test', 'rog']},
        'malStealTrain': {'path': '', 'dbName': '', 'merge': False, 'amount': singleMalTrainAmount,
                          'tag': ['mal', 'train', 'steal']},
        'malStealTest': {'path': '', 'dbName': '', 'merge': False, 'amount': singleMalTestAmount,
                         'tag': ['mal', 'test', 'steal']},
    }

    wkDirDict = wkDir.getAbsPathDict()
    fileList = sorted(wkDirDict.keys())
    InteractUtils.showList(fileList)
    for key, value in configDict.items():
        tags = value['tag']
        if 'mal' in tags and 'train' in tags:
            value['dbName'] = dbMalTrain
        elif 'mal' in tags and 'test' in tags:
            value['dbName'] = dbMalTest
        elif 'nor' in tags and 'train' in tags:
            value['dbName'] = dbNorTrain
        elif 'nor' in tags and 'test' in tags:
            value['dbName'] = dbNorTest

        for dirName in fileList:
            if listInStr(tags, dirName):
                value['path'] = wkDirDict[dirName]
                traceDir = os.path.join(wkDirDict[dirName], 'logs/traces')
                if not os.path.exists(traceDir):
                    value['merge'] = True
                break

    # deal with merging situation
    for key, value in configDict.items():
        if not value['merge']:
            continue
        print('Found parts of %s, now, merging...', key)

        keyDir = value['path']
        partPathList = []

        childDir = EasyDir(keyDir)
        childPath = childDir.getAbsPathDict().values()
        for cp in childPath:
            if os.path.isfile(cp):
                continue
            traceDir = os.path.join(cp, 'logs/traces')
            if os.path.exists(traceDir):
                partPathList.append(traceDir)
        if partPathList:
            mergedDir = os.path.join(keyDir, 'logs/traces')
            FileUtils.mkdir(mergedDir)
            for pp in partPathList:
                ppItems = FileUtils.listDir(pp)
                FileUtils.listCopy2(ppItems, mergedDir)
        print('Merge %s done!', key)

    # merging is done, next is filter traces,
    # 首先需要把某些东西都过一下rule，然后根据恶意与否进行筛选
    # 把正常的通过rule的样本筛出到某目录，然后把log过短和失效的样本筛掉，这里还是保持原traces目录不变，把相关的分类保存在list中
    # 把恶意的通过rule的样本筛出来就行了，分为ruled和norule的
    filterFlag = True
    for key, value in configDict.items():
        if not filterFlag:
            continue
        keyDir = value['path']
        dirTags = value['tag']
        dbAmount = value['amount']
        if not keyDir:
            continue
        ruleList = []
        noRuleList = []
        tracesDir = os.path.join(keyDir, 'logs/traces')
        ruleDir = os.path.join(keyDir, 'ruled')
        noruleDir = os.path.join(keyDir, 'noRule')
        shortOrInvalidDir = os.path.join(keyDir, 'shortInvalid')
        shortOrInvalidPath = os.path.join(keyDir, 'shortInvalid.txt')
        dblistPath = os.path.join(keyDir, 'dbList.txt')
        dbDir = os.path.join(keyDir, 'dbToUp')

        FileUtils.mkdir(ruleDir)
        FileUtils.mkdir(noruleDir)
        FileUtils.mkdir(shortOrInvalidDir)

        resultPath = os.path.join(keyDir, 'filtered.txt')
        cmd = 'java -jar %s -f %s >%s' % (filterRuleBin, tracesDir, resultPath)
        print(cmd)
        print('[!] Start to filter %s' % tracesDir)
        ThreadUtils.execute_command(cmd)
        print('[-] Filtering done!')
        ruleList, noRuleList = FileRoom.ruleStatistic(resultPath)

        ruleListG = CollectionUtils.graftListItem(ruleList, '', '.txt')
        noRuleListG = CollectionUtils.graftListItem(noRuleList, '', '.txt')

        FileUtils.listCopy(ruleListG, tracesDir, ruleDir)
        FileUtils.listCopy(noRuleListG, tracesDir, noruleDir)
        abandonBin = 'examples/filterLog.py'
        if noRuleList:
            abandomCmd = 'python %s -d %s -b %s' % (abandonBin, noruleDir, shortOrInvalidPath)
            ThreadUtils.execute_command(abandomCmd)
            shortOrInvalidList = FileUtils.readList(shortOrInvalidPath)
            shortOrInvalidList = CollectionUtils.graftListItem(shortOrInvalidList, '', '.txt')
            FileUtils.listCopy(shortOrInvalidList, noruleDir, shortOrInvalidDir)
        # 所有的筛选都完成了，接下来，将normal为通过rule的样本随机挑选对应的数量拷贝到特定目录上传到数据库
        selectSource = ''
        selectList = []
        if 'nor' in dirTags:
            selectSource = noruleDir
            selectList = noRuleList
        elif 'mal' in dirTags:
            selectSource = ruleDir
            selectList = ruleList
        if dbAmount > len(selectList):
            l.error('[?] Error, there are not enough(%d) logs to upload(which is %d): %s', len(selectList), dbAmount,
                    selectSource)
            continue
        dbList = random.sample(selectList, dbAmount)
        dbListG = CollectionUtils.graftListItem(dbList, tailStr='.txt')
        FileUtils.mkdir(dbDir)
        FileUtils.writeList(dbList, dblistPath)
        FileUtils.listCopy(dbListG, selectSource, dbDir)

    # Now, merge all dbdir to upload
    DBDir = wkDir.getCatPath('upDB')
    FileUtils.mkdir(DBDir)
    dbDirObj = EasyDir(DBDir)
    malTrainDir = FileUtils.mkdir(dbDirObj.getCatPath('malTrain'))
    malTestDir = FileUtils.mkdir(dbDirObj.getCatPath('malTest'))
    norTrainDir = FileUtils.mkdir(dbDirObj.getCatPath('norTrain'))
    norTestDir = FileUtils.mkdir(dbDirObj.getCatPath('norTest'))
    doMergeFlag = True
    for key, value in configDict.items():
        if not doMergeFlag:
            continue
        tags = value['tag']
        keyDir = value['path']
        if not keyDir:
            continue
        dbDir = os.path.join(keyDir, 'dbToUp')
        if not os.path.exists(dbDir):
            continue
        if 'mal' in tags and 'train' in tags:
            FileUtils.copytree(dbDir, malTrainDir)
        elif 'mal' in tags and 'test' in tags:
            FileUtils.copytree(dbDir, malTestDir)
        elif 'nor' in tags and 'train' in tags:
            FileUtils.copytree(dbDir, norTrainDir)
        elif 'nor' in tags and 'test' in tags:
            FileUtils.copytree(dbDir, norTestDir)

    dbDirDict = dbDirObj.getAbsPathDict()
    for key, value in dbDirDict.items():
        tags = key.lower()
        dbName = ''
        if 'mal' in tags and 'train' in tags:
            dbName = dbMalTrain
        elif 'mal' in tags and 'test' in tags:
            dbName = dbMalTest
        elif 'nor' in tags and 'train' in tags:
            dbName = dbNorTrain
        elif 'nor' in tags and 'test' in tags:
            dbName = dbNorTest
        # t = ThreadUtils.MyThread(uploadTracesDB,args=(value, dbName, upDBbin))
        # t.start()
        uploadTracesDB(value, dbName, upDBbin)
    print('fucking done!')





    
