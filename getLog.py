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
from multiprocessing import Process, Manager, Pool

logging.basicConfig()
l = logging.getLogger("getLog")


def UIRandomClick(packageName,launchActivity):
	print Package.getCurrentActivity()
	l.warning("start ui random click...")
	pk=Package(packageName)
	pk.dump()
	print("tap to continue...")
	for i in range(20):
		l.warning("**************random click %d ********************",i)
		pk.forward()
		res=pk.dump()
		if not res:
			return
def UIPassCheck(selectedDevId):
	i=0
	while i<5:
		res = getUIXml(selectedDevId)
		if 2==res:
			return
		i+=1
		l.warning("pass check!")
	if i==5:
		clickWelcome(selectedDevId)
	time.sleep(0.1)
	i=0
	while i<4:
		res = getUIXml(selectedDevId)
		if 2== res:
			return
		i+=1
		l.warning("pass check!")
	clickWelcome(selectedDevId)
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
			uidtmp = tmpList[1].split('uid:')[1].strip()
			if uid not in uidtmp:
				continue
			actionStr = tmpList[3].strip()
			filename = tmpList[4].strip()
			mid = reshapeKlog(filename,actionStr,pkgname)
			ktmp = 'time: %s, uid: %s, method_id: %s %s' %(timestamp,uidtmp,str(mid),filename)
			fres.write(ktmp+'\n')
		else:
			print(tmpklogPath)
			print('str: %s not valid' %klog)
	fres.close()

