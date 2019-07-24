# -*- coding:utf-8 -*-
import urllib
import urllib2
import re
import os
import json
import sys
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time



def getContent(url):
	request = urllib2.Request(url)
	response = urllib2.urlopen(request)
	content = response.read().decode('utf-8')
	return content



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