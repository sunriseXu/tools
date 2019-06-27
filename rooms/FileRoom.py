import os
import sys
import subprocess
import random
import logging
import argparse
logging.basicConfig()

pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules import FileUtils

l = logging.getLogger("FileRoom")

def print_all(module_):
    modulelist = dir(module_)
    length = len(modulelist)
    for i in range(0,length,1):
        print getattr(module_,modulelist[i])

def randomCopy(srcDir,destDir,maxNum):
    '''
    randomly select maxNum files in srcDir, and copy them to destDir
    '''
    fileList = FileUtils.listDir(srcDir)
    randomList = random.sample(fileList, maxNum)
    FileUtils.mkdir(destDir)
    FileUtils.listCopy2(randomList,destDir)
    return

def filterFileContent(filePath, splitStr):
    '''
    filter every line in file content, with a splitStr, specific list
    '''
    allLines=[]
    with open(filePath) as f:
        allLines=f.readlines()
    resList=[]
    for line in allLines:
        filtered=''
        line = line.strip()
        if not line:
            continue
        line=line.split(splitStr)[1]
        filtered=line.strip().split()[0]
        resList.append(filtered)
    return resList
def statisticLists(myDict):
    '''
    staticstic frequency in list<list>, {'a':[1,2],'b':[2,3]}=>{1:[1,['a']],2:[2,['a','b']],3:[1,['b']]}
    '''
    resDict={}
    for key,value in myDict.items():
        uniqList = list(set(value))
        for item in uniqList:
            if item not in resDict.keys():
                resDict.update({item:[1,[key]]})
            else:
                resDict[item][0] += 1
                resDict[item][1].append(key)
    return resDict
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument('-s', '--src', help='app name', nargs='?', default="")
    parser.add_argument('-d', '--dest', help='app name', nargs='?', default="")
    parser.add_argument('-i', '--num', help='test time', nargs='?',type=int, default=10)
    args = parser.parse_args()
    srcDir=args.src
    copyNum=args.num
    destDir = args.dest

    # srcDir = 'C:\\Users\\limin\\Desktop\\normal5000_filter\\normal_test_5000'
    # destDir = 'C:\\Users\\limin\\Desktop\\tmp'
    randomCopy(srcDir, destDir, copyNum)
    # testDict = {'a':[1,2],'b':[2,3]}
    # res = statisticLists(testDict)
    # print res