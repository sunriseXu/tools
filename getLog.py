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
import xml.dom.minidom as xmldom
from modules.xmlTest import *
from modules.FileUtils import *
from modules.CollectionUtils import *
from modules.ThreadUtils import *
from modules.AdbUtils import *


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


def log2file(filePath,uid,packageName,selectedDevId,testTime,interactFlag,kernelFlag):
	logcat_file = open(filePath, 'w')
	logcmd="adb"+selectedDevId+" logcat -e "+uid
	if kernelFlag:
		logcmd='adb %s shell "dmesg |grep %s"' %(selectedDevId,uid)
	logcmd=logcmd.strip().split()
	handle = subprocess.Popen(logcmd,stdout=logcat_file,stderr=subprocess.PIPE)
	if interactFlag:
		l.warning("press some key to stop logcat...")
		time.sleep(testTime)
		# raw_input()
	else:
		i=0
		while i<4:
			getUIXml(selectedDevId)
			i+=1
			l.warning("pass check!")
		if i==4:
			clickWelcome(selectedDevId)
		time.sleep(0.1)
		i=0
		while i<2:
			getUIXml(selectedDevId)
			i+=1
			l.warning("pass check!")
		clickWelcome(selectedDevId)
		# clickWelcome(selectedDevId)
		stopMonkey(selectedDevId)
		p = multiprocessing.Process(target=startMonkey, args=(packageName,selectedDevId,))
		p.start()
		p.join(testTime)
		l.warning("waiting,loging...")
		# time.sleep(testTime)
	handle.terminate()
	stopMonkey(selectedDevId)



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
	parser.add_argument("-x", "--kernel", help="dont uninstall after test one", action="store_true")
	args = parser.parse_args() 

	dirName=args.dirname
	appName=args.appname
	testTime=args.testtime
	maxLength=args.maxlength
	interactFlag=args.interact
	keepAll=args.keepall
	logsDir=args.logsdir
	kernenflag=args.kernel
	pureStop=True
	testInListFlag=args.totest
	apkItems= []
	logDir=logsDir+"/logs/traces/"
	tmplogDir=logsDir+"/logs/tmplog/"
	apkInfoPath=logsDir+"/logs/apkInfoDict.txt"
	errorFilePath=logsDir+"/logs/error.txt"
	toTestFilePath=logsDir+"/toTest.txt"
	testedFilePath=logsDir+"/logs/lastTest.txt"
	notInstallPath=logsDir+"/logs/notInstalled.txt"

	mkdir(tmplogDir)
	mkdir(logDir)

	toTestList=readList(toTestFilePath)
	testedList=readList(testedFilePath)
	notInstallList=readList(notInstallPath)
	apkInfoDict=readDict(apkInfoPath)

	apkItems=listDir(dirName,appName)
	
	itemLen=len(apkItems)
	if testInListFlag:
		itemLen=len(toTestList)
	
	devId,devNum=chooseDevice()

	selectedDevId=" "

	if devNum>0:
		l.warning("%d devices attached!",devNum)
		l.warning("device %s selected!",devId)
		selectedDevId=' -s %s '%devId
	else:
		l.warning("no device attached!")
		sys.exit()
	
	whiteList=['com.zhanhong.message',]
	l.warning("uninstall thirdParty apps")
	uninstallAllThird(selectedDevId,whiteList)


	testedIdx=len(testedList)
	for apkItem in apkItems:
		if testedIdx>maxLength:
			break
		if testedIdx and testedIdx%2==0:
			writeDict(apkInfoDict,apkInfoPath)
			writeList(testedList,testedFilePath)
		try:
			apkHash=os.path.basename(apkItem)
			apkHash= os.path.splitext(apkHash)[0]
			
			if testInListFlag and (apkHash not in toTestList):
				continue
			
			if apkHash in testedList:
				continue
			if apkHash in notInstallList:
				continue
			l.warning(time.strftime('%H:%M:%S',time.localtime(time.time())))
			
			# query manifest for apkInfo
			packageName=getApkInfo(apkItem,"package: name=")
			launchActivity=getApkInfo(apkItem,"launchable-activity: name=")
			apkName=getApkInfo(apkItem,"label=")
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
			stopApp(packageName,selectedDevId,pureStop)
			#clean logcat cache:adb logcat -c -b main  https://blog.csdn.net/u013166958/article/details/79096221
			cleanLog(selectedDevId)
			# start app: https://blog.csdn.net/ahaitongxue/article/details/80369325
			startApp(packageName,selectedDevId)
			#get app's uid
			uid = getUid(packageName, selectedDevId)
			l.warning("No.%d/%d, appName: %s, uid: %s, device: %s",testedIdx,itemLen,apkName,uid,selectedDevId)

			#start to logcat, https://blog.csdn.net/feixueyinjiayue/article/details/49229029
			tmplogPath = tmplogDir+"/"+apkHash+".txt"
			log2file(tmplogPath,uid,packageName,selectedDevId,testTime,interactFlag,kernenflag)

			#uninstall/stop
			if not keepAll:
				uninstallApp(packageName,selectedDevId)
			else:
				stopApp(packageName,selectedDevId,pureStop)

			#filter antivirus log
			newlogPath=logDir+'/'+apkHash+'.txt'
			trimLog(uid,tmplogPath,newlogPath)
			
			testedList.append(apkHash)
			testedIdx+=1
			if testedIdx%5==0:
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
