#coding=utf-8
from modules import FileUtils
from modules import CollectionUtils

from modules import RexUtils
from modules import AdbUtils
from modules import ApkUtils
from modules import FileUtils
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
from multiprocessing import Process
from multiprocessing import Pool
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
    # res = AdbUtils.getApkPermission('/home/limin/Desktop/malware/cou-qqpiliang.apk','uses-permission: name=')
    # print(res)


    def getPermissionList(myDir):
        haveList = []
        noList = []
        pathList = FileUtils.listDir(myDir)
        idx = 0
        for apkPath in pathList:
            idx+=1
            # if idx>1000:
            #     break
            apkHash = FileUtils.getFileName(apkPath)
            res = AdbUtils.getApkPermission(apkPath, 'uses-permission: name=')
            if not res:
                print('%s dont have permission' %apkPath)
                continue
            if 'android.permission.INTERNET' in res:
                haveList.append(apkHash)
            elif 'ERROR_DUMP' in res:
                print('%s dumpError!' %apkPath)
            else:
                noList.append(apkHash)
        return haveList,noList
    def getPermissionListLen(myDir):
        haveList, noList = getPermissionList(myDir)
        haveLen = len(haveList)
        noLen = len(noList)
        return haveLen,noLen
    # print('haveList length: %d' %len(haveList))
    # print('noList length: %d' %len(noList))

    # myDir = '/home/limin/Desktop/apks/huawei/todayApk-2019-08-15'
    # haveLen, noLen = getPermissionListLen(myDir)
    # print('haveList length: %d' %haveLen)
    # print('noList length: %d' %noLen)
    #
    # DirList = [
    #     '',
    #     '',
    #
    # ]

    # mydir = '/home/limin/Desktop/v4Log/v1Test/malpayTrain667/noRule'
    # noruleList = FileUtils.listDir3(mydir)
    # print(noruleList)
    #
    # destPath = '/home/limin/Desktop/v4Log/v1Test/malpayTrain667/norule.txt'
    # FileUtils.writeList(noruleList,destPath)
    # partNum = 2
    # originPath = '/home/limin/Desktop/v1pkg/aa/split3/v2NorTrainPart4.txt'
    # originList = FileUtils.readList(originPath)
    # print(len(originList))
    #
    #
    #
    # errorPath = '/home/limin/Desktop/v4Log/v2/norTrain20000/part4/logs/error.txt'
    # errorList = FileUtils.readList(errorPath)
    # print(len(errorList))
    #
    # notInstallPath = '/home/limin/Desktop/v4Log/v2/norTrain20000/part4/logs/notInstalled.txt'
    # notInstallList = FileUtils.readList(notInstallPath)
    # print(len(notInstallList))
    #
    # testedPath = '/home/limin/Desktop/v4Log/v2/norTrain20000/part4/logs/lastTest.txt'
    # testedList = FileUtils.readList(testedPath)
    # print(len(testedList))
    #
    # testedList = testedList+errorList+notInstallList
    # diffList = CollectionUtils.listDifference(originList,testedList)
    # print("difflen:")
    # print(len(diffList))
    # difflen = len(diffList)
    # half = difflen / 2
    # part1 = random.sample(diffList,half)
    # part2 = CollectionUtils.listDifference(diffList,part1)
    # print('part1 && part 2')
    # # print(len(CollectionUtils.listIntersection(part1,testedList)))
    # p5Path = '/home/limin/Desktop/v4Log/v2/norTrain20000/part7.txt'
    # p6Path = '/home/limin/Desktop/v4Log/v2/norTrain20000/part8.txt'
    # FileUtils.writeList(part1,p5Path)
    # FileUtils.writeList(part2,p6Path)

    # mydir = '/home/limin/Desktop/v4Log/v1Test/upDB/norTrain'
    # mydir = '/home/limin/Desktop/v4Extr/nortrain/dbToUp'
    # mypathList = FileUtils.listDir(mydir)
    #
    # timePath = '/home/limin/Desktop/v4Log/v1Test/timestamp.txt'
    # actionPath = '/home/limin/Desktop/v4Log/v1Test/action.txt'
    # uidPath = '/home/limin/Desktop/v4Log/v1Test/uid.txt'
    # timeInvalid = []
    # with open(timePath, "w") as f1,\
    #         open(actionPath, "w") as f2,\
    #         open(uidPath, "w") as f3:
    #     for mypath in mypathList:
    #         content = FileUtils.readList(mypath)
    #         for line in content:
    #             #time: 1567939248586, uid: 13846, method_id: 14001 Action_startProcessLocked
    #             if 'time' not in line or 'uid' not in line or 'method_id' not in line:
    #                 print(mypath + 'error in ' + line)
    #                 continue
    #             tmpList = line.split(',')
    #             if len(tmpList) < 3:
    #                 print(mypath + 'error in ' + line)
    #                 continue
    #             timestamp = tmpList[0].strip()
    #             # if len(timestamp
    #             timestamp = timestamp.split()
    #             if len(timestamp) != 2:
    #                 print(mypath+'error in '+line)
    #                 continue
    #             timestamp = timestamp[1].strip()
    #             # tmp = int(timestamp)
    #             # print(len(timestamp))
    #             if len(timestamp) < 13:
    #                 timeInvalid.append(os.path.basename(mypath))
    #
    #             uid = tmpList[1].strip()
    #             uid = uid.split()
    #             if len(uid) != 2:
    #                 print(mypath+'error in '+line)
    #                 continue
    #             uid = uid[1].strip()
    #             tmp = int(uid)
    #             mid = tmpList[2].strip()
    #             mid = mid.split()
    #             if len(mid) < 2:
    #                 print(mypath + 'error in ' + line)
    #                 continue
    #             mid = mid[1].strip()
    #             tmp = int(mid)
    #             f1.write(timestamp+'\n')
    #             f2.write(uid+'\n')
    #             f3.write(mid+'\n')
    # print 'hello?'
    # timeInvalid = list(set(timeInvalid))
    # InteractUtils.showList(timeInvalid)
    # part1dir = '/home/limin/Desktop/v4Log/v1/norTrain20000/part1/logs/traces'
    # part2dir = '/home/limin/Desktop/v4Log/v1/norTrain20000/part2/logs/traces'
    # part3dir = '/home/limin/Desktop/v4Log/v1/norTrain20000/part3/logs/traces'
    # part4dir = '/home/limin/Desktop/v4Log/v1/norTrain20000/part4/logs/traces'
    #
    # part1pathList = FileUtils.listDir2(part1dir)
    # part2pathList = FileUtils.listDir2(part2dir)
    # part3pathList = FileUtils.listDir2(part3dir)
    # part4pathList = FileUtils.listDir2(part4dir)
    #
    # p1 = []
    # p2 = []
    # p3 = []
    # p4 = []
    # for t in timeInvalid:
    #     if t in part1pathList:
    #         p1.append(t)
    #     elif t in part2pathList:
    #         p2.append(t)
    #     elif t in part3pathList:
    #         p3.append(t)
    #     elif t in part4pathList:
    #         p4.append(t)
    #     else:
    #         print(t+' no found')
    # print('part1 len: '+str(len(p1)))
    # print('part2 len: ' + str(len(p2)))
    # print('part3 len: ' + str(len(p3)))
    # print('part4 len: ' + str(len(p4)))
    #
    # p1 = CollectionUtils.trimListItem(p1,unTailStr='.txt')
    # p2 = CollectionUtils.trimListItem(p2,unTailStr='.txt')
    # FileUtils.writeList(p1,'/home/limin/Desktop/v4Log/v1/norTrain20000/p1_wrongTime.txt')
    # FileUtils.writeList(p2, '/home/limin/Desktop/v4Log/v1/norTrain20000/p2_wrongTime.txt')

    # p1 = '/home/limin/Desktop/v1pkg/aa/split3/v1NorTrain20000.txt'
    # p2 = '/home/limin/Desktop/v1pkg/aa/split3/v1NorTest5000.txt'
    # p3 = '/home/limin/Desktop/v1pkg/aa/split3/v2NorTrain20000.txt'
    # p4 = '/home/limin/Desktop/v1pkg/aa/split3/v2NorTest5000.txt'
    #
    # list1 = FileUtils.readList(p1)
    # list2 = FileUtils.readList(p2)
    # list3 = FileUtils.readList(p3)
    # list4 = FileUtils.readList(p4)
    #
    # p5 = '/home/limin/Desktop/apks/huawei/20190515_all'
    # list5 = FileUtils.listDir3(p5)
    # resList = CollectionUtils.listDifference(list5, list1+list2+list3+list4)
    #
    # FileUtils.writeList(resList,'/home/limin/Desktop/exceptv1v2.txt')
    #拷贝apk
    # v1MalTest = FileUtils.readList('totest/v4pkgname/v4db/v1MalTest.txt')
    # v1MalTrain = FileUtils.readList('totest/v4pkgname/v4db/v1MalTrain.txt')
    # v2MalTest = FileUtils.readList('totest/v4pkgname/v4db/v2MalTest.txt')
    # v2MalTrain = FileUtils.readList('totest/v4pkgname/v4db/v2MalTrain.txt')
    # v1NorTest = FileUtils.readList('totest/v4pkgname/v4db/v1NorTest.txt')
    # v2NorTest = FileUtils.readList('totest/v4pkgname/v4db/v2NorTest.txt')
    # #
    # cpApkList = v2NorTest
    # destDir = '/home/xjchi/apks/huawei/v2NorTest'
    # FileUtils.mkdir(destDir)
    # cpApkList = CollectionUtils.graftListItem(cpApkList, tailStr='.apk')
    # #
    # dirList = [
    #     '/home/xjchi/apks/huawei/20190515_all',
    #     '/home/xjchi/apks/huawei/201902_all',
    #     ]
    # allFileList = []
    # for mydir in dirList:
    #     allFileList = allFileList + FileUtils.listDirRecur(mydir)
    # print(len(allFileList))
    # rex = r'.*?\.apk'
    # for item in allFileList:
    #     res = RexUtils.rexFind(rex, item)
    #     if not res:
    #         allFileList.remove(item)
    # print(len(allFileList))
    # apkDict = {}
    # rex = r'/([^/]*?\.apk)'
    # for item in allFileList:
    #     res = RexUtils.rexFind(rex, item)
    #     if not res:
    #         print item
    #     else:
    #         bs = os.path.basename(item)
    #         apkDict[bs] = item
    # print(len(apkDict))
    # print(len(cpApkList))
    # for item in cpApkList:
    #     src = apkDict[item]
    #     dest = os.path.join(destDir,item)
    #     shutil.copy(src, dest)
