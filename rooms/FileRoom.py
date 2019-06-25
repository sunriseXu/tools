import os
import sys
import subprocess
import random
import logging
logging.basicConfig()
# sys.path.append('../tools')
from tools.modules.FileUtils import *
from tools.modules.AlgorithmUtils import *
l = logging.getLogger("FileRoom")

def randomCopy(srcDir,destDir,maxNum):
    '''
    randomly select maxNum files in srcDir, and copy them to destDir
    '''
    fileList = listDir(srcDir)
    randomList = random.sample(fileList, maxNum)
    mkdir(destDir)
    pathListCopy(randomList,destDir)
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


if __name__ == "__main__":
    srcDir = 'C:\\Users\\limin\\Desktop\\normal5000_filter\\normal_test_5000'
    destDir = 'C:\\Users\\limin\\Desktop\\tmp'
    randomCopy(srcDir, destDir, 2)