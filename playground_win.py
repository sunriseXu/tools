#coding=utf-8
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
logging.basicConfig()
l = logging.getLogger("playground")

def trimLog(uid,tmplogPath,newlogPath):
	f = open(tmplogPath,'r')
	emptyFlag=1
	fres=open(newlogPath,'w')
	line = f.readline()
	while line:
		myFilter="uid: "+uid
		if myFilter in line: 
			line_list=line.split("AntiVirusService: ")
			if line_list:
				emptyFlag=0
				fres.write(line_list[1])          
		line = f.readline()
	fres.close()
	if emptyFlag:
		os.remove(newlogPath)


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
    # dirname = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk28\\jsonRes'
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
    # FileUtils.writeList(permissionlist,'tmpOutO28.txt')
    # print 'class length'
    # print len(classList)
    # allDict = FileUtils.readDict('D:\\androidsdkdoc\\permission28.json')
    
    # partList = FileUtils.readList('tmpOutO28.txt')
    # resList = []
    # for permission in partList:
    #     tmp = ''
    #     for key,value in allDict.items():
    #         if permission in value:
    #             tmp = key+'\t'+permission +'\t' +' '.join(resDict[permission].keys())
    #             resList.append(tmp)
    # resList = sorted(resList)
    # FileUtils.writeList(resList, 'tmpOut28.txt')
    # FileUtils.writeDict()

    # list1 = FileUtils.readList('tmpOut.txt')
    # list2 = FileUtils.readList('tmpOutO24.txt')
    # print len(CollectionUtils.listIntersection(list1,list2))
    # res = CollectionUtils.listDifference(list2,list1)
    # InteractUtils.showList(res)
    #需要从normal中选出2000+200,从malware中选出500+50
    #v1 normal选一半
    # payList = FileUtils.listDir3('C:\\Users\\limin\\Desktop\\allMal\\malPayNo2\\ruled')
    # rogList = FileUtils.listDir3('C:\\Users\\limin\\Desktop\\allMal\\malRogNo2\\ruled')
    # stealList = FileUtils.listDir3('C:\\Users\\limin\\Desktop\\allMal\\malStealNo2\\ruled')

    # print('payList:')
    # print(len(payList))
    # print('rogList:')
    # print(len(rogList))
    # print("stealList")
    # print(len(stealList))

    # # 500+50 200 + 200 + 200 
    # # 30 + 30 + 30 rog: 25+5
    
    # v3_pay_train = random.sample(payList, 200)
    # v3_rog_train = random.sample(rogList, 200)
    # v3_steal_train = random.sample(stealList, 200)

    # print('v3_pay_train')
    # print(len(v3_pay_train))

    # print('v3_rog_train')
    # print(len(v3_rog_train))

    # print('v3_steal_train')
    # print(len(v3_steal_train))

    # print(len(CollectionUtils.listIntersection(v3_pay_train,v3_rog_train)))
    # print(len(CollectionUtils.listIntersection(v3_pay_train,v3_steal_train)))
    # print(len(CollectionUtils.listIntersection(v3_steal_train,v3_rog_train)))
    
    # v3_mal_train = v3_pay_train+v3_steal_train+v3_rog_train
    
    # payList = CollectionUtils.listDifference(payList,v3_pay_train)
    # rogList = CollectionUtils.listDifference(rogList,v3_rog_train)
    # stealList = CollectionUtils.listDifference(stealList, v3_steal_train)

    # v3_pay_test = random.sample(payList, 30)
    # v3_rog_test = random.sample(rogList, 30)
    # v3_steal_test = random.sample(stealList, 30)

    # v3_mal_test = v3_pay_test+v3_rog_test+v3_steal_test
    # print('v3_mal_train && v3_mal_test')
    # print(len(CollectionUtils.listIntersection(v3_mal_train,v3_mal_test)))

    # v3Dir = EasyDir('./totest/v3')
    # v3Dict = v3Dir.getAbsPathDict()

    # FileUtils.writeList(v3_pay_train,v3Dir.getCatPath('v3_pay_train'))
    # FileUtils.writeList(v3_rog_train,v3Dir.getCatPath('v3_rog_train'))
    # FileUtils.writeList(v3_steal_train,v3Dir.getCatPath('v3_steal_train'))
    # FileUtils.writeList(v3_pay_test,v3Dir.getCatPath('v3_pay_test'))
    # FileUtils.writeList(v3_rog_test,v3Dir.getCatPath('v3_rog_test'))
    # FileUtils.writeList(v3_steal_test,v3Dir.getCatPath('v3_steal_test'))


    # # 每类200 => 167  一共501
    # # 每类30 =>  17
    # def listInStr(myList, myStr):
    #     myStr = myStr.lower()
    #     for item in myList:
    #         if item not in myStr:
    #             # print('%s not in %s' %(item,myStr))
    #             return False
    #     # print('tags in %s' %(myStr))
    #     return True
    # def uploadTracesDB(myDir, dbName, upDBbin, debug=False):
        
    #     upCmd = 'java -jar %s -f %s -d %s' %(upDBbin, myDir, dbName)
    #     l.warning('uploadCmd: %s',upCmd)
    #     res = ThreadUtils.execute_command(upCmd)
    #     print('uploading thread done ..')
    #     if debug:
    #         print(res)

    # filterRuleBin = 'C:\\Users\\limin\\Desktop\\v3_log\\FeatureEngineeringTest.jar'
    # upDBbin = 'C:\\Users\\limin\\Desktop\\v3_log\\logUpload.jar'
    # wkDir = EasyDir('C:\\Users\\limin\\Desktop\\v3_log')
    
    # # jsonDir = EasyDir('C:\\Users\\limin\\Desktop\\androidSdkJsonClassName')
    # # jsonDict = jsonDir.getAbsPathDict()
    # # allList = []
    # # for key in jsonDict:
    # #     pa = jsonDict[key]
    # #     allList += FileUtils.readList(pa)
    # # res = sorted(list(set(allList)))
    # # print(len(res))
    # # FileUtils.writeList(res, jsonDir.getCatPath('mergedClassList.txt'))

    # jsonDir = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk28\\jsonRes'
    # # supportList = FileUtils.readList('C:\\Users\\limin\\Desktop\\totalClassList_support.txt')
    # # resDir = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\support24'
    # # FileUtils.mkdir(resDir)
    # jsonPaths = FileUtils.listDir(jsonDir)
    # resPath = 'C:\\Users\\limin\\Desktop\\alldesc\\all_description.txt'
    # with open(resPath,'a') as f:
    #     for item in jsonPaths:
    #         myDict = FileUtils.readDict(item)
    #         funcDict = myDict['Functions']
    #         tmpDesc = ''
    #         for funcName in funcDict:
    #             funcInfoDict = funcDict[funcName]
    #             desc = funcInfoDict['Description'].strip()
    #             if not desc:
    #                 continue
    #             f.writelines(desc.encode('utf-8').strip())
    #             f.writelines('\n')
    #             f.writelines('\n')
    #         f.flush()

    # fileList = FileUtils.listDir('C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk28\\jsonRes')
    # for item in fileList:
    #     content = FileUtils.readDict(item)
    
    # listPath = 'C:\\Users\\limin\\Desktop\\v4Log\\norule.txt'
    # norulelist = FileUtils.readList(listPath)

    # norulelist = CollectionUtils.graftListItem(norulelist,tailStr='.txt')

    # srcdir = 'C:\\Users\\limin\\Desktop\\v4Log\\v1\\payTrain667\\logs\\traces'
    # destdir = 'C:\\Users\\limin\\Desktop\\v4Log\\newv1PayTrain'
    # FileUtils.listCopy(norulelist,srcdir,destdir)

    # tDir = 'C:\\Users\\limin\\Desktop\\allMal'
    # myPathList = FileUtils.listDirRecur(tDir)
    # tmpList = []
    # for item in myPathList:
    #     if 'tmplog' in item or 'antivirusOut' in item or 'apkInfoDict' in item or \
    #         'lastTest' in item or 'notInstalled' in item or 'error' in item or\
    #             'tmpKlog' in item:
    #         continue
    #     if os.path.isfile(item):
    #         tmpList.append(item)
    # myPathList = tmpList
    # # method_id: 6004
    # allMethodIds = []
    # rex = r'method_id: (\d+) '
    # for mylog in myPathList:
    #     content = FileUtils.readFile(mylog)
    #     methodIds = RexUtils.rexFind(rex,content)
    #     methodIds = list(set(methodIds))
    #     allMethodIds = list(set(allMethodIds + methodIds)) 
    # resPath = 'C:\\Users\\limin\\Desktop\\v4Log\\allMethodIds_old_mal.txt'
    # FileUtils.writeList(allMethodIds, resPath)

    # dir1 = 'C:\\Users\\limin\\Desktop\\v4Log\\allMethodIds_old.txt'
    # dir2 = 'C:\\Users\\limin\\Desktop\\v4Log\\allMethodIds_new.txt'
    # dirList1 = FileUtils.readList(dir1)
    # dirList2 = FileUtils.readList(dir2)

    # print('old diff new:')
    # diffList = sorted(CollectionUtils.listDifference(dirList1,dirList2))
    # print diffList
    # FileUtils.writeList(diffList,'C:\\Users\\limin\\Desktop\\v4Log\\olddiffnew.txt')

    # print('new diff old:')
    # diffList = CollectionUtils.listDifference(dirList2,dirList1)
    # print diffList

    # FileUtils.writeList(tmpList,'C:\\Users\\limin\\Desktop\\v4Log\\allMethodIds_old.txt')

    # allSteal = FileUtils.listDir3('G:\\newMalware\\malSteal')

    # allMal1  = FileUtils.readList('C:\\Users\\limin\\Desktop\\v1pkg\\aa\\v1MalTest500.txt')
    # allMal2  = FileUtils.readList('C:\\Users\\limin\\Desktop\\v1pkg\\aa\\v1MalTrain2000.txt')
    # allMal3  = FileUtils.readList('C:\\Users\\limin\\Desktop\\v1pkg\\aa\\v2MalTest500.txt')
    # allMal4  = FileUtils.readList('C:\\Users\\limin\\Desktop\\v1pkg\\aa\\v2MalTrain2000.txt')
    # allMal = allMal1 + allMal2+allMal3+allMal4
    # diffList = CollectionUtils.listDifference(allSteal, allMal)
    # print(len(diffList))
    # FileUtils.writeList(diffList,'C:\\Users\\limin\\Desktop\\stealext.txt')
    # v1MalTest = FileUtils.readList('C:\\Users\\limin\\Desktop\\v1pkg\\v4db\\v1MalTest.txt')
    # v1MalTrain = FileUtils.readList('C:\\Users\\limin\\Desktop\\v1pkg\\v4db\\v1MalTrain.txt')
    # v2MalTest = FileUtils.readList('C:\\Users\\limin\\Desktop\\v1pkg\\v4db\\v2MalTest.txt')
    # v2MalTrain = FileUtils.readList('C:\\Users\\limin\\Desktop\\v1pkg\\v4db\\v2MalTrain.txt')

    # cpApkList = v2MalTest
    # destDir = 'C:\\Users\\limin\\Desktop\\apks\\v1MalTest'
    # cpApkList = CollectionUtils.graftListItem(cpApkList,tailStr='.apk')
    

    # dirList = [
    #     'G:\\malware',
    #     'G:\\newMalware',
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
    # flen = len('FC63850CF209FE54953BE035296630BC.apk')
    # # build map
    # apkDict = {}
    # rex = r'\\([^\\]*?\.apk)'
    # for item in allFileList:
    #     res = RexUtils.rexFind(rex, item)
    #     if not res:
    #         print item
    #     elif len(res[0])!=flen:
    #         print item
    #     else:
    #         bs = os.path.basename(item)
    #         apkDict[bs] = item

    # for item in cpApkList:
    #     src = apkDict[item]
    #     dest = os.path.join(destDir,item)
    #     shutil.copy(src, dest)
    # basedir = './0emptyDirs'
    # for i in range(0,1001):
    #     tmpdir = 'tmp_{}'.format(i)
    #     tmpdir = os.path.join(basedir,tmpdir)
    #     FileUtils.mkdir(tmpdir)
    # pkgD = EasyDir('C:\\Users\\limin\\Desktop\\aaaa')
    # pkgDict = pkgD.getAbsPathDict()
    # v1NorTrain = FileUtils.readList(pkgDict['v1NorTrain.txt'])
    # v1NorTest  = FileUtils.readList(pkgDict['v1NorTest.txt'])
    # v1MalTrain = FileUtils.readList(pkgDict['v1MalTrain.txt'])
    # v1MalTest  = FileUtils.readList(pkgDict['v1MalTest.txt'])
    # v2NorTrain = FileUtils.readList(pkgDict['v2NorTrain.txt'])
    # v2NorTest  = FileUtils.readList(pkgDict['v2NorTest.txt'])
    # v2MalTrain = FileUtils.readList(pkgDict['v2MalTrain.txt'])
    # v2MalTest  = FileUtils.readList(pkgDict['v2MalTest.txt'])

    # # print(len(v1NorTrain))
    # print(len(CollectionUtils.listIntersection(v2MalTrain,v1MalTest)))
    # v1apkMalTest = FileUtils.readList('F:\\aaaa\\v1MalTest.txt')
    # v2apkMalTest = FileUtils.readList('F:\\aaaa\\v2MalTest.txt')
    # v1apkNorTest = FileUtils.readList('F:\\aaaa\\v1NorTest.txt')
    # v2apkNorTest = FileUtils.readList('F:\\aaaa\\v2NorTest.txt')
    # print(len(CollectionUtils.listIntersection(v2apkNorTest,v2NorTest)))

    # pkgD = EasyDir('C:\\Users\\limin\\Desktop\\aaaa')
    # pkgDict = pkgD.getAbsPathDict()
    # norRuled = FileUtils.readList(pkgDict['norRuled.txt'])
    # v2NorTest  = FileUtils.readList(pkgDict['v2NorTest.txt'])
    # v2deleteFp = FileUtils.readList(pkgDict['v2deleteFp.txt'])
    # v2New = FileUtils.readList('C:\\Users\\limin\\Desktop\\newV2NorTest.txt')
    # v2NorTest = CollectionUtils.trimListItem(v2NorTest,unTailStr='\r')
    # v2New = CollectionUtils.trimListItem(v2New,unTailStr='\r')
    # print(len(norRuled))
    # print(len(v2NorTest))
    # print(len(v2deleteFp))
    # print(len(CollectionUtils.listIntersection(v2NorTest, v2New)))
    # print('done')
    # print(len(v2NorTest))
    # delete124 = random.sample(v2NorTest,124)
    # print(len(delete124))
    # delete from test2NorTest where pkgName="C100188771";
    # qString = ''
    # for i in delete124:
    #     qString += 'delete from test2NorTest where pkgName="{}";\n'.format(i)
    # FileUtils.writeFile('C:\\Users\\limin\\Desktop\\aaaa\\query.txt',qString)
    # ruled136 = random.sample(norRuled,137)
    # print(len(CollectionUtils.listIntersection(ruled136,v2NorTest)))
    # FileUtils.writeList(ruled136,'C:\\Users\\limin\\Desktop\\aaaa\\ruled137.txt')

    def findMatchedPath(className,fileList):
        packages = className.split('.')
        res = []
        for file in fileList:
            findFlag = True
            for package in packages:
                if package not in file:
                    findFlag = False
                    break
            if findFlag:
                res.append(file)
        return res
    def findDex(className, myDirs, cacheDir=''):
        '''
        className是要找的类的全称，myDir是解包后的目录，
        cacheDir是缓存目录（如果多次运行，那么直接从缓存中取结果）
        cache目录只缓存myDir对应的结果，并且一一对应
        myDir唯一的标准是创建时间，而非修改时间
        '''
        fileList = []
        for myDir in myDirs:
            tmpList = []
            #if cacheDir exist
            if cacheDir:
                dirName = os.path.basename(myDir)
                createTime = str(os.path.getctime(myDir))
                cacheName = dirName+'-'+createTime+'.txt'
                myCacheFile = os.path.join(cacheDir,cacheName)
                if os.path.exists(myCacheFile):
                    # read txt file to list
                    tmpList = FileUtils.readList(myCacheFile)
                else:
                    tmpList = FileUtils.listDirRecur(myDir)
                    #write to cache file
                    FileUtils.writeList(tmpList, myCacheFile)
            else:
                tmpList = FileUtils.listDirRecur(myDir)
            fileList.extend(tmpList)
        # now fileList contains all path string
        resPathList = findMatchedPath(className,fileList)
        return resPathList
    

    className = 'com.tencent.mm.model.az'
    myDirs = [
        'F:\\vxp\\wechat707'
    ]
    cacheDir = 'C:\\Users\\limin\\Desktop\\tmp'
    res = findDex(className,myDirs,cacheDir)
    InteractUtils.showList(res)
    
                    



        




    
    


    
