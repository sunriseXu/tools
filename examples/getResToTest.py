import os
import sys
pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules import FileUtils
from modules import CollectionUtils






if __name__ == "__main__":
    dir1 = '/home/limin/Desktop/logs_huawei3/logs/lastTest.txt'
    dir2 = '/home/limin/Desktop/logs_origin/logs/lastTest.txt'
    dir3 = '/home/limin/Desktop/logs_pixel1/logs/lastTest.txt'
    dir4 = '/home/limin/Desktop/logs_huawei1/logs/lastTest.txt'
    dir5 = '/home/limin/Desktop/logs_huawei2/logs/lastTest.txt'
    dir6 = '/home/limin/Desktop/logs_pixel2_2/logs/lastTest.txt'
    dir7 = '/home/limin/Desktop/logs_45610/logs/lastTest.txt'
    dir8 = '/home/limin/Desktop/logs_53190/logs/lastTest.txt'
    dir9 = '/home/limin/Desktop/logs_60156/logs/lastTest.txt'

    dir10 = '/home/limin/Desktop/logs_huawei1/toTest.txt'

    t1 = FileUtils.readList(dir1)
    t2 = FileUtils.readList(dir2)
    t3 = FileUtils.readList(dir3)
    t4 = FileUtils.readList(dir4)
    t5 = FileUtils.readList(dir5)
    t6 = FileUtils.readList(dir6)
    t7 = FileUtils.readList(dir7)
    t8 = FileUtils.readList(dir8)
    t9 = FileUtils.readList(dir9)
    
    allTest = CollectionUtils.listMerge(t1,t2,t3,t4,t5,t6,t7,t8,t9)
    print(len(allTest))

    t10 =FileUtils.readList(dir10)
    print(len(t10))

    restList = CollectionUtils.listDifference(t10,allTest)
    print(len(restList))
    destPath = '/home/limin/Desktop/toTest4w.txt'
    FileUtils.writeList(restList,destPath)



