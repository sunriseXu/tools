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
import pymysql
import re
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

def uploadTracesDB(myDir, ipAndPort,dbName,account,passwd,tableName, upDBbin, debug=False):
    upCmd = 'java -jar %s -f %s -i %s -d %s -u %s -s %s -t %s' \
            % (upDBbin, myDir,ipAndPort,dbName,account,passwd,tableName)
    l.warning('uploadCmd: %s', upCmd)
    res = ThreadUtils.execute_command(upCmd,debug=True)
    print('uploading thread done ..')
    if debug:
        print(res)
def table_exists(con,table_name):
    sql = "show tables;"
    con.execute(sql)
    tables = [con.fetchall()]
    table_list = re.findall('(\'.*?\')',str(tables))
    table_list = [re.sub("'",'',each) for each in table_list]
    if table_name in table_list:
        return 1
    else:
        return 0

def createTable(tableName):
    
    # 打开数据库连接
    #10.141.209.138:6603 -d antivirus -u antivirus -s antivirus -t test2NorTest
    db = pymysql.connect(host="10.141.209.138",port=6603,user="antivirus",password="antivirus",database="antivirus" )
    # 使用 cursor() 方法创建一个游标对象 cursor
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL，如果表存在则删除
    cursor.execute("DROP TABLE IF EXISTS {}".format(tableName))
    # 使用预处理语句创建表
    sql = """create table {}
        (
        GUID      varchar(255) not null,
        pkgName   varchar(255) not null,
        timestamp varchar(255) not null,
        ActionID  int          not null
        )""".format(tableName)
    print(sql)
    cursor.execute(sql)
    print("CREATE TABLE OK")
    # 关闭数据库连接
    db.close()
# 1.首先每日下载app在凌晨进行，然后测试app在每日7点开始
# python3 huaweiSpy.py && python3 downloadApk.py
# 定时完成测试 完成 检查下载是否完成
# 2.需要检查下载是否完成，

# 3.测试app也是由每日定时任务完成
# 本意是有一个配置文件,写好每一类的测试总数,可用测试机,以及每台手机的测试速度,
# 用以计算每一类是否需要分批测试,指定分批测试数量,如果大于1,那么就分批次进行测试,同样得,有8类
# 定时任务,每个小时完成一次测试,每次测试20个apk文件
# 4. trace的筛选上传到数据库，数据库可以批量建好
# 筛选脚本用一键脚本好了,但是需要生成配置文件,有点繁琐啊,不过也没有什么关系呢? python如何生成配置文件?

# 5.然后用脚本进行测试，这个怎么测试呢有点问题啊
    # 完成
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument('-d', '--workdir', help='config file path', nargs='?', default="")
    parser.add_argument('-i', '--ipAndPort', help='ip:port', nargs='?', default="")
    parser.add_argument('-b', '--dbname', help='db name', nargs='?', default="")
    parser.add_argument('-u', '--user', help='user name', nargs='?', default="")
    parser.add_argument('-s', '--passwd', help='passwd name', nargs='?', default="")
    parser.add_argument('-t', '--tablename', help='table name', nargs='?', default="")

    args = parser.parse_args()



    wkPath = args.workdir
    ipAndPort = args.ipAndPort
    dbName = args.dbname
    account = args.user
    passwd = args.passwd
    tableName = args.tablename
    upDBbin='/home/limin/Desktop/filterAnduploadBin/logUpload.jar'

    pwd = os.path.dirname(os.path.realpath(__file__))
    abandonBin = os.path.join(pwd, 'examples/filterLog.py')

    wkDir = EasyDir(wkPath)
    wkDirDict = wkDir.getAbsPathDict()
    fileList = sorted(wkDirDict.keys())
    InteractUtils.showList(fileList)

    # 首先需要做的事情是把traces筛选出那些崩溃的和log过短的
    # 如果存在分批测试得情况,需要merge
    partPathList = []
    childPath = wkDirDict.values()
    traceDir = ""
    for cp in childPath:
        if os.path.isfile(cp):
            continue
        traceDir = os.path.join(cp, 'logs/traces')
        if os.path.exists(traceDir):
            partPathList.append(traceDir)
    if partPathList:
        mergedDir = os.path.join(wkPath, 'logs/traces')
        FileUtils.mkdir(mergedDir)
        for pp in partPathList:
            ppItems = FileUtils.listDir(pp)
            FileUtils.listCopy2(ppItems, mergedDir)
        print('Merge %s done!' %wkPath)

    print("wkpath "+wkPath)
    tracesDir = wkPath+'/logs/traces'
    print("tracesDir:"+tracesDir)
    
    allTraceList = FileUtils.listDir3(tracesDir)
    shortOrInvalidPath = os.path.join(wkPath, 'shortInvalid.txt')
    shortOrInvalidDir = os.path.join(wkPath, 'shortInvalid')
    validDir = os.path.join(wkPath, 'valid')
    FileUtils.mkdir(shortOrInvalidDir)
    FileUtils.mkdir(validDir)

    abandomCmd = 'python %s -d %s -b %s' % (abandonBin, tracesDir, shortOrInvalidPath)

    ThreadUtils.execute_command(abandomCmd)
    shortOrInvalidList = FileUtils.readList(shortOrInvalidPath)
    validList = CollectionUtils.listDifference(allTraceList, shortOrInvalidList)
    shortOrInvalidList = CollectionUtils.graftListItem(shortOrInvalidList, tailStr='.txt')
    validList = CollectionUtils.graftListItem(validList, tailStr='.txt')
    FileUtils.listCopy(shortOrInvalidList, tracesDir, shortOrInvalidDir)
    FileUtils.listCopy(validList, tracesDir, validDir)
    # 所有的筛选都完成了，接下来，将normal为通过rule的样本随机挑选对应的数量拷贝到特定目录上传到数据库

    uploadTracesDB(tracesDir,ipAndPort,dbName,account,passwd,tableName, upDBbin)







