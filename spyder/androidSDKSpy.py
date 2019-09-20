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
import uuid
reload(sys)

sys.setdefaultencoding('utf-8')


pwd = os.path.dirname(os.path.realpath(__file__))
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

from modules import SpyderUtils
from modules import FileUtils
from modules import CollectionUtils,RexUtils, InteractUtils
def create_uid():
    return str(uuid.uuid1())
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

def getAllTextByTagDesc(ehtml,xRef):
    h = ehtml.xpath(xRef)
    allDesc = []
    hrefs = []
    if len(h) == 0:
        return ''
    for hi in h:
        text = hi.xpath('string(.)').strip()
        allDesc.append(text)
        hreftmp = hi.xpath('.//a')
        if len(hreftmp)>0:
            hrefs = hrefs+hreftmp
    allDesc = ''.join(allDesc)
    # [' '.join(i.split()) for i in allDesc]
    allDesc = ' '.join(allDesc.split())
    # print allDesc
    textWithHref = []
    idx = 0
    # print len(hrefs)
    for href in hrefs:
        idx += 1
        links = href.xpath('@href')
        subtexts = href.xpath('text()')
        if len(links)==0 or len(subtexts)==0:
            continue
        link = links[0].strip()
        subtext = subtexts[0].strip()
        subtext = ' '.join(subtext.split()).strip()
        if not subtext or '/reference/' not in link:
            continue
        textWithHref.append((subtext,link,create_uid()))
    textWithHref = sorted(textWithHref,key = lambda i:len(i[0]),reverse=True)
    # print textWithHref
    for subtext,href,myTag in textWithHref:
        # print 'replace {} to {}'.format(subtext, myTag)
        allDesc = allDesc.replace(subtext,myTag)
    for subtext,href,myTag in textWithHref:
        # print 'replace {} to {}'.format(myTag, subtext)
        allDesc = allDesc.replace(myTag,'[{}]({})'.format(subtext,href))
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
def getSeeAlso(ec):
    seeAlsoList = []
    seealso = ec.xpath('.//div')
    for sc in seealso:
        tmp = sc.xpath('.//p/b/text()')
        if 'See also:' in ' '.join(tmp):
            lis = sc.xpath('.//ul/li')
            for li in lis:
                hrefs = li.xpath('.//a/@href')
                texts = li.xpath('string(.)').strip()
                href = ''
                if len(hrefs)>0:
                    href = hrefs[0]
                seeAlsoList.append([texts, href])
            return seeAlsoList
    return seeAlsoList
def getSeeAlso2(ec):
    seeAlsoList = []
    seealso = ec.xpath('.//div[@class="jd-tagdata"]')
    for sc in seealso:
        tmp = sc.xpath('.//h5/text()')
        if 'See Also' in ' '.join(tmp):
            lis = sc.xpath('.//ul/li')
            for li in lis:
                hrefs = li.xpath('.//a/@href')
                texts = li.xpath('string(.)').strip()
                href = ''
                if len(hrefs)>0:
                    href = hrefs[0]
                seeAlsoList.append([texts, href])
            return seeAlsoList
    return seeAlsoList


