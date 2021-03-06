# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os
import json
import sys
from lxml import etree
import requests
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from modules.FileUtils import writeFile


def getUrlContent(url):
    request = urllib2.Request(url)
    request.add_header('User-Agent','Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US; rv:1.9.1.6) Gecko/20091201 Firefox/3.5.6')
    content = ''
    try:
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
    except:
        content = ''
    return content

def getUrlTextEtree(url):
	content = getUrlContent(url)
	# writeFile('C:\\Users\\limin\\Desktop\\today\\test.html',content.encode('utf-8'))
	res = ''
	if content:
		return etree.HTML(content)
	return res

# 前台开启浏览器模式
def openChrome():
	# 加启动配置
	option = webdriver.ChromeOptions()
	option.add_argument('disable-infobars')
	# 打开chrome浏览器
	driver = webdriver.Chrome(chrome_options=option)
	return driver

# 授权操作
def operationAuth(driver):
	url = "http://wlrz.fudan.edu.cn/srun_portal_pc.php?ac_id=1&url=http://www.msftconnecttest.com/redirect&phone=1"
	driver.get(url)
	# 找到输入框并输入查询内容
	elem = driver.find_element_by_id("loginname")
	elem.send_keys("18212010044")

	elem = driver.find_element_by_id("password")
	elem.send_keys("xcz1995818123")
	# 提交表单
	driver.find_element_by_id("button").click()

def main():
    # 加启动配置
	driver = openChrome()
	operationAuth(driver)