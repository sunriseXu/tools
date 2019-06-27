#/usr/bin/python
import os
import sys
import subprocess
import logging
logging.basicConfig()

pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules.FileUtils import *
from modules.InteractUtils import *
from modules.ApkUtils import *
l = logging.getLogger("decompileAndFind")

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
    parser.add_argument('-c', '--cdict', nargs='?', default="")
    parser.add_argument('-s', '--string', help='string to find', nargs='?', default="")
    args = parser.parse_args()
    apkPath=args.apkpath
    dictPath= args.cdict
    myString = args.string

    apkName = os.path.basename(apkPath)
    apkName = os.path.splitext(apkName)[0]
    dirname = os.path.dirname(apkPath)
    
    outName = apkName+'-output'
    outPath = os.path.join(dirname,outName)

    mydict = readDict(dictPath)

    whiteList=[
        ('android','support'),
        ('tencent','bugly'),

    ]
    
    if not os.path.exists(outPath):
        decompileApk(apkPath,outPath)
    fileList = listDirRecur(outPath)
    resList = []
    for item in fileList:
        if '.smali' in item:
            if listItemInStr(whiteList,item):
                continue
            res = findInFile(item,myString)
            if res:           
                resList.append(os.path.basename(item))
    
    if apkName not in mydict.keys():
        mydict.update({apkName:resList})
        writeDict(mydict,dictPath)

    l.warning("*****%slist*******",myString)
    l.warning('list length:%d',len(resList))
    showList(resList)