#     /home/limin/Desktop/stage2_apk/apks/v1MalTest
#     v1MalTest = FileUtils.listDir3('/home/limin/Desktop/stage2_apk/apks/v1MalTest')
#     v2MalTest = FileUtils.listDir3('/home/limin/Desktop/stage2_apk/apks/v2MalTest')
#     v1NorTest = FileUtils.listDir3('/home/limin/Desktop/stage2_apk/apks/v1NorTest')
    # v2NorTest = FileUtils.listDir3('/home/limin/Desktop/stage2_apk/apks/v2NorTest')
#
#     FileUtils.writeList(v1MalTest,'/home/limin/Desktop/aaaa/v1MalTest.txt')
#     FileUtils.writeList(v2MalTest, '/home/limin/Desktop/aaaa/v2MalTest.txt')
#     FileUtils.writeList(v1NorTest, '/home/limin/Desktop/aaaa/v1NorTest.txt')
#     FileUtils.writeList(v2NorTest, '/home/limin/Desktop/aaaa/v2NorTest.txt')

    # rule137 = FileUtils.readList('/home/limin/Documents/jianguoyun/Nutstore/shareTemp/ruled137.txt')
    # print(len(rule137))
    # rule137 = CollectionUtils.trimListItem(rule137,unTailStr='\r')
    # rule137 = CollectionUtils.graftListItem(rule137,'','.txt')
    # srcDir = '/home/limin/Desktop/v4Log/v1Test/norRuled/ruled'
    # destDir = '/home/limin/Desktop/v4Log/ruled137'
    # for i in rule137:
    #     src = os.path.join(srcDir,i)
    #     dest = os.path.join(destDir,i)
    #     shutil.copy(src,dest)
    # newV2NorTest = FileUtils.readList('/home/limin/Documents/jianguoyun/Nutstore/shareTemp/newV2NorTest.txt')

    # newV2NorTest = CollectionUtils.trimListItem(newV2NorTest,unTailStr='\r')
    # inter = CollectionUtils.listIntersection(v2NorTest,newV2NorTest)
    # print(len(inter))
    # toDe = CollectionUtils.listDifference(v2NorTest,newV2NorTest)
    # # print(toDe)

    # toAdd = CollectionUtils.listDifference(newV2NorTest,v2NorTest)
    # print(len(toAdd))
    #delete tode
    # toDe = CollectionUtils.graftListItem(toDe,tailStr='.apk')
    # src = '/home/limin/Desktop/stage2_apk/apks/v2NorTest'
    # for item in toDe:
    #     srcApk = os.path.join(src,item)
    #     os.remove(srcApk)

    #add toAdd
    # cpApkList = toAdd
    # destDir = '/home/limin/Desktop/stage2_apk/apks/v2NorTest'
    # cpApkList = CollectionUtils.graftListItem(cpApkList, tailStr='.apk')

    # dirList = [
    #     '/home/limin/Desktop/apks/huawei/20190515_all',
    #     '/home/limin/Desktop/apks/huawei/201902_all',
    #     ]
    # allFileList = []
    # for mydir in dirList:
    #     allFileList = allFileList + FileUtils.listDirRecur(mydir)
    # print(len(allFileList))
    # rex = r'.*?\.apk'
    # for item in allFileList:
    #     res = RexUtils.rexFind(rex, item)
    #     if not res:
    #         allFileList.remove(item)
    # print(len(allFileList))
    # apkDict = {}
    # rex = r'/([^/]*?\.apk)'
    # for item in allFileList:
    #     res = RexUtils.rexFind(rex, item)
    #     if not res:
    #         print item
    #     else:
    #         bs = os.path.basename(item)
    #         apkDict[bs] = item
    # print(len(apkDict))
    # print(len(cpApkList))
    # for item in cpApkList:
    #     src = apkDict[item]
    #     dest = os.path.join(destDir,item)
    #     shutil.copy(src, dest)
    # srcDir = '/home/limin/Desktop/tmpFp+fileman'
    # myList = FileUtils.listDir(srcDir)
    # destPath = '/home/limin/Desktop/v4Log/tmp.txt'
    # lines = ''
    # for item in myList:
    #     apkHash = os.path.basename(item)
    #     if '.apk' not in apkHash:
    #         continue
    #     packageName=AdbUtils.getApkInfo(item,"package: name=")
    #     apkName=AdbUtils.getApkInfo(item,"label=")
    #     print("apkHash:"+apkHash)
    #     print("pkgName:"+packageName)
    #     print("appName:"+apkName)
    #     line = '{}\t{}\t{}\n'.format(apkHash,packageName,apkName)
    #     lines+=line
    # FileUtils.writeFile(destPath,lines)
    # tmpdir = '/home/limin/Desktop/v4Log/v2Test/malrogTest167/dbToUp'
    # dest  = '/home/limin/Desktop/v2Rog167.txt'
    # todir = '/home/limin/Desktop/stage2_apk/apks/v2MalTest'
    # rest = '/home/limin/Desktop/v2MalTest500.txt'
    # myList = FileUtils.listDir3(tmpdir)
    # alllist = FileUtils.listDir3(todir)
    # # alllist = CollectionUtils.listDifference(alllist,myList)
    # print(len(alllist))
    # FileUtils.writeList(alllist,rest)
    # import subprocess
    # import time
    # antivirusOutPath = 'modelTest.txt'
    # filteredStr = 'ModelHandler'
    # logcmd = 'adb %s shell logcat -s "%s">>%s' %('-s D3H0117704000035',filteredStr,antivirusOutPath)
    # print logcmd
    # # logcmd=logcmd.strip().split()
    # modelHandler = subprocess.Popen(logcmd, shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # while True:
    #     print(modelHandler)
    #     time.sleep(3)

    20190515_all/C100638971.apk
    20190515_all/C100214101.apk
    20190515_all/C10275525.apk
    201902_all/C7272499.apk
    20190515_all/C100427563.apk
    20190515_all/C100302225.apk
    20190515_all/C100133529.apk 疑似关闭debug模式









    
