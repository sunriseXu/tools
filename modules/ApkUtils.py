import os
import sys
import subprocess

def unzipApk(apkPath,outPath):
    cmd = 'unzip %s -d %s' %(apkPath,outPath)
    # os.popen(cmd)
    subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()

def decompileApk(apkPath,outPath):
    cmd = 'd2j-baksmali.sh %s -o %s' %(apkPath,outPath)
    subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()