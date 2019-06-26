#/usr/bin/python
import os
import sys
import subprocess
import argparse
from modules.FileUtils import *
from modules.InteractUtils import *
from modules.ThreadUtils import execute_command


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument('-d', '--dirname', help='app name', nargs='?', default="")
    parser.add_argument('-c', '--dict', help='app name', nargs='?', default="")
    args = parser.parse_args()
    dirPath=args.dirname
    elfDict=args.dict
    
    testedPath = './tmp.txt'
    testedList = readList(testedPath)
    fileList = listDir(dirPath)
    for item in fileList:
        if item in testedList:
            continue
        
        fileName = os.path.basename(item)
        # print fileName
        # tmp = os.path.splitext(fileName)
        # if len(tmp) == 1:
        #     continue
        # ext = tmp[1]
        
        # if 'apk' not in ext:
        #     continue
        tmp = getFileType(item)
        if 'zip archive data' not in tmp.lower():
            continue    
        print item
        cmd = 'python examples/listELFInAPK.py -d %s -c %s' %(item,elfDict)
        # sub = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        # res = sub.stdout.read()
        res = execute_command(cmd, 60)
        print res
        # print 'tap to continue...'
        testedList.append(item)
        writeList(testedList,testedPath)
        print '\n'
        # raw_input()

    # allelfPath='./allelf.txt'
    # allelfList = readList(allelfPath)
    # pathListCopy(allelfList,'~/Desktop/allelf')
    # print('done')