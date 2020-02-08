# -*- coding:utf-8 -*-
import subprocess
import shutil
import os
import argparse
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

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="recompile!!")
    parser.add_argument('-s', '--srcApk', help='srcApk', nargs='?', default="")
    parser.add_argument('-d', '--decompilePath', help='decompiledir', nargs='?', default="")
    parser.add_argument('-r', '--replacedDir', help='replaced dirname', nargs='?', default="")
    parser.add_argument('-o', '--outputApk', help='resigned apk path', nargs='?', default="")
    parser.add_argument('-k', '--keypath', help='passwd path', nargs='?', default="")

    args = parser.parse_args()

    srcApk = args.srcApk
    decompilePath = args.decompilePath
    replaceDir = args.replacedDir
    keyPath = args.keypath
    outputApk = args.outputApk

    decompileFlag = True
    repackageFlag = True
    signFlag = True
    srcPath = srcApk
    destPath = decompilePath
    repactApkPath = outputApk
    #反编译
    if decompileFlag:
        print("start to decompile...")
        
        if os.path.exists(destPath):
            print("remove origin dir...")
            shutil.rmtree(destPath)
        decompileApk(srcPath,destPath)
        print("decompile success...")

    taobaoDir = os.path.join(destPath,'smali\\com\\taobao')
    trueTaobao = os.path.join(replaceDir,'taobao')

    deRobvDir = os.path.join(destPath,'smali\\de')
    trueDeRobv = os.path.join(replaceDir,'de')

    weishuepicDir = os.path.join(destPath,'smali\\me\\weishu\\epic') 
    trueepic = os.path.join(replaceDir,'me\\weishu\\epic')

    weishuexposedDir = os.path.join(destPath,'smali\\me\\weishu\\exposed')
    trueexposed = os.path.join(replaceDir,'me\\weishu\\exposed')

    weishureflectionDir = os.path.join(destPath,'smali\\me\\weishu\\reflection')
    truereflection = os.path.join(replaceDir,'me\\weishu\\reflection')

    libDir = os.path.join(destPath,'lib\\armeabi-v7a')  
    truelib = os.path.join(replaceDir,'armeabi-v7a')

    dirList = [
        (taobaoDir,trueTaobao),(deRobvDir,trueDeRobv),
        (weishuepicDir,trueepic),(weishuexposedDir,trueexposed),
        (weishureflectionDir,truereflection),(libDir,truelib)
    ]

    for oriDir,trueDir in dirList:
        if os.path.exists(oriDir):
            shutil.rmtree(oriDir)
        mkdir(oriDir)
        copytree(trueDir,oriDir)

    #重打包
    # if repackageFlag:
    #     if os.path.exists(repactApkPath):
    #         os.remove(repactApkPath)
    #     print("start to repackage...")
    #     recompileApk(destPath, repactApkPath)
            
    # #签名
    # passwd = '123456'
    # alias = 'demo.keystore'
    # if signFlag:
    #     print("start to sign apk...")
    #     signApk(keyPath,passwd,repactApkPath,alias)


