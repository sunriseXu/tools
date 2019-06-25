#/usr/bin/python
import os
import sys
import subprocess
import logging
logging.basicConfig()
l = logging.getLogger("listELFInAPK")
sys.path.append('../tools')
from modules.FileUtils import *
from modules.InteractUtils import *
from modules.ApkUtils import *


def findInDir(dirname,mystr):
    cmd='find %s -type f -name "*.smali"|xargs grep -i "%s"' %(dirname,mystr)
    return subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
def findInFile(filename,mystr):
    buf = readFile(filename)
    if buf:
        if mystr in buf:
            return True
        else:
            return False
    return False
def listItemInStr(myList,myStr):
    for item in myList:
        count=0
        for i in item:
            if i in myStr:
                count+=1
        if count == len(item):
            return True
    return False
import argparse
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument('-d', '--apkpath', help='app name', nargs='?', default="")
    args = parser.parse_args()
    apkPath=args.apkpath

    apkName = os.path.basename(apkPath)
    apkName = os.path.splitext(apkName)[0]
    outName = apkName+'-unzip'
    dirname = os.path.dirname(apkPath)
    outPath = os.path.join(dirname,outName)

    elfDictPath = 'res/elfDict.txt'
    elfDict = readDict(elfDictPath)

    if not os.path.exists(outPath):
        unzipApk(apkPath,outPath)
    whiteList=[
        'libcocos2dcpp',
        'libSecShell',
        'libshell',
        'libexec',
        'libexecmain',
        'libbaiduprotect',
        'libBugly',

    ]
    fileList = listDirRecur(outPath)
    elfFileList = []
    
    for item in fileList:
        basename = getFileName(item)
        if os.path.isfile(item):
            filetype = getFileType(item)
            if ('ELF' in filetype) and (not listItemInStr(whiteList,basename)) :
                elfFileList.append(item)
    elfNameList=[]
    for path in elfFileList:
        elfName = getFileName(path)
        if elfName not in elfNameList:
            elfNameList.append(elfName)

    if apkName not in elfDict.keys():
        elfDict.update({apkName:elfNameList})
        writeDict(elfDict,elfDictPath)

    l.warning("*****elfList*******")
    l.warning('list length:%d',len(elfFileList))
    showList(elfFileList)


    
    





