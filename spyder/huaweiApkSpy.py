import requests
import os
import sys
import argparse
from datetime import datetime
from lxml import etree


pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules import SpyderUtils
from modules import FileUtils
from modules import CollectionUtils

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument("-a", "--start", help="filter size", nargs='?',type=int, default=10000000)
    parser.add_argument('-e', '--end', help='app name', nargs='?',type=int, default=10100000)
    parser.add_argument('-d', '--dir', help='app name', nargs='?',default='./')
    args = parser.parse_args() 
    startIdx=args.start
    endIdx=args.end
    basedir = args.dir

    myUrl = 'https://appstore.huawei.com/app/C'+'100749001'
    resDict = {}
    todayPath = basedir+'/todayList.txt'
    resDictPath = basedir+'/resDict.txt'
    todayList = []
    FileUtils.mkdir(basedir)
    date = datetime.now()
    datester = date.strftime('%Y-%m-%d')
    print 'today:'
    print datester

    s = SpyderUtils.getUrlTextEtree(myUrl)
    upTime = s.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[1]/ul[2]/li[2]/span')
    t1 =s.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[1]/ul[1]/li[2]/p[1]/span[1]')
    print upTime[0].text
    print t1[0].text