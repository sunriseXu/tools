#coding=utf-8
from modules import FileUtils
from modules import CollectionUtils

from modules import RexUtils
from modules import AdbUtils
from modules import ApkUtils
from modules.FileUtils import EasyDir
import os
import shutil
import random
import logging
import sys
from rooms.FileRoom import *

logging.basicConfig()
l = logging.getLogger("playground")



if __name__ == "__main__":
    # # 对目标目录下的pkgList文件通过hash-pkg字典进行转换，变成对应的hashList文件，写入目标目录，两个字典文件也需要在目标目录下
    # pkg2HashInDir('C:\\Users\\limin\\Desktop\\v1pkg',r'v1_train_nor',False)
    # pkg2HashInDir('C:\\Users\\limin\\Desktop\\v1pkg',r'v1.*?mal',True)
    
    # # 读取目标目录下的所有hashList文件，并且计算list之间的交集 并集 差集
    # pkgDir = EasyDir('C:\\Users\\limin\\Desktop\\v1pkg')
    # pkgPathDict = pkgDir.getAbsPathDict()
    # v1TrainMal = FileUtils.readList(pkgPathDict['v1_train_mal_hash'])
    # v1TestMal = FileUtils.readList(pkgPathDict['v1_test_mal_hash'])
    # v1TrainNor = FileUtils.readList(pkgPathDict['v1_train_nor_hash'])
    # v1TestNor = FileUtils.readList(pkgPathDict['v1_test_nor'])
    # v2TrainMal = FileUtils.readList(pkgPathDict['v2_train_mal'])
    # v2TestMal = FileUtils.readList(pkgPathDict['v2_test_mal'])
    # v2TrainNor = FileUtils.readList(pkgPathDict['v2_train_nor'])
    # v2TestNor = FileUtils.readList(pkgPathDict['v2_test_nor'])
    # test1 = v1TrainMal+v1TestMal
    # print len(test1)
    # test2 =  v2TrainMal+v2TestMal
    # print len(test2)
    # print len(CollectionUtils.listIntersection(test1,test2))
    
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

    # 在所有normal trace的文件夹下, 包含v1 所有上传到数据库的列表, 筛选出v2列表和文件夹
    myDir = EasyDir('/home/limin/Desktop/allHashInDb')
    dirDict = myDir.getAbsPathDict()
    v1_test_mal = FileUtils.readList(dirDict['v1_test_malicious500_201907221211.csv'])
    v1_test_nor = FileUtils.readList(dirDict['v1_test_normal5000_201907221220.csv'])
    v1_train_mal = FileUtils.readList(dirDict['v1_train_malicious2000_201907221216.csv'])
    v1_train_nor = FileUtils.readList(dirDict['v1_train_nor_Hash.csv'])
    v2_test_mal = FileUtils.readList(dirDict['v2_test_malicious500_201907220955.csv'])
    v2_test_nor = FileUtils.readList(dirDict['v2_test_normal5000_2_201907220950.csv'])
    v2_train_mal = FileUtils.readList(dirDict['v2_train_malicious2000_201907220955.csv'])
    v2_train_nor = FileUtils.readList(dirDict['v2_train_normal20000_2_201907220953.csv'])
    all_list = [v1_test_mal,v1_test_nor,v1_train_mal,v1_train_nor,v2_test_mal,v2_test_nor,v2_train_mal,v2_train_nor]
    # print all_list[2]
    for i in range(0,len(all_list)):
        all_list[i] = [item.strip('"') for item in all_list[i]]
        print len(all_list[i])
    # all_mal_dict = FileUtils.readDict(dirDict['allNorDict.txt'])
    # all_mal_dict=dict(zip(all_mal_dict.values(), all_mal_dict.keys()))
    # v1_train_nor = pkg2Hash(all_list[3],all_mal_dict)
    # all_list[3]  = v1_train_nor
    # FileUtils.writeList(v1_train_nor, myDir.getCatPath('v1_train_nor_Hash.csv'))
    v1_test_mal = all_list[0]
    v1_test_nor = all_list[1]
    v1_train_mal = all_list[2]
    v1_train_nor = all_list[3]
    v2_test_mal = all_list[4]
    v2_test_nor = all_list[5]
    v2_train_mal = all_list[6]
    v2_train_nor = all_list[7]
    
    v1_mal_list = v1_train_mal + v1_test_mal
    v2_mal_list = v2_train_mal + v2_test_mal

    FileUtils.writeList(v1_mal_list, myDir.getCatPath('v1_mal.txt'))
    FileUtils.writeList(v2_mal_list, myDir.getCatPath('v2_mal.txt'))

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

    

