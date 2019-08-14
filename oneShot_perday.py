# coding=utf-8
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
import argparse
from datetime import datetime
from multiprocessing import Process
from multiprocessing import Pool
from configparser import ConfigParser

logging.basicConfig()
l = logging.getLogger("playground")


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
    res = ThreadUtils.execute_command(upCmd,debug=True)
    print('uploading thread done ..')
    if debug:
        print(res)
# 1.首先每日下载app在凌晨进行，然后测试app在每日7点开始
python3 huaweiSpy.py && python3 downloadApk.py
定时完成测试 完成 检查下载是否完成
# 2.需要检查下载是否完成，

# 3.测试app也是由每日定时任务完成
本意是有一个配置文件,写好每一类的测试总数,可用测试机,以及每台手机的测试速度,
用以计算每一类是否需要分批测试,指定分批测试数量,如果大于1,那么就分批次进行测试,同样得,有8类
定时任务,每个小时完成一次测试,每次测试20个apk文件
# 4. trace的筛选上传到数据库，数据库可以批量建好
筛选脚本用一键脚本好了,但是需要生成配置文件,有点繁琐啊,不过也没有什么关系呢? python如何生成配置文件?

# 5.然后用脚本进行测试，这个怎么测试呢有点问题啊
    # 完成
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument('-c', '--config', help='config file path', nargs='?', default="")
    parser.add_argument('-d', '--dest', help='app name', nargs='?', default="")
    parser.add_argument('-i', '--num', help='test time', nargs='?', type=int, default=10)
    args = parser.parse_args()
    configPath = args.config
    copyNum = args.num
    destDir = args.dest

    cfg = ConfigParser()
    cfg.read(configPath)

    pwd = os.path.dirname(os.path.realpath(__file__))

    abandonBin = os.path.join(pwd,'examples/filterLog.py')
    filterRuleBin = cfg.get('execute','filterRuleBin')
    upDBbin = cfg.get('execute', 'upDBbin')
    wkPath = cfg.get('directory','working')

    malTrainAmount = cfg.getint('amount','malTrainAmount')
    malTestAmount = cfg.getint('amount','malTestAmount')
    norTrainAmount = cfg.getint('amount','norTrainAmount')
    norTestAmount = cfg.getint('amount','norTestAmount')
    singleMalTrainAmount = malTrainAmount / 3 + 1
    singleMalTestAmount = malTestAmount / 3 + 1

    dbMalTrain = cfg.get('database','dbMalTrain')
    dbMalTest = cfg.get('database','dbMalTest')
    dbNorTrain = cfg.get('database','dbNorTrain')
    dbNorTest = cfg.get('database','dbNorTest')

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
    wkDir = EasyDir(wkPath)
    wkDirDict = wkDir.getAbsPathDict()
    fileList = sorted(wkDirDict.keys())
    InteractUtils.showList(fileList)

    '''
    初始化各个目录的字典
    '''
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

    '''
        [!] 顺序:紧接上一个block执行完成才能到这里
        将各个目录下分段测试的合成一个段,这里牵扯到另一个问题,测试之前如何分段
        [!] 多进程:当循环内部是计算密集型,那么多进程更好
        [!] 多线程:由于循环内部是IO密集型操作,所以多线程更加适合
    '''
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
    '''
        [!] 顺序:紧接上一个block执行完成才能到这里
        将各个目录用rule进行筛选,并且将筛选后的数据挑选一些放入特定文件夹
        [!] 多进程:当循环内部是计算密集型,那么多进程更好
        [!] 多线程:由于循环内部是IO密集型操作,所以多线程更加适合
        修改:
        for key in configDict:
            pass
    '''
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

        if noRuleList:
            abandomCmd = 'python %s -d %s -b %s' % (abandonBin, noruleDir, shortOrInvalidPath)
            ThreadUtils.execute_command(abandomCmd)
            shortOrInvalidList = FileUtils.readList(shortOrInvalidPath)
            shortOrInvalidList = CollectionUtils.graftListItem(shortOrInvalidList, tailStr='.txt')
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
        FileUtils.cleanAndMkdir(dbDir)
        FileUtils.writeList(dbList, dblistPath)
        FileUtils.listCopy(dbListG, selectSource, dbDir)


    '''
        [!] 顺序:紧接上一个block执行完成才能到这里
        将各个目录下特定文件夹进行合并,然后开多进程,将数据传入数据库
        [!] 多进程:当循环内部是计算密集型,那么多进程更好
        [!] 多线程:由于循环内部是IO密集型操作,所以多线程更加适合
        修改:
            for key in configDict:
                pass
    '''
    # Now, merge all dbdir to upload
    DBDir = wkDir.getCatPath('upDB')
    FileUtils.mkdir(DBDir)
    dbDirObj = EasyDir(DBDir)
    malTrainDir = FileUtils.cleanAndMkdir(dbDirObj.getCatPath('malTrain'))
    malTestDir = FileUtils.cleanAndMkdir(dbDirObj.getCatPath('malTest'))
    norTrainDir = FileUtils.cleanAndMkdir(dbDirObj.getCatPath('norTrain'))
    norTestDir = FileUtils.cleanAndMkdir(dbDirObj.getCatPath('norTest'))
    doMergeFlag = True
    poolLen = len(configDict.keys())
    myPool = Pool(poolLen)
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
        destDir = ''
        if 'mal' in tags and 'train' in tags:
            destDir = malTrainDir
        elif 'mal' in tags and 'test' in tags:
            destDir = malTestDir
        elif 'nor' in tags and 'train' in tags:
            destDir = norTrainDir
        elif 'nor' in tags and 'test' in tags:
            destDir = norTestDir
        myPool.apply_async(FileUtils.copytree, args=(dbDir, destDir,))
    myPool.close()
    myPool.join()

    '''
        [!] 顺序:紧接上一个block执行完成才能到这里
        将各个目录下特定文件夹进行合并,然后开多进程,将数据传入数据库
        [!] 多进程:当循环内部是计算密集型,那么多进程更好
        [!] 多线程:由于循环内部是IO密集型操作,所以多线程更加适合
        今天我传数据库特别慢,比我自己手动跑上传脚本还慢,有问题,后来发现是数据库很慢
        同学在大量读写数据库
        修改:
            for key in configDict:
                pass
    '''
    dbDirObj.updateDir()
    dbDirDict = dbDirObj.getAbsPathDict()
    poolLen = len(dbDirDict.keys())
    myPool = Pool(poolLen)
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
        # multiprocess
        myPool.apply_async(uploadTracesDB, args=(value, dbName, upDBbin,))
    print('Waiting for all subprocesses done...')
    myPool.close()
    myPool.join()
    print('done!')






