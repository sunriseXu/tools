#coding=utf-8
import io
import json
import argparse 
import os
import sys
import subprocess
import time
import multiprocessing
import threading
import logging
import re
import traceback 
import datetime
import xml.dom.minidom as xmldom
from modules.xmlTest import *
from modules.FileUtils import *
from modules.CollectionUtils import *
from modules.ThreadUtils import *
from modules.AdbUtils import *
from multiprocessing import Process, Manager
from multiprocessing import Pool
# K_AntiVirusService: time: 1567510830141, uid: 10014, action: Kernel_Action:100,sys_open, filename: /storage/emulated/0/DCIM/.thumbnails
def trimLog(uid,tmplogPath,newlogPath):
	f = open(tmplogPath,'rb')
	emptyFlag=1
	fres=open(newlogPath,'w')
	line = f.readline()
	while line:
		line = str(line).strip()
		myFilter="uid: "+uid
		myFilter2 = 'AntiVirusService: time:'
		myFileter3 = 'Message from kernel'
		if myFilter in line and myFilter2 in line and myFileter3 not in line: 
			line_list=line.split("AntiVirusService: ")
			if line_list and line_list[1].startswith('time:'):
				emptyFlag=0
				fres.write(line_list[1]+'\n')          
		line = f.readline()
	fres.close()
	if emptyFlag:
		os.remove(newlogPath)
def reshapeKlog(filename,actionStr,pkgname):
    if 'sys_rmdir' in actionStr:
        mid = 400
    elif 'sys_unlink' in actionStr:
        mid = 300
    elif 'sys_renameat2' in actionStr:
        mid = 200
    elif 'sys_open' in actionStr:
        mid = 100
    if mid == 100:
        if pkgname in filename:
            mid += 0;
        elif "/storage/emulated/0/Download" in filename or "/sdcard/Download" in filename:
            mid += 2;
        elif "/storage/emulated/0/Music" in filename or "/sdcard/Music" in filename:
            mid += 3;
        elif "/storage/emulated/0/Android" in filename or "/sdcard/Android" in filename:
            mid += 4;
        elif "/storage/emulated/0/DCIM" in filename or "/sdcard/DCIM" in filename:
            mid += 5;
        elif "/storage/emulated/0/Movies" in filename or "/sdcard/Movies" in filename:
            mid += 6;
        elif "/storage/emulated/0/Pictures" in filename or "/sdcard/Pictures" in filename:
            mid += 7;
        elif "/storage/emulated/0/Notifications" in filename or "/sdcard/Notifications" in filename:
            mid += 8;
        elif "/storage/emulated/0/Ringtones" in filename or "/sdcard/Ringtones" in filename:
            mid += 9;
        elif "/storage/emulated/0/guard" in filename or "/sdcard/guard" in filename:
            mid += 10;
        else:
            mid += 1;
    else:
        if pkgname in filename:
            mid += 0;
        elif "guard" in filename:
            mid += 2;
        else:
            mid += 1;
    return mid

def trimKlog(uid,pkgname,tmpklogPath,newlogPath):
    klogList = readList(tmpklogPath)
    klogList = list(set(klogList))
    fres=open(newlogPath,'a')
    for klog in klogList:
        if not klog:
            continue
        tmpList = klog.split(',')
        if len(tmpList)<5:
            continue
        timestamp = ''
        actionStr = ''
        filename = ''
        mid = 0
        if 'time:' in tmpList[0] and 'uid:' in tmpList[1] and \
            'action:' in tmpList[2] and 'sys_' in tmpList[3] and \
                'filename:' in tmpList[4]:
            timestamp = tmpList[0].split('time:')[1].strip()
            uid = tmpList[1].split('uid:')[1].strip()
            actionStr = tmpList[3].strip()
            filename = tmpList[4].strip()
            mid = reshapeKlog(filename,actionStr,pkgname)
            ktmp = 'time: %s, uid: %s, method_id: %s %s' %(timestamp,uid,str(mid),filename)
            fres.write(ktmp+'\n')
        else:
            print(tmpklogPath)
            print('str: %s not valid' %klog)
    fres.close()
def getKlog(uid):
    # logcat_file = open(filePath, 'a')
    logcmd='adb shell "dmesg |grep K_AntiVirusService|grep %s"' %(uid)
    # logcmd='adb shell "dmesg |grep %s"' %(uid)
    print logcmd
    handle = subprocess.Popen(logcmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    res = handle.stdout.read()
    handle.terminate()
    return res
def loopGetKlog( uid, testtime, resDict):
    currenttime = 0
    totalres = ''
    while True:
        res = getKlog( uid)
        totalres+=res
        time.sleep(10)
        currenttime+=10
        print currenttime
        if currenttime>=testtime:
            resDict['ret'] = totalres
            return
def getlog(filePath,uid):
    logcat_file = open(filePath, 'w')
    logcmd="adb logcat -e "+uid
    logcmd=logcmd.strip().split()
    handle = subprocess.Popen(logcmd,stdout=logcat_file,stderr=subprocess.PIPE)
    time.sleep(20)
    handle.terminate()

if __name__ == '__main__':
    print 'hello'
    manager = Manager()
    resDict = manager.dict()
    myPool = Pool(2)
    myPool.apply_async(getlog,args=('logcat.txt','10097',))
    myPool.apply_async(loopGetKlog,args=('10097',20,resDict,))
    myPool.close()
    myPool.join()
    writeFile('./klog.txt',resDict['ret'])

    trimLog('10097','logcat.txt','trimed.txt')  
    trimKlog('10097','com.tencent.FileManager','klog.txt','trimed.txt')

