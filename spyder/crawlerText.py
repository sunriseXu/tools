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

def getAllTextByTag(ehtml,xRef):
    h = ehtml.xpath(xRef)
    allDesc = []
    hrefs = []
    if len(h) == 0:
        return ''
    idx = 0
    for hi in h:
        idx += 1
        text = hi.xpath('string(.)').strip()
        allDesc.append(text)
        hreftmp = hi.xpath('.//a')
        if len(hreftmp)>0:
            hrefs = hrefs+hreftmp
    allDesc = ''.join(allDesc)
    # allDesc = [' '.join(i.split()) for i in allDesc]
    allDesc = ' '.join(allDesc.split())
    print allDesc
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
        subtext = str(' '.join(subtext.split())).strip()
        # print type(subtext)
        if not subtext or '/reference/' not in link:
            continue
        #并且需要判断subtext 和 link为空 不然会爆炸的
        #这里需要生成唯一id，因为如果自己生成，那么$$XCZ-22 也是子串 $$XCZ-2
        textWithHref.append((subtext,link,create_uid()))
    textWithHref = sorted(textWithHref,key = lambda i:len(i[0]),reverse=True)
    print textWithHref
    for subtext,href,myTag in textWithHref:
        print subtext
        print myTag
        print 'replace {} to {}'.format(subtext, myTag)
        allDesc = allDesc.replace(subtext,myTag)

    print allDesc
    for subtext,href,myTag in textWithHref:
        print 'replace {} to {}'.format(myTag, subtext)
        allDesc = allDesc.replace(myTag,'[{}]({})'.format(subtext,href))
    return allDesc

content = FileUtils.readFile('test.html')
# print(content)
ec = etree.HTML(content)

# text = getAllTextByTag(ec,'.//p')
# print text
def getSeeAlso(ec):
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
# print seealso
# print(text)
# seeAlsoList = getSeeAlso(ec)
# print seeAlsoList
classDescX = '//*[@id="jd-content"]/div[1]'
text = getAllTextByTag(ec,classDescX)
print text

