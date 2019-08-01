#coding=utf-8
import urllib
import urllib.request
import io
import os
from lxml import etree
import re
import threading
from datetime import datetime


class MyThread(threading.Thread):
    def __init__(self,func,args=()):
        super(MyThread,self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(*self.args)

    def get_result(self):
        try:
            return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
        except Exception:
            return None

def mkdir(path):
	folder = os.path.exists(path)
	if not folder:
		os.makedirs(path)

def downloadFile(dlink,savePath):
    resFlag = True
    try:
        urllib.request.urlretrieve(dlink, savePath)
    # print('downloaded')
    except:
    #     print('download faile')
        resFlag = False
    return resFlag
currTime=datetime.now()
currTime = currTime.strftime('%Y-%m-%d')
resPath = 'huawei-%s.csv' %currTime
with io.open(resPath,'w') as f:
    f.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format('应用代码','应用名称','应用类型','公司名称','app大小','版本号','更新时间','评分','下载人数','应用介绍','图标','下载地址','爬取时间'))
    
    testedList = []
    # mkdir('./todayApk')

    url = 'https://appstore.huawei.com/soft/list_13_1'
    headers = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
    #直接访问应用市场网址会提示403错误
    #需要模拟浏览器访问，解决403错误
    opener = urllib.request.build_opener()
    opener.addheaders = [headers]
    data = opener.open(url).read()
    s=etree.HTML(data)
    allCategoryList = []
    allCategoryList.append('/soft/list_13')
    for i in range(1,20):
        allCategoryRex = '/html/body/div[1]/div[5]/div[1]/div[1]/p/span[2]/a[%d]/@href' %i
        allCategory = s.xpath(allCategoryRex)
        if len(allCategory)>0:
            allCategoryList.append(allCategory[0]) 
    print(allCategoryList)
    idx = 0
    for dev in allCategoryList:
        idx += 1
        for page in range(1,10):    
            url ="http://appstore.huawei.com{}_1_{}".format(dev,page)
            headers = ("User-Agent","Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36")
            #直接访问应用市场网址会提示403错误
            #需要模拟浏览器访问，解决403错误
            opener = urllib.request.build_opener()
            opener.addheaders = [headers]
            data = opener.open(url).read()
            s=etree.HTML(data)
            print(url)
            href_list = []
            for i in range(1,40):
                xpathReg = '/html/body/div[1]/div[5]/div[1]/div[2]/div[2]/div[%d]/div[2]/h4/a/@href' %i
                href=s.xpath(xpathReg)
                if len(href)>0:
                    href_list.append(href[0])
            print('href_list size:')
            print(len(href_list))
            for nhref in href_list:
                url2="http://appstore.huawei.com"+nhref
                # print('open url:'+url2)
                data2 = opener.open(url2).read()
                s2=etree.HTML(data2)
                # print('open url success')
                try:
                    # print('get apk info:')
                    name=s2.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[1]/ul[1]/li[2]/p[1]/span[1]/text()')[0]
                    size=s2.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[1]/ul[2]/li[1]/span/text()')[0]
                    updataTime=s2.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[1]/ul[2]/li[2]/span/text()')[0]
                    company=s2.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[1]/ul[2]/li[3]/span/@title')[0]
                    version=s2.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[1]/ul[2]/li[4]/span/text()')[0]
                    downloadNum=s2.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[1]/ul[1]/li[2]/p[1]/span[2]/text()')[0]
                    strNum=downloadNum.lstrip('下载：')
                    ranking = s2.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[1]/ul[1]/li[2]/p[2]/span/@class')[0]
                    introduct=s2.xpath('//*[@id="app_strdesc"]/text()')[0]
                    # print(name)
                    # print(updataTime)
                    # csv是用英文逗号来区分一列的，所以如果应用介绍中有英文逗号需要替换成空格，要不然应用介绍会分成好几列
                    if ',' in introduct:
                        introduct=introduct.replace(',','  ')
                    updataTime=updataTime.strip()#去掉字符串前后空格
                
                    if updataTime not in currTime:
                        print('not today')
                        continue
                    company=company.strip()#去掉字符串前后空格
                    version=version.strip()#去掉字符串前后空格
                    strNum=strNum.strip()#去掉字符串前后空格
                    introduct=introduct.split()[0].strip()#去掉字符串前后空格
                    picture=s2.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[1]/ul[1]/li[1]/img/@src')[0]
                    # print(picture)
                    infor=s2.xpath('//*[@id="bodyonline"]/div/div[5]/div[1]/div/div/div[2]/a/@onclick')[0]
                    allInfor=re.findall(r"['](.*?)[']",infor)#取出下载地址
                    appCode = allInfor[0]                                                     
                    appType = allInfor[4]
                    downaddr = allInfor[5]

                    dApkPath = './todayApk/%s.apk' %appCode
                    # downloadFile(downaddr, dApkPath)
                    # t=MyThread(downloadFile,args=(downaddr,dApkPath))
                    # t.start()
                
                    if appCode in testedList:
                        print(appCode+' in list!')
                        continue
                    print(url2)
                    # print('found new apk')
                    testedList.append(appCode)
                    f.write('{},{},{},{},{},{},{},{},{},{},{},{},{}'.format(appCode,name,appType,company,size,version,updataTime,ranking,
                                                                   strNum,introduct,picture,downaddr,currTime))
                    f.write('{}'.format('\n'))

                except IndexError:#出现异常跳出，防止程序崩溃
                    print('indexerror')
                    pass
            # print("{},{}".format(dev,page))

