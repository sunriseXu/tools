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
from modules import CollectionUtils,RexUtils, InteractUtils

def getAllTextByTag(ehtml,xRef):
    h = ehtml.xpath(xRef)
    allDesc = []
    for hi in h:
        text = hi.xpath('string(.)').strip()
        print text
        allDesc.append(text)
    allDesc = ''.join(allDesc)
    allDesc = ' '.join(allDesc.split())
    textWithHref = []
    hrefs = ehtml.xpath('.//a')
    for href in hrefs:
        link = href.xpath('@href')[0]
        subtext = href.xpath('text()')[0]
        textWithHref.append((subtext,subtext+'(href="'+link+'")'))
    print textWithHref

    for subtext,href in textWithHref:
        allDesc = allDesc.replace(subtext,href)

    return allDesc

content = FileUtils.readFile('test.html')
# print(content)
ec = etree.HTML(content)

text = getAllTextByTag(ec,'.//p')
print(text)

