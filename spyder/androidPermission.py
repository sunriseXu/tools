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
    