# -*- coding:utf-8 -*-
import io
import json
import argparse 
import os
import sys
import subprocess
import time
import multiprocessing
import threading
import datetime
import shutil
import traceback

def readList(myPath):
    resList = []
    with open(myPath) as f:
        resList = f.readlines()
    resList = [i.strip('\n').strip('\r') for i in resList]
    return resList


def execute_command(cmdstring, timeout=None,env=None, debug=False):
    if timeout:
        end_time = datetime.datetime.now() + datetime.timedelta(seconds=timeout)
    try:
        sub = None
        if not env:
            sub = subprocess.Popen(cmdstring,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
        else:
            sub = subprocess.Popen(cmdstring, shell=True,env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    except OSError:
        return 'OSError'
    while True:
        if sub.poll() is not None:
            break
        time.sleep(0.1)
        # print 'poll is none'
        if debug:
            buff = sub.stdout.readline()
            print(buff)
        if timeout:
            if end_time <= datetime.datetime.now():
                try:
                    sub.kill()
                except Exception:
                    return "TIME_OUT"
                return "TIME_OUT"
    res=sub.stdout.read()
    if sub.stdin:
        sub.stdin.close()
    if sub.stdout:
        sub.stdout.close()
    if sub.stderr:
        sub.stderr.close()
    try:
        sub.kill()
    except OSError:
        return res
    return res
def mkdir(path):
    folder = os.path.exists(path)
    if not folder:
        os.makedirs(path)
    return path
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
def listDir(dirPath,filePath=''):
	fileList=[]
	if not filePath.strip():
		for filename in os.listdir(dirPath):
			pathname = os.path.join(dirPath, filename)
			fileList.append(pathname)
		if len(fileList)==0:
			return fileList
	else:
		fileList.append(filePath)
		# l.debug("list 1 file: "+filePath+"!")
	return fileList
def decompileApk(srcPath, destPath):
    cmd = 'apktool -r d {} -o {}'.format(srcPath,destPath)
    subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
def recompileApk(srcPath, destPath):
    cmd = 'apktool b {} -o {}'.format(srcPath,destPath)
    subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
def signApk(keyPath,passwd,apkPath,alias):
    cmd = 'jarsigner -keystore {} {} {} -storepass {}'.format(keyPath, apkPath, alias, passwd)
    print(cmd)
    subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
def deleteDir(srcPath):
    cmd = 'rm -rf {}'.format(srcPath)
    print(cmd)
    subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()
def execJar(jarPath,argv,redirectPath=""):
    if redirectPath:
        redirectPath = '> '+redirectPath
    cmd = 'java -jar {} {} {}'.format(jarPath,argv,redirectPath)
    print(cmd)
    cmd = cmd.split()
    try:
        out = subprocess.check_output(cmd,shell=True,stderr=subprocess.STDOUT).strip()
        out = out.decode()
        print(out)
    except Exception as e:
        print(traceback.format_exc())
        raise
def singleExtract(apkPath):
    outPath = './tmp'
    apkName = os.path.basename(apkPath)
    apkName = apkName.split('.')[0]
    # 反编译
    decompileApk(apkPath, outPath)
    # 用jar包找smali中的const-string
    jarPath = './stringObfuscate.jar'
    smaliPath = outPath+'/'+'smali'
    if not os.path.exists('out'):
        os.mkdir('out')
    redirectPath = 'out/{}.txt'.format(apkName)
    execJar(jarPath, smaliPath,redirectPath)
    # 删除
    deleteDir(outPath)
if __name__ == "__main__":
    apkPath = sys.argv[1]
    if not os.path.isdir(apkPath):
        singleExtract(apkPath)
    else:
        print("dir:{}".format(apkPath))
        apkPathList = listDir(apkPath)
        for apkPath in apkPathList:
            fileSize = size = os.path.getsize(apkPath)
            if fileSize>800000:
                continue
            # input()
            print("start to extract {}".format(apkPath))
            singleExtract(apkPath)
            print("extract {} done! input to continue".format(apkPath))
            # input()