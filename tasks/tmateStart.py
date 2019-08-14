import os
import sys
import psutil
pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules import FileUtils
from modules import CollectionUtils
from modules import ThreadUtils

if __name__ == '__main__':
    pidList = psutil.pids()
    for pid in pidList:
        p = psutil.Process(pid)
        print(p.name())
