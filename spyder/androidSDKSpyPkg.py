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
    baseUrl = 'https://developer.android.com'
    homeDir = os.getenv("HOME")
    baseDir = os.path.join(homeDir,'androidSdkInAll')
    FileUtils.mkdir(baseDir)
    fileResDictDir = os.path.join(baseDir,'classRes')
    FileUtils.mkdir(fileResDictDir)

    classesUrl = 'https://developer.android.com/reference/classes'
    classSummaryPath = baseDir + '/reference/classes.html'

    # packagesUrl = 'https://developer.android.com/reference/packages'
    # packagesSummaryPath = baseDir + '/reference/packages.html'

    supportPkgUrl = 'https://developer.android.com/reference/android/support/packages'
    supPkgSPath = baseDir + '/reference/android/support/packages.html'
    # https://developer.android.com/reference/android/support/test/packages
    # https://developer.android.com/reference/android/databinding/packages
    # https://developer.android.com/reference/android/support/wearable/packages
    packagesUrl = 'https://developer.android.com/reference/android/support/wearable/packages'
    packagesSummaryPath = baseDir + '/reference/android/support/wearable/packages.html'



    # classesData = fetchData(classSummaryPath, classesUrl)
    # packagesData = fetchData(supPkgSPath, supportPkgUrl)
    packagesData = fetchData(packagesSummaryPath, packagesUrl)
    if not packagesData:
        print 'classes fetching failed!'
        sys.exit()
    
    # 爬取pkg页面中每一个pkg的链接
    pkgXpath = './/table/tr'
    pkgList = getElementInRawHtml(packagesData,pkgXpath)
    # print len(pkgList)
    # 边爬边存！并且以某种目录的形式存起来
    # 爬的时候检查本地是否有缓存，优先从本地读取，如果没有那么从网上读取
    # 检查链接是否以 /reference开头，否则怎么办？否则停止 debug， 但是要注意下次需要从中断处开始
    
    pkgLen = len(pkgList)

    for pkgE in pkgList:
        # 获取具体链接
        pkgLink = pkgE.xpath('.//a/@href')[0]

        pkgUrl = baseUrl + pkgLink
        pkgLocalPath = baseDir + pkgLink

        if 'http' in pkgLink:
            pkgUrl = pkgLink
            pkgLocalPath = baseDir + '/reference' + pkgLink.split('/reference')[1]

        # if 'annotation' not in pkgLink:
        #     continue
        # print 'annotation found'
        # print pkgLink
        # raw_input()
        # 根据链接获得特定pkg的页面
        pkgData = fetchData(pkgLocalPath, pkgUrl)
        pkgE = etree.HTML(pkgData)

        #<table class="jd-sumtable-expando">
        tableXpath = './/table[@class="jd-sumtable-expando"]'
        tablesList = pkgE.xpath(tableXpath)
        classList = []
        for tableE in tablesList:
            rowsList = tableE.xpath('.//tr')
            classList += rowsList

        # 然后获取每个类的链接及页面
        #<tr data-version-added
        
        # classXpath = './/tr[@data-version-added]'
        # classList = pkgE.xpath(classXpath)
        idx = 0
        classLen = len(classList)
        for myClass in classList:
            idx += 1
            # if idx % 100 == 0:
                
            classDict = {}
            classDict['ClassName'] = ''
            classDict['AddedLevel'] = ''
            classDict['DeprecatedLevel'] = ''
            classDict['Functions'] = ''
            classDict['Inheritance'] = None


            className = myClass.xpath('.//td[@class="jd-linkcol"]/a/text()')[0]
            # print className
            # raw_input()

            classAddedLevel = myClass.xpath('@data-version-added')
            if classAddedLevel:
                classAddedLevel = classAddedLevel[0]
            else:
                classAddedLevel = ''
            classDeprecatedLevel = myClass.xpath('@data-version-deprecated')
            if classDeprecatedLevel:
                classDeprecatedLevel = classDeprecatedLevel[0]
            else:
                classDeprecatedLevel = ''
            classDict['ClassName'] = ''
            classDict['AddedLevel'] = classAddedLevel
            classDict['DeprecatedLevel'] = classDeprecatedLevel



            # print className
            classLink = myClass.xpath('.//td[@class="jd-linkcol"]/a/@href')[0]
            if not className:
                print "className not found"
            if not classLink:
                print 'classLink not found'
            if not classLink.startswith('/reference'):
                print 'classlink erro'
            classOnlineLink = baseUrl + classLink
            localPath = baseDir + classLink
            if 'http' in classLink:
                classOnlineLink = classLink
                localPath = baseDir + '/reference' + classLink.split('/reference')[1]
            classHtmlData = fetchData(localPath, classOnlineLink)
            # classHtmlData = FileUtils.readFile('C:/Users/limin/androidSdkInAll/reference/android/bluetooth/BluetoothDevice.html')
            print 'No %d/%d' %(idx,classLen)
            print 'className: %s; link: %s; localPath: %s' %(className, classOnlineLink,localPath)

            # # 获取类页面所有类成员的list # #
            methodXpath = './/div[@data-version-added]'
            classHtmlE = etree.HTML(classHtmlData)
            methodEList = classHtmlE.xpath(methodXpath)
            # # methodEList 包含所有成员的列表xpath元素 # #

            # # # 获取文件的所有继承类 API 24, 23 # # #
            succList = []
            succXpath = './/table[@class="jd-inheritance-table"]'
            succRes = classHtmlE.xpath(succXpath)
            if len(succRes)>0:
                #过滤所有含有相应class的td标签，获取它们之间的字符串
                wtf = getAllTextByTag(succRes[0],'.//td[@class="jd-inheritance-class-cell"]')
                if wtf:
                    # 去除 \xa0 空白字符
                    succList = [' '.join(i.split()) for i in wtf]
            # # # 结束 结果存入succList中 # # # 
            classDict['Inheritance'] = succList
            classDict['ClassName'] = succList[-1]

            jsonName = succList[-1].replace('<','(')
            jsonName = jsonName.replace('>',')')
            jsonName = jsonName.replace('?','!')
            fileResDictPath = os.path.join(fileResDictDir, jsonName+'.json')

            if os.path.exists(fileResDictPath):
                continue

            functionsDict = {}
            classDict['Functions'] = functionsDict

            # mothod 代表了每个类成员的xpath元素，首先获取成员名字
            methodFX = './/h3[@class="api-name"]/@id'
            for methodE in methodEList:
                eleName = methodE.xpath(methodFX)
                if len(eleName) != 1:
                    continue
                eleName = eleName[0]
                # # 判断成员名是否包含两个括号 # #
                methodRex = r'.*?\(.*?\)'
                res = RexUtils.rexFind(methodRex,eleName)
                if len(res) == 0:
                    continue
                functionDict = {}
                # 方法名提取完毕
                methodName = eleName
                functionsDict[methodName] = functionDict

                functionDict['Description'] = ''
                functionDict['FullName'] = ''
                functionDict['Parameters'] = ''
                functionDict['Returns'] = ''
                functionDict['Throws'] = ''
                functionDict['Permissions'] = ''
                functionDict['AddedLevel'] = ''
                functionDict['DeprecatedLevel'] = ''

                # # 获取函数完整格式，而非仅仅函数名
                # h4 class="jd-details-title"
                fullName = ''
                fullNameXpath = './/pre[@class="api-signature no-pretty-print"]'
                fullName = getAllTextByTag(methodE,fullNameXpath)
                if fullName:
                    # 去除 \xa0 空白字符
                    fullName = ' '.join(fullName[0].split())
                functionDict['FullName'] = fullName

                # # api等级提取 非常关键 # #
                apiLevelXpath = '@data-version-added'
                apiLevelRemovedXpath = '@data-version-deprecated'
                addedLevel = methodE.xpath(apiLevelXpath)[0]
                removedLevel = methodE.xpath(apiLevelRemovedXpath)
                if removedLevel:
                    removedLevel = removedLevel[0]
                    # it's strange that the level sometimes equals 'REL', not too much
                    if (not CollectionUtils.is_number(addedLevel)) or (not CollectionUtils.is_number(removedLevel)):
                        print methodName
                        print addedLevel
                        print removedLevel
                        # raw_input()
                    elif int(addedLevel)>int(removedLevel):
                        print methodName
                        print addedLevel
                        print removedLevel
                        # raw_input()
                    functionDict['DeprecatedLevel'] = removedLevel
                functionDict['AddedLevel'] = addedLevel

                # # 方法描述提取 # #
                fullNameXpath = './/pre[@class="api-signature no-pretty-print"]'
                fullName = getAllTextByTag(methodE,fullNameXpath)
                if fullName:
                    # 去除 \xa0 空白字符
                    fullName = ' '.join(fullName[0].split())
                allDesc = ''
                # .//p and //p is totally different
                allDesc = getAllTextByTag(methodE,'.//p')
                allDesc = ''.join(allDesc)
                allDesc = ' '.join(allDesc.split())
                functionDict['Description'] = allDesc
                # # 方法描述提取完毕 # #

                # 观察到函数的permission在函数描述种，并且包含链接，指向特定permission路径
                permissionList = []
                hrefs = methodE.xpath('.//a/@href')
                for href in hrefs:
                    bsName = os.path.basename(href)
                    if ('Manifest.permission' in bsName) and (bsName not in permissionList):
                        permissionList.append(bsName)
                functionDict['Permissions'] = permissionList
                # # 至此，潜在的permission字段被提取出来

                # # 提取参数 返回 异常信息
                tables = methodE.xpath('.//table')
                for myTable in tables:
                    myTags = myTable.xpath('.//th/text()')
                    if len(myTags) == 0:
                        continue
                    myTag = myTags[0]
                    allRows = getTableRows(myTable)
                    if myTag in 'Parameters':
                        functionDict['Parameters'] = allRows
                    elif myTag in 'Returns':
                        functionDict['Returns'] = allRows
                    elif myTag in 'Throws':
                        functionDict['Throws'] = allRows
                    else:
                        print 'some else'
                        print myTag
                # # 提取完毕 # # 
            print "******************write Dict file******************"
            print fileResDictPath
            FileUtils.writeDict(classDict, fileResDictPath)

