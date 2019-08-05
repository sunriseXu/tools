#coding=utf-8
import requests
import os
import sys
import re
import argparse
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
from modules import CollectionUtils,RexUtils

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

def getElementInRawHtml(rawData, myXpath):
    eRaw = etree.HTML(rawData)
    return eRaw.xpath(myXpath)


if __name__ == "__main__":
    permissionPath = 'D:\\androidsdkdoc\\docs-24_r01\\docs\\reference\\android\\Manifest.permission.html'
    permissionDPath = 'D:\\androidsdkdoc\\permission24.json'
    htmlData = FileUtils.readFile(permissionPath)
    # htmlE = etree.HTML(htmlData)

    # 正则匹配每一个 类成员的描述段
    apiRex = r'<A NAME="(.*?)">.*?</A>'
    items = RexUtils.rexSplit(apiRex, htmlData)

    permissionDict = {'unknown':[]}
    methodFX = './/h3[@class="api-name"]/text()'
    for methodE in items:
        methodE = etree.HTML(methodE)
        eleName = methodE.xpath(methodFX)
        if len(eleName) != 1:
            continue
        eleName = eleName[0]
        print 'Name:'
        print eleName

        prgX = './/p/text()'
        prgList = methodE.xpath(prgX)
        proLevel = ''
        for prg in prgList:
            if 'Protection level:' in prg:
                proLevel = prg.split('Protection level:')[1].strip()
                break
            if 'Not for use by third-party applications' in prg:
                proLevel = 'no-third-party'
        print 'level:'
        print proLevel
        print '\n'
        
        if not proLevel:
            permissionDict['unknown'].append(eleName)
        else:
            if proLevel not in permissionDict:
                permissionDict.update({proLevel:[eleName]})
            else:
                permissionDict[proLevel].append(eleName)
    # print permissionDict
    FileUtils.writeDict(permissionDict,permissionDPath)
        # raw_input()