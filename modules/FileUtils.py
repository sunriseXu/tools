# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os
import json
import shutil
import sys
import subprocess
import logging
logging.basicConfig()
l = logging.getLogger("FileUtils")

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

def listDir(dirPath,filePath=''):
	fileList=[]
	if not filePath.strip():
		for filename in os.listdir(dirPath):
			pathname = os.path.join(dirPath, filename)
			fileList.append(pathname)
		if len(fileList)==0:
			sys.exit()
		else:
			print("list "+str(len(fileList))+" files in: "+dirPath+"!")
	else:
		fileList.append(filePath)
		print("list 1 file: "+filePath+"!")
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
		temp.close()
	with open(myPath,"r") as file:
		mystr=file.read()
		reslist=mystr.strip().split("\n")
	return reslist


def writeList(myList,myPath):
	with open(myPath,"w") as file:
		for item in myList:
			item=item.strip()+"\n"
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

def writeFile(filePath,myStr):
	with open(filePath,'a') as f:
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
			l.warning("%s not exists",srcPath)
			continue
		destPath=os.path.join(destDir,item)
		shutil.copy(srcPath,destPath)
	return

def pathListCopy(myList,destDir):
	'''
	myList contain all file pathes that need to copy to destDir
	'''
	if len(myList)==0:
		return
	mkdir(destDir)
	for path in myList:
		if not os.path.exists(path):
			continue
		basename = os.path.basename(path)
		destPath = os.path.join(destDir, basename)
		shutil.copy(path,destPath)

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
	print listDirRecur('./')
	# print value2keylist(mylist,mydict)
	# print key2Valuelist(myklist,mydict)
