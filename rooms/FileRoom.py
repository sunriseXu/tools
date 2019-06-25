import os
import sys
import subprocess
import random
import logging
logging.basicConfig()
# sys.path.append('../tools')
from modules.FileUtils import *
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


if __name__ == "__main__":
    srcDir = 'C:\\Users\\limin\\Desktop\\normal5000_filter\\normal_test_5000'
    destDir = 'C:\\Users\\limin\\Desktop\\tmp'
    randomCopy(srcDir, destDir, 2)