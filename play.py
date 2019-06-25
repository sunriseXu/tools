#/usr/bin/python
import os
import sys
import subprocess
import argparse
from modules.FileUtils import *
from modules.InteractUtils import *




if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument('-d', '--dirname', help='app name', nargs='?', default="")
    args = parser.parse_args()
    dirPath=args.dirname
    
    testedPath = './tmp'
    testedList = readList(testedPath)
    fileList = listDir(dirPath)
    for item in fileList:
        if item in testedList:
            continue
        
        fileName = os.path.basename(item)
        # print fileName
        tmp = os.path.splitext(fileName)
        if len(tmp) == 1:
            continue
        ext = tmp[1]
        
        if 'apk' not in ext:
            continue
        print item
        cmd = 'python examples/listELFInAPK.py -d %s' %item
        sub = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        res = sub.stdout.read()
        print res
        print 'tap to continue...'
        testedList.append(item)
        writeList(testedList,testedPath)
        print '\n'
        # raw_input()

    allelfPath='./allelf.txt'
    allelfList = readList(allelfPath)
    pathListCopy(allelfList,'~/Desktop/allelf')
    print('done')