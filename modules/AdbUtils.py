import os
import sys
import time
import logging
import subprocess
from InteractUtils import *
from ThreadUtils import execute_command
from FileUtils import *
logging.basicConfig()
l = logging.getLogger("AdbUtils")

def getApkInfo(apkPath,param):
	paramValue=""
	if not param:
		return paramValue
	aaptCom="aapt d badging "+apkPath
	res = os.popen(aaptCom)
	line = res.readline()
	while line:
		if param in line:
			startIdx=line.find(param)
			paramValue = line[startIdx:].split("'")[1]
			if paramValue:
				break
		line=res.readline()
	return paramValue
def getApkPermission(apkPath,param):
	paramValue=""
	if not param:
		return paramValue
	aaptCom="aapt d badging "+apkPath
	permissionList = []
	res =execute_command(aaptCom)
	res = res.split('\n')
	for line in res:
		if 'ERROR: dump failed' in line:
			return ['ERROR_DUMP']
		if param in line:
			startIdx=line.find(param)
			paramValue = line[startIdx:].split("'")[1]
			if paramValue:
				permissionList.append(paramValue)
		# line=res.readline()
	return permissionList
def getHashPkgDict(myDir):
    allApkPathList = listDir(myDir)
    hashPkgDict = {}
    idx = 0
    for apkPath in allApkPathList:
        idx+=1
        print(str(idx)+', '),
        apkHash = getFileName(apkPath)
        packageName= getApkInfo(apkPath,"package: name=")
        # print apkHash,packageName
        if packageName:
            hashPkgDict.update({apkHash:packageName})
    return hashPkgDict

def getUid(packageName, selectedDevId):
    getUidCom='adb'+selectedDevId+' shell "dumpsys package %s | grep userId="' %(packageName)
    # uid=os.popen(getUidCom).read()
    uid = execute_command(getUidCom,3)
    uid=uid.strip().split("\n")[0]
    uid=uid.split('=')[1]
    return uid

def startApp(packageName,selectedDevId):
    startAppCmd="adb "+selectedDevId+"shell monkey -p "+packageName+" "+"-c android.intent.category.LAUNCHER 1"
    # res = os.popen(startAppCmd)
    execute_command(startAppCmd,3)
    time.sleep(1)

def stopApp(packageName,selectedDevId,pureStop=True):
	stopAppCmd=""
	#stop app
	if pureStop:
		stopAppCmd="adb"+selectedDevId+" shell pm clear "+packageName
	else:
		stopAppCmd="adb "+selectedDevId+" shell am force-stop "+packageName
	execute_command(stopAppCmd,3)
	time.sleep(1)

def AdbRoot(selectedDevId):
    cmd = 'adb '+selectedDevId+' root'
    # print(os.popen(cmd))
    execute_command(cmd)

def listThirdInstalledApps(selectedDevId):
	mycmd='adb '+selectedDevId+'shell pm list packages -3'
	return os.popen(mycmd).read()

def getThirdApps(selectedDevId):
	thirdPartyList=listThirdInstalledApps(selectedDevId)
	thirdPartyList=thirdPartyList.strip().split()
	thirdPartyList=[item.split(':')[1] for item in thirdPartyList]
	return thirdPartyList

def uninstallApp(packageName,selectedDevId):
    uninsCmd="adb "+selectedDevId+"uninstall "+packageName
    # os.popen(uninsCmd)
    execute_command(uninsCmd,3)
    time.sleep(1)

def uninstallAllThird(selectedDevId, whiteList):
	thirdPartyList=getThirdApps(selectedDevId)
	for item in thirdPartyList:
		if item in whiteList:
			continue
		uninstallApp(item,selectedDevId)