def main(filePath, fileResDictDir, testedList, apiLevel):
    print filePath
    htmlContent = FileUtils.readFile(filePath)
    # # # 类名：{继承关系：[], 方法：{方法名：{描述：str，参数：{param1:desc,param2:desc},返回：{类型：str，描述：str}}}}
    classDict = {}

    classDict['Inheritance'] = None
    classDict['ClassDesc'] = ''
    classDict['Functions'] = {}


    # # # 获取文件的所有继承类 API 24, 23 # # #
    succList = []
    succXpath = './/table[@class="jd-inheritance-table"]'
    se = etree.HTML(htmlContent)
    succRes = se.xpath(succXpath)
    if len(succRes)>0:
        #过滤所有含有相应class的td标签，获取它们之间的字符串
        wtf = getAllTextByTag(succRes[0],'.//td[@class="jd-inheritance-class-cell"]')
        if wtf:
            # 去除 \xa0 空白字符
            succList = [' '.join(i.split()) for i in wtf]
    # # # 结束 结果存入succList中 # # # 
    # print succList
    
    classDict['Inheritance'] = succList
    classDict['ClassName'] = succList[-1]
    if succList[-1] in testedList:
        return ''
    # 确定字典文件名
    jsonName = succList[-1].replace('<','(')
    jsonName = jsonName.replace('>',')')
    jsonName = jsonName.replace('?','!')
    fileResDictPath = os.path.join(fileResDictDir, jsonName+'.json')

    # 匹配类描述
    if apiLevel in range(24,30):
        classDescX = '//*[@id="jd-content"]/p[2]'
        classDesc = getAllTextByTagDesc(se,classDescX)
        classDict['ClassDesc'] = classDesc
    else:
        # //*[@id="jd-content"]/div[1]
        classDescX = '//*[@id="jd-content"]/div[1]'
        classDesc = getAllTextByTagDesc(se,classDescX)
        classDict['ClassDesc'] = classDesc


    # 正则匹配每一个 类成员的描述段
    apiRex = r'<A NAME="(.*?)">.*?</A>'
    items = RexUtils.rexSplit(apiRex, htmlContent)

    # 筛去那些非函数，例如成员变量的描述
    validRex = r'<A NAME="(.*?\(.*?\))"></A>'
    idx = 0
    for item in items:
        idx += 1
        # 获取成员变量或者方法的名字，用括号过滤
        res = RexUtils.rexFind(validRex,item)
        if len(res)==0:
            continue
        # 至此 成员函数到达这里
        functionDict = {}

        functionName = res[0]
        classDict['Functions'][functionName] = functionDict
        print '#### %s ####' %functionName
        
    

        # 获取每个成员函数的段，因为上面正则匹配不太准确，会匹配多余的段
        ei = etree.HTML(item)
        ediv = ei.xpath('//div')
        ei = ediv[0]
        # # 至此 ei 正式表达每个成员函数的段

        # # 获取函数完整格式，而非仅仅函数名
        # h4 class="jd-details-title"
        fullName = ''
        fullNameXpath = ''
        if apiLevel in range(24,30):
            fullNameXpath = './/pre[@class="api-signature no-pretty-print"]'
        elif apiLevel in [23,22,21,19,18,17,16,15,14]:
            fullNameXpath = './/h4[@class="jd-details-title"]'
        fullName = getAllTextByTag(ei,fullNameXpath)
        if fullName:
            # 去除 \xa0 空白字符
            fullName = ' '.join(fullName[0].split())
        ## 至此 完整格式完成

        # 由于观察到 函数的描述在某些特定标签下面，依api不同有所变化 所以提取此标签下面所有的文字
        allDesc = ''
        if apiLevel in range(24,30):
            # .//p and //p is totally different
            allDesc = getAllTextByTagDesc(ei,'.//p')
            # allDesc = ''.join(allDesc)
            # allDesc = ' '.join(allDesc.split())
        elif apiLevel in [23,22,21,19,18,17,16,15,14]:
            #div class="jd-tagdata jd-tagdescr"
            allDesc = getAllTextByTagDesc(ei,'.//div[@class="jd-tagdata jd-tagdescr"]')
            # allDesc = ''.join(allDesc)
            # allDesc = ' '.join(allDesc.split())
        # # 至此 allDesc 字符串 包含所有描述
        
        functionDict['Description'] = allDesc
        functionDict['FullName'] = fullName
        functionDict['Parameters'] = ''
        functionDict['Returns'] = ''
        functionDict['Throws'] = ''
        functionDict['Permissions'] = ''
        functionDict['SeeAlso'] = ''

        # 观察到函数的permission在函数描述种，并且包含链接，指向特定permission路径
        permissionList = []
        hrefs = ei.xpath('.//a/@href')
        for href in hrefs:
            bsName = os.path.basename(href)
            if ('Manifest.permission' in bsName) and (bsName not in permissionList):
                permissionList.append(bsName)
        functionDict['Permissions'] = permissionList
        # # 至此，潜在的permission字段被提取出来

        #观察到api24中 所有参数描述，返回类型描述，异常都在表格中，所以提取出表格
        if apiLevel in range(24,30):
            tables = ei.xpath('//table')
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
            seeAlsoList = getSeeAlso(ei)
            functionDict['SeeAlso'] = seeAlsoList
        elif apiLevel in [23,22,21,19,18,17,16,15,14]:
            # div class="jd-tagdata">
            tables = ei.xpath('//div[@class="jd-tagdata"]')
            for myTable in tables:
                myTags = myTable.xpath('.//h5/text()')
                if len(myTags) == 0:
                    continue
                myTag = myTags[0]
                print myTag
                allRows = getTableRows2(myTable)
                if myTag in 'Parameters':
                    functionDict['Parameters'] = allRows
                elif myTag in 'Returns':
                    functionDict['Returns'] = allRows
                elif myTag in 'Throws':
                    functionDict['Throws'] = allRows
                else:
                    print 'some else'
            seeAlsoList = getSeeAlso2(ei)
            functionDict['SeeAlso'] = seeAlsoList
        # #至此，表格信息提取完毕
    # 将结果写入字典
    FileUtils.writeDict(classDict, fileResDictPath)
    return succList[-1]


