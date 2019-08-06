# -*- coding:utf-8 -*-
import urllib
# import urllib2
import re
import os
import json
import sys



def rexSplit(rex,content):
    '''
    this function will split content with the delimiter which defined by rex, 
    and return the segments with delimiter in a list
    eg: "#aaa#bbb#ccc" => ['#aaa','#bbb','#ccc']
    '''
    pattern=re.compile(rex,re.S)
    myIterator = re.finditer(pattern,content)
    head=0
    end=0
    foundFlag=False
    mylist=[]
    idx=0
    for i in myIterator:
        foundFlag=True
        end=i.start()
        if idx!=0:
            mylist.append(content[head:end])
        head=end
        idx+=1
    if foundFlag:
        mylist.append(content[end:len(content)+1])
    return mylist

def rexFind(rex,content):
    '''
    simplely find all string which matches rex in content, return list
    
    '''
    pattern=re.compile(rex,re.S)
    resList=re.findall(pattern,content)
    return resList

if __name__ == "__main__":
    rexSplit(r'#','#aaa#bbb#ccc#ddd')    