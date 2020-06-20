# -*- coding:utf-8 -*-
import urllib
# import urllib2
import re
import os
import json
import shutil
import sys
import subprocess
import logging
from modules.RexUtils import rexFind
from distutils.dir_util import copy_tree
logging.basicConfig()
l = logging.getLogger("FileUtils")

class EasyDir:
	def __init__(self, myDir):
		self.currentDir = myDir
		self.fileNameList = listDir2(myDir)
		self.absPathDict = {}
		for fileName in self.fileNameList:
			absPath = os.path.join(myDir, fileName)
			self.absPathDict.update({fileName:absPath})
	def getFileAbsPath(self, fileName):
		if fileName not in self.absPathDict:
			return ''
		return self.absPathDict[fileName]
	def updateDir(self):
		self.fileNameList = listDir2(self.currentDir)
		self.absPathDict = {}
		for fileName in self.fileNameList:
			absPath = os.path.join(self.currentDir, fileName)
			self.absPathDict.update({fileName: absPath})
	def getAbsPathDict(self):
		return self.absPathDict
	def rexFindPath(self, myRex):
		resDict = {}
		for key,value in self.absPathDict.items():
			if len(rexFind(myRex, key))>0:
				resDict.update({key:value})
		return resDict
	def getCatPath(self, fileName):
		absPath = os.path.join(self.currentDir,fileName)
		dirPath = os.path.dirname(absPath)
		if not os.path.exists(dirPath):
			os.makedirs(dirPath)
		return absPath

def copytree2(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        print(item)
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            copy_tree(s, d)
        else:
            shutil.copy2(s, d)
def MergeAllDir2One(root, dest):
    childDir = EasyDir(root)
    childPathList = childDir.getAbsPathDict().values()        
    for childDir in childPathList:
        print("start to copy {} to {}".format(childDir, dest))
        copytree2(childDir, dest)
def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)
	return path
def cleanAndMkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)
	else:
		shutil.rmtree(path)
		os.makedirs(path)
	return path

def createPDkir(fPath):
	dirName = os.path.dirname(fPath)
	mkdir(dirName)

def listDir(dirPath,filePath=''):
	fileList=[]
	if not filePath.strip():
		for filename in os.listdir(dirPath):
			pathname = os.path.join(dirPath, filename)
			fileList.append(pathname)
		if len(fileList)==0:
			return fileList
		else:
			l.debug("list "+str(len(fileList))+" files in: "+dirPath+"!")
	else:
		fileList.append(filePath)
		l.debug("list 1 file: "+filePath+"!")
	return fileList

def listDir2(dirPath):
	fileList = []
	if not os.path.exists(dirPath):
		return fileList
	for filename in os.listdir(dirPath):
		fileList.append(filename)
	l.debug("list %d files in: %s!",len(fileList),dirPath)
	return fileList

def listDir3(dirPath):
	fileList = []
	if not os.path.exists(dirPath):
		return fileList
	for filename in os.listdir(dirPath):
		basename = os.path.basename(filename)
		rawname = os.path.splitext(basename)[0]
		fileList.append(rawname)
	l.debug("list %d files in: %s!",len(fileList),dirPath)
	return fileList

def listDirRecur(path):
	'''
	recursively list all files/dirs in path, return a list
	'''
	allfile=[]
	for dirpath,dirnames,filenames in os.walk(path):
		for dir in dirnames:
			allfile.append(os.path.join(dirpath,dir))
		for name in filenames:
			allfile.append(os.path.join(dirpath, name))
	return allfile

def getFileName(myPath):
	bn = os.path.basename(myPath)
	fn = os.path.splitext(bn)[0]
	return fn


def readList(myPath):
	reslist=[]
	if not os.path.exists(myPath):
		temp=open(myPath,'w')
		l.warning("%s not exist! created instead",myPath)
		temp.close()
	with open(myPath,"r") as file:
		reslist=file.readlines()
	reslist = [i.strip().strip('\r') for i in reslist]
	return reslist


def writeList(myList,myPath):
	with open(myPath,"w") as file:
		for item in myList:
			item=str(item).strip()+"\n"
			file.write(item)

