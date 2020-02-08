#coding=utf-8
from modules import FileUtils
# from modules import CollectionUtils

from modules import RexUtils
from modules import AdbUtils
from modules import ApkUtils
from modules.FileUtils import EasyDir
# from modules import SpyderUtils
from modules import InteractUtils
from modules import ThreadUtils
from rooms import FileRoom
import os
import shutil
import random
import logging
import sys
import time
from datetime import datetime
import argparse 


def genParagraph(content):
    return "<p> {} </p>".format(content)

def genTitle(level, content):
    if level<1 or level > 5:
        return ''
    head = '#'*level
    return '{} {}'.format(head, content)
def genTextBlock(content):
    return '\n> {}'.format(content)

def genPicture(url,desc=''):
    return '\n![{}]({})'.format(desc, url)

def genCenter(content):
    return '<center>{}</center>'.format(content)

def genFont(content, color='black', size=3):
    return '<font color={} size={}>{}</font>'.format(color,size,content)

def genCenterPara(content):
    res = genFont('font test')
    res = genCenter(res)
    res = genParagraph(res)
    return res

class MyTable:
    def __init__(self, lows, cols):
        self.lows = lows
        self.cols = cols
        self.head = []
        self.datas = []
    def setTitle(self, columnNames):
        self.head.extend(columnNames)
    def addRowData(self, row):
        self.datas.append(row)
    def genHead(self):
        content = ""
        sep = ""
        isFirst = True
        for headName in self.head:
            if isFirst:
                content += '|'
                sep += '|'
                isFirst = False
            content += ' {} |'.format(headName)
            sep += ' {} |'.format("----")
        content += '\n'
        content += '{}\n'.format(sep)
        return content
    
    def genRowData(self,row):
        content = ""
        isFirst = True
        for item in row:
            if isFirst:
                content += '|'
                isFirst = False
            content += ' {} |'.format(item)
        content += '\n'
        return content
    def genRows(self):
        content = ""
        for row in self.datas:
            content += self.genRowData(row)
        return content
    def setJump(self, columnIdx):
        if columnIdx<0 or columnIdx>=self.cols:
            return
        for i in range(0, len(self.datas)):
            element = self.datas[i][columnIdx]
            element = "[{}](#{})".format(element,element)
            print(element)
            self.datas[i][columnIdx] = element
        return
    def getMDContent(self):
        content = ''
        if not self.head or not self.datas:
            print("rows are null!")
            return ""
        content += self.genHead()
        content += self.genRows()
        return content

def genOrdListInBlock(myList):
    content = ""
    for i in range(1,len(myList)+1):
        item = myList[i-1]
        content += "> {}. {}\n".format(i,item)
    return content

def genTag(tag, content):
    return "<span id=\"{}\">{}</span>".format(tag,content)

            
if __name__ == "__main__":

    startDate = ""
    endDate = ""
    TraceNum = ""
    FpNum = ""
    imgPath = ""
    sumupList =  ["meiyou","nishi"]
    tableTitle = ["商城代码","名称","日期","预测结果","人工分析"]
    tableData = [['a','b'],['aa','bb']]
    mdList = []
    #标题
    res = genTitle(1,genCenter("每日APK测试报告"))
    mdList.append(res)

    #测试结果
    res = genTitle(2, genParagraph(genFont("测试结果",'#0099ff',5)))
    mdList.append(res)

    #测试结果描述
    content = "日期跨度:{}-{}\nAPP日志总数:{}\nFP数量:{}".format(startDate,endDate,TraceNum,FpNum)
    res = genTextBlock(content)
    mdList.append(res)

    #插入测试图片
    res = genPicture(imgPath,"result")
    mdList.append(res)

    #第二段 误报分析
    res = genTitle(2, genParagraph(genFont("误报分析",'#0099ff',5)))
    mdList.append(res)

    #插入表格

    table = MyTable(5,5)
    table.setTitle(tableTitle)
    for item in tableData:
        table.addRowData(item)
    table.setJump(0)
    res = table.getMDContent()
    mdList.append(res)

    #第三段 总结
    res = genTitle(2, genParagraph(genFont("总 结",'#0099ff',5)))
    mdList.append(res)

    res = genOrdListInBlock(sumupList)
    mdList.append(res)

    #第四段 附录
    res = genTitle(2, genParagraph(genFont("附 录",'#0099ff',5)))
    mdList.append(res)
    
    res = genTag("aa","c1000010")
    mdList.append(res)

    mdContent = "\n".join(mdList)
    print(mdContent)