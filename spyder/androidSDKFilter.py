#coding=utf-8
import requests
import os
import sys
import re
import argparse
# from bs4 import BeautifulSoup
from datetime import datetime
import lxml
from lxml import etree
import logging
logging.basicConfig()
l = logging.getLogger("spyderAndroid")


pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules import SpyderUtils
from modules import FileUtils
from modules import CollectionUtils,RexUtils,InteractUtils

def getMatchContent(description,rex,lowerFlag=False):
	content=""
	if lowerFlag:
		content=description.lower()
	else:
		content=description
	pattern=re.compile(rex,re.S)
	items = re.findall(pattern,content)
	return items

def getAllTextByTag(ehtml,xRef):
    h = ehtml.xpath(xRef)
    allDesc = []
    for hi in h:
        allDesc.append(hi.xpath('string(.)').strip())
    return allDesc

def getTableRows(myTable):
    # print 'deal with table ##################'
    eRows = myTable.xpath('.//tr')
    allRows = []
    for eRow in eRows:
        eCols = eRow.xpath('.//td')
        oneRow= []
        for eCol in eCols:
            #提取标签下所有字符串text
            res=eCol.xpath('string(.)')
            res = ' '.join(res.split())
            oneRow.append(res)
        if oneRow:
            allRows.append(oneRow)
    return allRows
def getTableRows2(myTable):
    # print 'deal with table ##################'
    eRows = myTable.xpath('.//tr')
    allRows = []
    if not eRows:
        res=getAllTextByTag(myTable,'.//li')
        res = ''.join(res)
        res = ' '.join(res.split())
        allRows.append(['',res])
        return allRows
    for eRow in eRows:
        eCols = eRow.xpath('.//td|.//th')
        oneRow= []
        for eCol in eCols:
            #提取标签下所有字符串text
            res=eCol.xpath('string(.)')
            res = ' '.join(res.split())
            oneRow.append(res)
        if oneRow:
            allRows.append(oneRow)
    return allRows    

def getTableRowsLinks(myTable):
    eRows = myTable.xpath('.//tr')
    allRows = []
    for eRow in eRows:
        eCols = eRow.xpath('.//td')
        oneRow= []
        for eCol in eCols:
            #提取标签下所有字符串text
            href=eCol.xpath('.//a/@href')
            if len(href)>0:
                oneRow.append(href[0])
        if oneRow:
            allRows.append(oneRow[0])
    return allRows

def fetchData(localPath, onlineLink):
    myData = ''
    if os.path.exists(localPath):
        # l.warning('fetching from local: %s', localPath)
        myData = FileUtils.readFile(localPath)
    else:
        l.warning('fetching from online: %s', onlineLink)
        myData = SpyderUtils.getUrlContent(onlineLink)
        if myData:
            FileUtils.writeFile(localPath,myData.encode('utf-8'))
        else:
            l.warning('fetching online failed!')
            pass
    return myData

if __name__ == "__main__":
    apiLevel = 24
    allDictDir = 'C:\\Users\\limin\\androidSdkInAll\\classRes'

    allDictPaths = FileUtils.listDir(allDictDir)
    classList = []

    for dictPath in allDictPaths:
        classDict = FileUtils.readDict(dictPath)
        classAddApiLevel = classDict['AddedLevel']

        if 'REL' in classAddApiLevel:
            continue
        if int(classAddApiLevel) <= apiLevel:
            classList.append(classDict['ClassName'])
    print len(classList)

    anotherList = []
    anotherDir = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk24_bk\\jsonRes'
    allDictPaths = FileUtils.listDir(anotherDir)
    # print len(allDictPaths)
    for dictPath in allDictPaths:
        classDict = FileUtils.readDict(dictPath)
        className = classDict['ClassName']
        anotherList.append(className)
    print len(anotherList)
    print len(CollectionUtils.listIntersection(classList,anotherList))
    diffList =  CollectionUtils.listDifference(anotherList,classList)
    diffList = sorted(diffList)
    InteractUtils.showList(diffList)