def readDict(dictFile):
	'''
	read json file, return the dict
	'''
	flag = True
	if not os.path.exists(dictFile):
		flag=False
		temp=open(dictFile,'w')
		temp.close()
	file1=open(dictFile,'r')
	jsonFile=file1.read()
	if flag and jsonFile:
		myDict=json.loads(jsonFile)
	else:
		myDict={}
	file1.close()
	return myDict

def writeDict(myDict,myDictPath):
	'''
	write dict to json file
	'''
	js = json.dumps(myDict)   
	file2 = open(myDictPath, 'w')
	file2.write(js)  
	file2.close()

def readFile(filePath):
	if not os.path.exists(filePath):
		temp=open(filePath,'w')
		temp.close()
	myStr=''
	with open(filePath,'r') as f:
		myStr=f.read()
	return myStr

def readFileLines(filePath, lineNum):
	lines = ""
	with open(filePath,"r") as f:
		for i in range(lineNum):
			lines += f.readline()
	return lines



def writeFile(filePath,myStr):
	createPDkir(filePath)
	with open(filePath,'w') as f:
		f.write(myStr)
	return

def getFileType(filePath):
    cmd = 'file %s' %filePath
    return subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()

def listCopy(myList,srcDir,destDir):
	'''
	item in myList must have the same file name in srcDir
	copy list item in srcDir to destDir,when destDir not exist, create it
	'''
	mkdir(destDir)
	for item in myList:
		if not item:
			continue
		
		srcPath=os.path.join(srcDir,item)
		if not os.path.exists(srcPath):
			# print srcPath,'not exist'
			l.warning("listCopy: %s not exists",srcPath)
			continue
		destPath=os.path.join(destDir,item)
		shutil.copy(srcPath,destPath)
	return

def listCopy2(myList,destDir):
	'''
	myList must contain abs path list 
	'''
	if len(myList) == 0:
		return
	mkdir(destDir)
	for myPath in myList:
		if not os.path.exists(myPath):
			continue
		basename = os.path.basename(myPath)
		destPath = os.path.join(destDir, basename)
		shutil.copy(myPath,destPath)


def listCopy3(listPath, srcDir, destDir):
	myList = readList(listPath)
	listCopy(myList, srcDir, destDir)

def listCut(myList,srcDir,destDir=''):
	'''
	cut file in myList to destDir from srcDir, default destDir is $srcDir_cut 
	'''
	if not destDir:
		absSrcPath=os.path.abspath(srcDir)
		#get parent dir path
		parentPath=os.path.dirname(absSrcPath)
		destName=os.path.basename(absSrcPath)+'_cut'
		destDir=os.path.join(parentPath,destName)
		mkdir(destDir)
	else:
		if not os.path.exists(destDir):
			l.warning('destDir is not exist, failed!')
			return 
	for item in myList:
		srcPath=os.path.join(srcDir,item)
		if not os.path.exists(srcPath):
			continue
		destPath=os.path.join(destDir,item)
		shutil.move(srcPath,destPath)
	return 

def listCut2(listPath, srcDir, destDir):
	myList = readList(listPath)
	listCut(myList, srcDir, destDir)

def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)


def xorFileWithByte(src,dest,myByte):
	'''
	xor all content byte by byte in src file with myByte, write new file to dest
	'''
	f = open(src,"rb")
	myStr = f.read()
	myBy = bytes(myStr)
	newBy=''
	for i in myBy:
		newBy=newBy+chr(ord(i)^myByte)
	with open(dest,'wb') as f:
		f.write(newBy)



if __name__ == "__main__":
	# listCut(['test.txt'],'C:\\Users\\limin\\Desktop\\test\\test1_cut')
	mydict={'1':'hello','2':'xiao','3':'niao'}
	myklist=['1','5','3']
	mylist=['niao','xxx','hello']
	# print listDirRecur('./')
	reslist=listDir2('./')
	# print reslist
	# print value2keylist(mylist,mydict)
	# print key2Valuelist(myklist,mydict)
