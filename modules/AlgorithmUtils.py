# -*- coding:utf-8 -*-
from tools.modules.FileUtils import *

def culculateSuccessive(myList, myElement, myWindow):
    '''
    culculate successive(within myWindow) element in myList, return its count
    '''
    maxcount=0
    icount=0
    gap=0
    flag=True
    inGap=False
    for element in myList:
        if myElement in element:
            flag=False
            inGap=False
            icount+=1
            gap=0
        else:
            if flag and (not inGap):
                gap+=1
            flag=True
        if gap>=myWindow-1:
            if icount>maxcount:
                maxcount=icount
            icount=0
            gap=0
            inGap=True
    maxcount=icount
    return maxcount

if __name__ == "__main__":
    testlist = ['a','b','b','a','a','a']
    print culculateSuccessive(testlist,'a',2)