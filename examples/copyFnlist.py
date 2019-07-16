from modules import FileUtils
from modules import CollectionUtils
import time
import subprocess

def log2file(filePath,uid,selectedDevId):
    logcat_file = open(filePath, 'w')
    logcmd='adb %s shell "dmesg |grep %s"' %(selectedDevId,uid)
    print logcmd
    # logcmdarg=logcmd.strip().split()
    handle = subprocess.Popen(logcmd,stdout=logcat_file,stderr=subprocess.PIPE)
    time.sleep(2)
    handle.terminate()
def renameAll(srcDir):
    mylist = FileUtils.listDir2(srcDir)
    for i in mylist:
        srcpath=os.path.join(srcDir,i)
        ri = i.split('log_')[1]
        destpath=os.path.join(srcDir,ri)
        os.rename(srcpath,destpath)
import os
import shutil
if __name__ == "__main__":
    mal1='C:\\Users\\limin\\Desktop\\maltrain_test2500\\trainmalicious'
    mal2='C:\\Users\\limin\\Desktop\\maltrain_test2500\\testmalicious_ruled500'
    mal3='C:\\Users\\limin\\Desktop\\allMal\\malAll'
    mal4=''
    mal5=''

    mallist1=FileUtils.listDir2(mal1)
    mallist2=FileUtils.listDir2(mal2)
    mallist3=FileUtils.listDir2(mal3)
    dest = 'C:\\Users\\limin\\Desktop\\'
    listpath='C:\\Users\\limin\\Desktop\\fnlist.txt'
    fnlist = FileUtils.readList(listpath)
    for fn in fnlist:
        fn = fn+'.txt'
        destpath= os.path.join(dest, fn)
        if fn in mallist1:
            srcpath = os.path.join(mal1,fn)
            shutil.copy(srcpath,destpath)
        elif fn in mallist2:
            srcpath = os.path.join(mal2,fn)
            shutil.copy(srcpath,destpath)
        elif fn in mallist3:
            srcpath = os.path.join(mal3,fn)
            shutil.copy(srcpath,destpath)
        else:
            print 'fn %s not found' %fn
    
    
    
    