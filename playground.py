#coding=utf-8
from modules import FileUtils
from modules import CollectionUtils

from modules import RexUtils
from modules import AdbUtils
from modules import ApkUtils
from modules.FileUtils import EasyDir
from modules import SpyderUtils
import os
import shutil
import random
import logging
import sys
from rooms.FileRoom import *
from datetime import datetime
logging.basicConfig()
l = logging.getLogger("playground")



if __name__ == "__main__":
    # # 对目标目录下的pkgList文件通过hash-pkg字典进行转换，变成对应的hashList文件，写入目标目录，两个字典文件也需要在目标目录下
    # pkg2HashInDir('C:\\Users\\limin\\Desktop\\v1pkg',r'v1_train_nor',False)
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
    
    hashListPath1 = '/mnt/apk/huawei/md5_201902.log'
    hashListPath2 = '/mnt/apk/huawei/md5_201905.log'
    reportsDir = '/mnt/apk/huawei/reports_normal'
    hashApkNameDictPath = './norhashApkNameDict.txt'
    positiveDictPath = './positiveDictNor.json'

    hashList1 = FileUtils.readList(hashListPath1)
    hashList2 = FileUtils.readList(hashListPath2)
    print len(hashList1)
    print len(hashList2)
    print len(hashList1)+len(hashList2)
    hashList = list(set(hashList1 + hashList2))
    print len(hashList)
    hashApkNameDict = {}
    positiveDict={}

    for item in hashList:
        itemList = item.split()
        myHash = itemList[0].strip()
        apkName = itemList[1].strip().strip('\r')
        print myHash,apkName
        if myHash not in hashApkNameDict:
            hashApkNameDict.update({myHash:apkName})
    FileUtils.writeDict(hashApkNameDict, hashApkNameDictPath)
    print 'write hashapkName done!'
    for key, value in hashApkNameDict.items():
        apkHash = key
        jsonName = key+'.json'
        jsonPath = os.path.join(reportsDir,jsonName)
        print jsonPath
        positivesCount = -1
        firstSeen = ''
        if os.path.exists(jsonPath):
            jsonDict = FileUtils.readDict(jsonPath)
            positivesCount = jsonDict['positives']
            firstSeen = jsonDict['first_seen']
        if apkHash not in positiveDict:
            positiveDict.update({apkHash:[positivesCount, firstSeen]})
    FileUtils.writeDict(positiveDict, positiveDictPath)