def installApp(apkPath,selectedDevId):
    if not os.path.isfile(apkPath):
        l.warning("apkPath valid!")
        return False
    fileName=os.path.basename(apkPath)
    pDir=os.path.dirname(apkPath)
    newFilePath=""
    if ".apk" not in apkPath:
        newFileName=fileName+".apk"
        newFilePath=os.path.join(pDir,newFileName)
        os.rename(apkPath,newFilePath)
        apkPath=newFilePath
    installCom="adb"+selectedDevId+" install -r "+apkPath
    res=subprocess.Popen(installCom,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
    if "Success" not in res:
        return False
    l.warning("install "+apkPath+" success!")
    return True

def cleanLog(selectedDevId):
    logcmd="adb"+selectedDevId+" logcat -c"
    # os.popen(logcmd)
    execute_command(logcmd,1)
def chooseDevice():
	adbCmd="adb devices"
	res =os.popen(adbCmd).read()
	res = res.strip().split('\n')
	res = [i.strip().split()[0:2] for i in res]
	res = [i[0] for i in res if "device" in i]
	res1=[]
	for item in res:
		if item not in res1:
			res1.append(item)
	res=res1
	if len(res)>1:
		showList(res)
		devi=selectListItemByIdx(res)
		# devi = res[0]
		l.warning("%s selected",devi)
		return (devi,len(res))
	elif len(res)==1:
		devi = res[0]
		l.warning("%s selected", devi)
		return (devi, len(res))
	else:
		return (None,0)

def unlockPhone(selectedDevId):
	checkLockedCmd='adb'+selectedDevId+' shell "dumpsys window policy|grep isStatusBarKeyguard"'
	print(checkLockedCmd)
	res = os.popen(checkLockedCmd).read()
	if "false" in res:
		swipeCmd="adb"+selectedDevId+" shell input swipe 500 1000 500 0"
		# os.popen(swipeCmd)
		# time.sleep(0.5)
		return 
	unlockCmd="adb"+selectedDevId+" shell input keyevent 26 &ping -n 2 127.0.0.1>nul &adb"+selectedDevId+" shell input swipe 500 1000 500 0"
	os.popen(unlockCmd)
	print('unlocking phone!!!!!')
	time.sleep(0.5)

def startMonkey(packageName,selectedDevId):
	useMonkeyCmd="adb"+selectedDevId+" shell monkey -v -v -v -s 123123 --throttle 500 --pct-touch 70 --pct-motion 10 --pct-appswitch 10  --pct-majornav 10  --pct-trackball 0 --ignore-crashes --ignore-timeouts --ignore-native-crashes -p %s 10000>nul" %(packageName)
	os.popen(useMonkeyCmd).read()

def stopMonkey(selectedDevId):
	getUidCmd='adb'+selectedDevId+' shell "ps|grep monkey"'
	monkeyUid=os.popen(getUidCmd).read()
	if monkeyUid:
		monkeyUid=monkeyUid.strip().split()[1]
		killUidCmd='adb'+selectedDevId+' shell "kill %s"' %(monkeyUid)
		os.popen(killUidCmd)

def pullFile(selectedDevId,srcPath, destPath,timeout=10):
	cmd = 'adb -s %s pull %s %s' %(selectedDevId,srcPath,destPath)
	# some issue here, if timeout not set, the process will hang! to do
	res = execute_command(cmd,timeout)
	# l.warning(res)
def rebootRecovery(selectedDevId):
	'''
	enter recovery mode, to wipe data!
	'''
	cmd = 'adb {} reboot recovery'.format(selectedDevId)
	execute_command(cmd)
# def pullRootFile(selectedDevId, srcPath, destPath, timeout=10):
def getDevices():
	adbCmd="adb devices"
	res =os.popen(adbCmd).read()
	res = res.strip().split('\n')
	res = [i.strip().split()[0:2] for i in res]
	res = [i[0] for i in res if "device" in i]
	res1=[]
	for item in res:
		if item not in res1:
			res1.append(item)
	return res1
def getPhoneModel(selectedDevId):
	cmd = 'adb {} shell getprop ro.product.model'.format(selectedDevId)
	res = os.popen(cmd).read()
	return res
def muteMusic(selectedDevId):
	cmd = 'adb {} shell media volume --set 0'.format(selectedDevId)
	res = os.popen(cmd).read()
	return res
def disableIME(selectedDevId):
	cmd = 'adb {} shell ime disable com.android.inputmethod.latin/.LatinIME'.format(selectedDevId)
	res = os.popen(cmd).read()
	return res

if __name__ == "__main__":
	devId,devNum=chooseDevice()
	# print devId
	srcPath = '/sdcard/newdex'
	destPath = 'C:\\Users\\limin\\Desktop\\tmp2'
	# pullFile(devId,srcPath,destPath,5)
	res = getApkInfo('/home/limin/Desktop/malware/cou-qqpiliang.apk','uses-permission: name=')
	print(res)