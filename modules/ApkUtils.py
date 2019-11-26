import os
import sys
import subprocess
from modules.ThreadUtils import execute_command
import modules.AdbUtils
import platform


def unzipApk(apkPath,outPath):
    cmd = 'unzip %s -d %s' %(apkPath,outPath)
    # os.popen(cmd)
    subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()

def apk2smali(apkPath,outPath):
    myPlat = platform.system().lower()
    cmdhead = ''
    if 'windows' in myPlat:
        cmdhead = 'd2j-baksmali.bat'
    elif 'linux' in myPlat:
        cmdhead = 'd2j-baksmali.sh'
    cmd = '%s %s -o %s' %(cmdhead, apkPath, outPath)
    subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT).stdout.read()

def dex2smali(dexPath,outPath):
    apk2smali(dexPath,outPath)
    

if __name__ == "__main__":
    srcpath='C:\\Users\\limin\\Desktop\\tmp2\\com.pac.skgdxa93452.dex'
    outpath='C:\\Users\\limin\\Desktop\\tmp2\\com.pac.skgdxa93452-out'
    dex2smali(srcpath,outpath)