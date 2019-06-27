#!/usr/bin/python
import os
import sys
import subprocess
import argparse

pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules.FileUtils import *
from modules.InteractUtils import *
from modules.ThreadUtils import execute_command


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument('-d', '--dirname', help='app name', nargs='?', default="")
    parser.add_argument('-e', '--elfdict', help='app name', nargs='?', default="")
    parser.add_argument('-m', '--smalidict', nargs='?', default="")
    parser.add_argument('-s', '--mystring', help='app name', nargs='?', default="")
    args = parser.parse_args()
    dirPath=args.dirname
    elfDict=args.elfdict
    smaliDict=args.smalidict
    mystr = args.mystring
    
    testedPath = './tmp.txt'
    testedList = readList(testedPath)
    fileList = listDir(dirPath)
    for item in fileList:
        if item in testedList:
            continue
        
        fileName = os.path.basename(item)
        tmp = getFileType(item)
        if 'zip archive data' not in tmp.lower():
            continue    
        print item
        
        cmd = 'python %s/listELFInAPK.py -d %s -c %s' %(pwd,item,elfDict)
        print cmd
        res = execute_command(cmd, 60)
        print res

        cmd = 'python %s/decompileAndFind.py -d %s -s %s -c %s' %(pwd,item,mystr,smaliDict)
        print cmd
        res = execute_command(cmd, 60)
        print res

        testedList.append(item)
        writeList(testedList,testedPath)
        print '\n'
        # raw_input()

