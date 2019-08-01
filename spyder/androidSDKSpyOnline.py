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




if __name__ == "__main__":
    baseUrl = 'https://developer.android.com'
    classesUrl = 'https://developer.android.com/reference/classes'
    # classesData = SpyderUtils.getUrlTextEtree(classesUrl)
    classesPath = 'C:\\Users\\limin\\Desktop\\today\\test.html'
    classesData = FileUtils.readFile(classesPath)
    classesDataE = etree.HTML(classesData)

    # allClasses = classesDataE.xpath('//*[@id="gc-wrapper"]/div/devsite-content/article/article/div[3]/div[1]/table/tbody')
    # print len(allClasses)
    classList = classesDataE.xpath('.//tr[@data-version-added]')
    print len(classList)
    # 边爬边存！并且以某种目录的形式存起来
    # 爬的时候检查本地是否有缓存，优先从本地读取，如果没有那么从网上读取
    # 检查链接是否以 /reference开头，否则怎么办？否则停止 debug， 但是要注意下次需要从中断处开始

    homeDir = os.getenv("HOME")
    baseDir = os.path.join(homeDir,'androidSdkInAll')
    # baseDir = 'C:/Users/limin/Desktop/androidSdkInAll'
    FileUtils.mkdir(baseDir)
    print baseDir
    input()
    

    classLen = len(classList)
    idx = 0

    for myClass in classList:
        idx += 1
        
        className = myClass.xpath('.//td[@class="jd-linkcol"]/a/text()')[0]
        classLink = myClass.xpath('.//td[@class="jd-linkcol"]/a/@href')[0]
        # print className 
        if not className:
            print "className not found"
        if not classLink:
            print 'classLink not found'
        if not classLink.startswith('/reference'):
            print 'classlink erro'



        classOnlineLink = baseUrl + classLink
        localPath = baseDir + classLink
        
        print 'No %d/%d' %(idx,classLen)
        print 'className: %s; link: %s' %(className, classOnlineLink)

        classHtmlData = ''
        
        if os.path.exists(localPath):
            print 'file in local'
            classHtmlData = FileUtils.readFile(localPath)
        else:
            print 'file online, fetching'
            classHtmlData = SpyderUtils.getUrlContent(classOnlineLink)
            FileUtils.writeFile(localPath,classHtmlData.encode('utf-8'))
            print 'file written'
        # input()


