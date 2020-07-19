#coding=utf-8
import os
import sys
# pwd = os.path.dirname(os.path.realpath(__file__))
pwd = os.getcwd()
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)
from modules import FileUtils
from modules import CollectionUtils

from modules import RexUtils
from modules import AdbUtils
from modules import ApkUtils
from modules.FileUtils import EasyDir
from modules import InteractUtils
from modules import ThreadUtils
import os
import shutil
import random
import logging
import sys
import time
from datetime import datetime
import argparse 
from modules import InteractUtils
import random
import re

def splitFullMethodName2(item):
    '''
    基础重要方法，对完整方法名进行分离成 类名 方法名 参数
    输入：
        item：完整方法名
    输出：
        方法名的分解
    '''
    tmp = item.strip().split('(')
    fullName = tmp[0]
    params = tmp[1].strip(')')
    fullNameList = fullName.split('.')
    clazz = fullNameList[0:-1]
    clazzName = '.'.join(clazz)
    methodName = fullNameList[-1].strip()
    # methodIdentifier = methodName+params
    return clazzName, methodName, params
xposedPointString = '''
    final String logName{} = "{}";
    XC_MethodHook methodHook{} = new XC_MethodHook() {{
        @Override
        protected void afterHookedMethod(MethodHookParam param) throws Throwable {{
            
            Xlog.d(logName{});
                    
        }}
    }};
    try {{
        className = "{}";
        methodName = "{}";
        hookclass = classloader.loadClass(className);
        Object[] paramAndCall = {{ 
            {}
            methodHook{}
        }};

        XposedHelpers.findAndHookMethod(hookclass, methodName, paramAndCall);
    }} catch (Exception e) {{
        Xlog.e(TAG, logName{}, e);
        return;
    }}

'''

xposedPointConstrString = '''
    final String logName{} = "{}";
    XC_MethodHook methodHook{} = new XC_MethodHook() {{
        @Override
        protected void afterHookedMethod(MethodHookParam param) throws Throwable {{
            
                    Xlog.d(logName{});
                  
        }}
    }};
    try {{
        className = "{}";
        hookclass = classloader.loadClass(className);
        Object[] paramAndCall = {{ 
            {}
            methodHook{}
        }};

        XposedHelpers.findAndHookConstructor(hookclass, paramAndCall);
    }} catch (Exception e) {{
        Xlog.e(TAG, logName{}, e);
        return;
    }}

'''

def appendContent2File(outPath, content):
    with open(outPath, 'a+') as f:
        f.write(content)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="find dex!!")
    parser.add_argument('-b', '--basePath', nargs='?',default="") #多个参数 默认放入list中 +表示至少一个 + 就放在list中
    # parser.add_argument('-d', '--tarPath', nargs='?',default="")
    parser.add_argument('-c', '--caller', help='tmp dir', nargs='?',default="")
    parser.add_argument('-o', '--outPath', help='get all class dict', nargs='?',default="")
    # parser.add_argument('-l', '--caller', help='tmp dir', nargs='?',default="")

    args = parser.parse_args() 
    basePath=args.basePath
    outPath = args.outPath
    caller = args.caller

    methodList = FileUtils.readList(basePath)

    # Initialising values 
    occurrence = 2
    
    methodList2 = []
    for item in methodList:
        
        # Finding nth occurrence of substring 
        inilist = [m.start() for m in re.finditer(r" ", item)] 
        # print(inilist)
        if len(inilist)>= occurrence: 
            methodList2.append(item[inilist[occurrence]:])


    # methodList = [i.split()[-1].strip() for i in methodList]
    methodList2 = list(set(methodList2))
    methodList3 = []
    fullHookStr = '''
    @Override
    public void doHook() {{
        {}
    }}
    '''
    hookListString = ''
    idx = 0
    for item in methodList2:
        idx+=1
        item = item.strip()
        if not item.startswith('java') and not item.startswith('android'):
            methodList3.append(item)
            className, methodN, param = splitFullMethodName2(item)
            paramList = param.split(',')
            paramList = [i.strip() for i in paramList if len(i)>0]
            # print(paramList)
            paramStr = ''
            if len(paramList) > 0:
                for p in paramList:
                    p = p.strip()
                    paramStr += '"'+p+'", '
            if 'init' in methodN:
                xposedPointStringtmp = xposedPointConstrString.format(idx, item+" called", idx, idx, className, paramStr, idx, idx)
            else:
                xposedPointStringtmp = xposedPointString.format(idx, item+" called", idx,idx, className, methodN, paramStr, idx, idx)
            hookListString += xposedPointStringtmp
    FileUtils.writeFile(outPath, fullHookStr.format(hookListString))