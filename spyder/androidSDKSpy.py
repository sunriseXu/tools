#coding=utf-8
import requests
import os
import sys
import re
import argparse
from bs4 import BeautifulSoup
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
    allDesc = ''
    for hi in h:
        allDesc = allDesc+ ' ' + hi.xpath('string(.)').strip()
    allDesc = allDesc.replace('\n',' ')
    allDesc = ' '.join(allDesc.split())
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


def main():
    filePath = 'D:/Android/android-sdk/docs/reference/android/bluetooth/BluetoothDevice.html'
    # filePath = 'spyder/test.html'
    htmlContent = FileUtils.readFile(filePath)
    fileResDictPath = './BlueTooth.json'
    # # # 类名：{继承关系：[], 方法：{方法名：{描述：str，参数：{param1:desc,param2:desc},返回：{类型：str，描述：str}}}}
    classDict = {}

    classDict['Inheritance'] = None
    classDict['Functions'] = {}
    # # # 获取文件的所有继承类 # # #
    succList = []
    succXpath = '//table[1]'
    se = etree.HTML(htmlContent)
    succRes = se.xpath(succXpath)
    # print succRes
    if len(succRes)>0:
        # wtf = succRes[0].xpath('.//td[@class="jd-inheritance-class-cell"]') #//*[@id="jd-content"]/table[1]/tbody/tr[2]/td[2]
        #过滤所有含有相应class的td标签，获取它们之间的字符串
        wtf = getAllTextByTag(succRes[0],'.//td[@class="jd-inheritance-class-cell"]')
        if wtf:
            succList = wtf.split()
    # # # 结束 结果存入succList中 # # # 
    classDict['Inheritance'] = succList
    classDict['ClassName'] = succList[-1]

    apiRex = r'<A NAME="(.*?)">.*?</A>'
    items = RexUtils.rexSplit(apiRex, htmlContent)
    validRex = r'<A NAME="(.*?\(.*?\))"></A>'
    idx = 0
    for item in items:
        idx += 1

        res = RexUtils.rexFind(validRex,item)
        if len(res)==0:
            continue
        
        functionDict = {}

        functionName = res[0]
        classDict['Functions'][functionName] = functionDict

        ei = etree.HTML(item)
        ediv = ei.xpath('//div')
        ei = ediv[0]

        # .//p and //p is totally different
        allDesc = getAllTextByTag(ei,'.//p')
        
        functionDict['Description'] = allDesc
        functionDict['Parameters'] = ''
        functionDict['Returns'] = ''
        functionDict['Throws'] = ''
        functionDict['Permissions'] = ''
        permissionList = []
        hrefs = ei.xpath('.//a/@href')
        for href in hrefs:
            bsName = os.path.basename(href)
            if ('Manifest.permission' in bsName) and (bsName not in permissionList):
                permissionList.append(bsName)
        functionDict['Permissions'] = permissionList

        tables = ei.xpath('//table')
        for myTable in tables:
            myTag = myTable.xpath('.//th/text()')[0]
            allRows = getTableRows(myTable)
            if myTag in 'Parameters':
                functionDict['Parameters'] = allRows
            elif myTag in 'Returns':
                functionDict['Returns'] = allRows
            elif myTag in 'Throws':
                functionDict['Throws'] = allRows
            else:
                print 'some else'
    # FileUtils.writeDict(classDict, fileResDictPath)

if __name__ == "__main__":
    sdkRefDir = 'D:\\Android\\android-sdk\\docs\\reference'
    FileUtils.listDirRecur(sdkRefDir)