def getKlog(uid,selectedDevId):
	logcmd='adb %s shell "dmesg |grep K_AntiVirusService|grep %s"' %(selectedDevId,uid)
	handle = subprocess.Popen(logcmd,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
	res = handle.stdout.read()
	handle.terminate()
	return res
def loopGetKlog(uid, selectedDevId,testtime, resDict):
    currenttime = 0
    totalres = ''
    while True:
        res = getKlog(uid,selectedDevId)
        totalres+=res
        time.sleep(10)
        currenttime+=10
        print currenttime
        if currenttime>=testtime:
            resDict['ret'] = totalres
            return

def log2file(filePath,uid,packageName,selectedDevId,testTime,interactFlag):
	logcat_file = open(filePath, 'w')
	logcmd="adb"+selectedDevId+" logcat -e "+uid
	logcmd=logcmd.strip().split()
	handle = subprocess.Popen(logcmd,stdout=logcat_file,stderr=subprocess.PIPE)
	if interactFlag:
		l.warning("press some key to stop logcat...")
		time.sleep(testTime)
		# raw_input()
	else:
		l.warning("start UIPassCheck!")
		UIPassCheck(selectedDevId)
		l.warning("stop UIPassCheck!")
		l.warning("start MonkeyTest...")
		stopMonkey(selectedDevId)
		startTime = time.clock()
		# p = multiprocessing.Process(target=startMonkey, args=(packageName,selectedDevId,))
		t = MyThread(startMonkey, args=(packageName,selectedDevId,))
		t.start()
		t.join(testTime)
		endTime = time.clock()
		l.warning('MonkeyTesting time: %d', endTime-startTime)
	logcat_file.flush()
	l.warning("stop MonkeyTest...")
	handle.terminate()
	stopMonkey(selectedDevId)


def touchFile(selectedDevId):
	cmd = 'adb %s push guard /sdcard/' %selectedDevId
	return os.popen(cmd).read()

def checkDeviceOn(selectedDevId):
	idx = 0
	devId = selectedDevId.split('-s')[1].strip()
	rebootCmd = 'fastboot {} reboot'.format(selectedDevId)
	while(True):
		idx += 1
		res = touchFile(selectedDevId)
		print("check device on : push file res- {}".format(res))
		# device shutdown

		if devId in res and 'not found' in res:
			print("device shut down, try to reboot, timeId: {}".format(idx))
			os.popen(rebootCmd).read()
			time.sleep(30)
		elif 'file pushed' in res:
			print("device is running!")
			break
		if idx > 5:
			print("try to reboot device 5 times, but not work! check manually")
			break


def checkAppAlive(selectedDevId, pkgName):
	# alive?
	aliveCmd = 'adb %s shell "ps|grep %s"' %(selectedDevId, pkgName)
	res = os.popen(aliveCmd).read()
	if pkgName not in res:
		l.warning('pkg: %s is not running!', pkgName)
		l.warning("start pkgName: %s",pkgName)
		startApp(pkgName,selectedDevId)
	return 
	
	
def trimLog(uid,tmplogPath,tmpKlogPath,newlogPath):
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

if __name__ == "__main__":
	desktopDir=os.path.join(os.path.expanduser("~"), 'Desktop')
	parser = argparse.ArgumentParser(description="test!!")
	parser.add_argument('-n', '--appname', help='app name', nargs='?', default="")
	parser.add_argument('-d', '--dirname', help='dir name', nargs='?', default=desktopDir+"/"+"/malware/")
	parser.add_argument('-t', '--testtime', help='test time', nargs='?',type=float, default=60)
	parser.add_argument('-m', '--maxlength', help='max number of test samples', nargs='?',type=int, default=60000)
	parser.add_argument("-a", "--interact", help="interactive testing,this is an optional argument", action="store_true")
	parser.add_argument("-k", "--keepall", help="dont uninstall after test one", action="store_true")
	parser.add_argument("-l", "--logsdir", help="destination of logs",nargs='?', default=desktopDir)
	parser.add_argument("-e", "--totest", help="dont uninstall after test one", action="store_true")
	parser.add_argument("-s", "--totestPath", help="toTestPath", nargs='?', default='')
	parser.add_argument("-x", "--kernel", help="dont uninstall after test one", action="store_true")
	args = parser.parse_args() 

	dirName=args.dirname
	appName=args.appname
	testTime=args.testtime
	maxLength=args.maxlength
	interactFlag=args.interact
	keepAll=args.keepall
	logsDir=args.logsdir
	kernelflag=args.kernel
	pureStop=True
	testInListFlag=args.totest
	toTestPath = args.totestPath
	apkItems= []
	logDir=logsDir+"/logs/traces/"
	tmplogDir=logsDir+"/logs/tmplog/"
	klogDir = logsDir+'/logs/tmpKlog/'
	apkInfoPath=logsDir+"/logs/apkInfoDict.txt"
	errorFilePath=logsDir+"/logs/error.txt"
	testedFilePath=logsDir+"/logs/lastTest.txt"
	notInstallPath=logsDir+"/logs/notInstalled.txt"
	if not toTestPath:
		toTestFilePath = logsDir + "/toTest.txt"
	else:
		toTestFilePath = toTestPath

	mkdir(tmplogDir)
	mkdir(logDir)
	mkdir(klogDir)

	toTestList=readList(toTestFilePath)
	testedList=readList(testedFilePath)
	notInstallList=readList(notInstallPath)
	apkInfoDict=readDict(apkInfoPath)

	devId,devNum=chooseDevice()
	selectedDevId=" "
	if devNum>0:
		l.warning("%d devices attached!",devNum)
		l.warning("device %s selected!",devId)
		selectedDevId=' -s %s '%devId
	else:
		l.warning("no device attached!")
		sys.exit()
	
	apkItems=listDir(dirName,appName)
	itemLen=len(apkItems)
	if testInListFlag:
		itemLen=len(toTestList)
	unlockPhone(selectedDevId)
	whiteList=[
		'com.zhanhong.message',
		'com.antivirus.dbconnector',
		'com.fdu.testcryptfile',
		'com.tencent.mm',
		'com.tencent.mobileqq',
		'com.eg.android.AlipayGphone',
		'com.example.limin.sendsmsoneline',
		'com.sina.weibo',
		]
	l.warning("uninstall thirdParty apps")
	uninstallAllThird(selectedDevId,whiteList)

	date = time.strftime('%H-%M-%S',time.localtime(time.time()))
	# antivirusOutPath = '%s/antivirusOut-%s.txt' %(logsDir,date)
	fileName = 'antivirusOut-%s.txt' %(date)
	antivirusOutPath = os.path.join(logsDir,fileName)
	antiResHandle = open(antivirusOutPath, 'w')
	filteredStr = 'Modelresult'
	logcmd = 'adb %s shell logcat -s %s' %(selectedDevId,filteredStr)
	logcmd=logcmd.strip().split()
	p = subprocess.Popen(logcmd, stdout=antiResHandle,stderr=subprocess.PIPE)
	
	
	testedIdx=len(testedList)
	testingFlag = False
	for apkItem in apkItems:
		if testedIdx>maxLength:
			break
		if testedIdx and testedIdx%2==0 and testingFlag: 
			testingFlag = False
			writeDict(apkInfoDict,apkInfoPath)
			writeList(testedList,testedFilePath)
		# if testedIdx%30==0:
		# 	writeList(testedList, '/home/limin/Documents/jianguoyun/Nutstore/tested.txt')
		try:
			apkHash=os.path.basename(apkItem)
			apkHash= os.path.splitext(apkHash)[0]
			
			if testInListFlag and (apkHash not in toTestList):
				continue
			
			if apkHash in testedList:
				continue
			if apkHash in notInstallList:
				continue

			# todo check device is attached, otherwise, fastboot -s dev reboot
			checkDeviceOn(selectedDevId)

			l.warning(time.strftime('%H:%M:%S',time.localtime(time.time())))
			touchFile(selectedDevId)
			testingFlag = True
			AdbRoot(selectedDevId)
			unlockPhone(selectedDevId)
			checkAppAlive(selectedDevId,'com.fdu.testcryptfile')
			

			# query manifest for apkInfo
			packageName=getApkInfo(apkItem,"package: name=")
			launchActivity=getApkInfo(apkItem,"launchable-activity: name=")
			apkName=getApkInfo(apkItem,"label=")
			if packageName in 'com.ioty_app':
				continue
			appendDict(apkInfoDict,apkHash,[packageName,apkName])
			l.warning("start to install apk, Hash:%s pkgName:%s apkName:%s !",apkHash, packageName, apkName)
			
			# start to install apkFile, set delayTime
			delayTime = 50
			t=MyThread(installApp,args=(apkItem,selectedDevId))
			t.start()
			t.join(delayTime)
			resFlag= t.get_result()
			if (not resFlag) or (resFlag==None):
				notInstallList.append(apkHash)
				writeList(notInstallList,notInstallPath)
				l.warning("install %s failed!",apkName)
				continue
			
			#if app is running, stop it
			# stopApp(packageName,selectedDevId,pureStop)
			#clean logcat cache:adb logcat -c -b main  https://blog.csdn.net/u013166958/article/details/79096221
			cleanLog(selectedDevId)
			# start app: https://blog.csdn.net/ahaitongxue/article/details/80369325
			startApp(packageName,selectedDevId)
			#get app's uid
			uid = getUid(packageName, selectedDevId)
			l.warning("No.%d/%d, appName: %s, uid: %s, device: %s",testedIdx,itemLen,apkName,uid,selectedDevId)

			#start to logcat, https://blog.csdn.net/feixueyinjiayue/article/details/49229029
			tmplogPath = tmplogDir+"/"+apkHash+".txt"
			tmpklogPath = klogDir+"/"+apkHash+".txt"
			
			manager = Manager()
			resDict = manager.dict()
			myPool = Pool(2)
			myPool.apply_async(log2file,args=(tmplogPath,uid,packageName,selectedDevId,testTime,interactFlag,))
			# myPool.apply_async(loopGetKlog,args=(uid,selectedDevId,testTime+10,resDict,))
			myPool.close()
			myPool.join()
			# writeFile(tmpklogPath,resDict['ret'])
			
			#uninstall/stop
			if not keepAll:
				uninstallApp(packageName,selectedDevId)
			else:
				stopApp(packageName,selectedDevId,pureStop)

			#filter antivirus log
			newlogPath=logDir+'/'+apkHash+'.txt'
			trimLog(uid,tmplogPath,tmpklogPath,newlogPath)
			# trimKlog(uid,packageName,tmpklogPath, newlogPath)
			testedList.append(apkHash)
			antiResHandle.flush()
			testedIdx+=1
			if testedIdx%10==0:
				uninstallAllThird(selectedDevId,whiteList)
		except IOError:
			errorStr="IOError dealing with: %s\n" %(apkHash)
			l.warning(errorStr)
			writeFile(errorFilePath,errorStr)	
		except RuntimeError:
			errorStr="RuntimeError dealing with: %s\n" %(apkHash)
			l.warning(errorStr)
			writeFile(errorFilePath,errorStr)
		except IndexError,e:
			errorStr="IndexError dealing with: %s\n" %(apkHash)
			l.warning(errorStr)
			l.warning(traceback.print_exc())
			writeFile(errorFilePath,errorStr)
	writeDict(apkInfoDict,apkInfoPath)
	writeList(testedList,testedFilePath)
	l.warning("all done!")