import argparse 
import sys
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="test!!")
    parser.add_argument('-e', '--level', help='test time', nargs='?',type=int, default=25)
    args = parser.parse_args() 
    apiLevel = args.level
    # sdkRefDir = 'D:\\androidsdkdoc\\docs-%d\\reference' %apiLevel
    sdkRefDir = 'D:\\androidsdkdoc\\docs-%d\\offline-sdk\\reference' %apiLevel
    if not os.path.exists(sdkRefDir):
        print 'dir not exists!'
        sys.exit()
    # sdkRefDir = 'D:\\Android\\android-sdk\\docs\\reference' 
    fileResDictDir = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk%d\\jsonRes' %apiLevel
    noFilePath = 'C:\\Users\\limin\\Desktop\\androidSdkJson\\sdk%d\\noFileError.txt' %apiLevel
    # noFilePath = 'C:\\Users\\limin\\Desktop\\androidSdkJsonClassName\\sdk%d\\noFileError.txt' %apiLevel
    testedListPath = 'C:\\Users\\limin\\Desktop\\androidSdkJsonClassName\\sdk%d.txt' %apiLevel
    
    allhtmlPath = FileUtils.listDirRecur(sdkRefDir)
    testedList = []
    noFileList = []
    FileUtils.mkdir(fileResDictDir)
    print "file no:"
    print len(allhtmlPath)
    for oneHtmlPath in allhtmlPath:
        if 'package-summary.html' not in oneHtmlPath:
            continue
        print 'deal with: %s' %oneHtmlPath
        dirPath = os.path.dirname(oneHtmlPath)
        htmlContent = FileUtils.readFile(oneHtmlPath)

        se = etree.HTML(htmlContent)
        tables = se.xpath('.//table')

        for myTable in tables:
            allClassLinkList = getTableRowsLinks(myTable)
            
            for classLink in allClassLinkList:
                # classPath = os.path.join(dirPath, classLink)
                classPath = dirPath+'/'+classLink
                
                if classLink.startswith('/reference'):
                    classPath = dirPath.split('reference')[0]+'/'+classLink
                # print classPath
                if not os.path.exists(classPath):
                    print 'file not exists error'
                    noFileList.append(classPath)
                    FileUtils.writeList(noFileList, noFilePath)
                    continue
                # classPath='D:\\androidsdkdoc\\docs-23_r01\\docs\\reference\\android\\bluetooth\\BluetoothDevice.html'
                classFullName = main(classPath, fileResDictDir, testedList, apiLevel)
                # input()
                if classFullName:
                    testedList.append(classFullName)
    FileUtils.writeList(testedList,testedListPath)