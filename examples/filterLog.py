# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os
import json
import shutil
import sys
import argparse

pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules.FileUtils import *

def trimLog(logPath):
    '''
    get all actionId, return list
    '''
    allLines=[]
    with open(logPath) as f:
        allLines=f.readlines()
    actionIdList=[]
    for line in allLines:
        actionId=''
        line = line.strip()
        if not line:
            continue
        line=line.split('method_id:')[1]
        actionId=line.strip().split()[0]
        actionIdList.append(actionId)
    return actionIdList

# 1.首先，去掉无效的log：包含的 进程启动 action过多
# 2.再通过rulebase过滤，因为trace很短可能也包含恶意行为
# 3.无法通过rule的log再根据大小过滤：10条trace的log去掉
	
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument("-s", "--filtersize", help="filter size", action="store_true")
    parser.add_argument('-d', '--dirname', help='dir name', nargs='?')
    args = parser.parse_args() 

    logsDir = args.dirname
    filterSize=args.filtersize

    desktopDir=os.path.join(os.path.expanduser("~"), 'Desktop')
    abondonedPath=desktopDir+'/abandon.txt'

    startActionId='14001'
    myWindow=10
    maxlen=9
    logsList=listDir(logsDir,'')
    abandonedList=readList(abondonedPath)
    for logPath in logsList:
        logName=os.path.basename(logPath)
        actionIdList=trimLog(logPath)
        if not filterSize:                       
            maxcount=0
            icount=0
            gap=0
            flag=True
            inGap=False
            for actionId in actionIdList:
            
                if startActionId in actionId:
                    flag=False
                    inGap=False
                    icount+=1
                    gap=0
                else:
                    if flag and (not inGap):
                        gap+=1
                    flag=True
                if gap>=myWindow-1:
                    if icount>maxcount:
                        maxcount=icount
                    icount=0
                    gap=0
                    inGap=True
            maxcount=icount

            if maxcount > maxlen:
                abandonedList.append(logName)
        else:
            if len(actionIdList)<10:
                abandonedList.append(logName)
    # print abandonedList
    writeList(abandonedList,abondonedPath)

    