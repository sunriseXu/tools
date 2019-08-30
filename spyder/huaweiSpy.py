#coding=utf-8
import urllib
import urllib.request
import io
import os
from lxml import etree
import re
import threading
import sys
from datetime import datetime,timedelta


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
# currTime=datetime.now()
debug = False
testAmount=10
pwd = os.path.dirname(os.path.realpath(__file__))
yesterday = datetime.today() + timedelta(-1)

currTime = yesterday.strftime('%Y-%m-%d')

resPath = 'huawei-%s.csv' %currTime
resPath = os.path.join(pwd,resPath)
with io.open(resPath,'w') as f:
    f.write("{},{},{},{},{},{},{},{},{},{},{},{},{}\n".format('应用代码','应用名称','应用类型','公司名称','app大小','版本号','更新时间','评分','下载人数','应用介绍','图标','下载地址','爬取时间'))
    f.flush()
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
            # for i in range(1,40):
                #/html/body/div[1]/div[4]/div[1]/div[2]/div[2]/div[2]/div[2]/h4/a
                #/html/body/div[1]/div[4]/div[1]/div[2]/div[2]/div[3]/div[2]/h4/a
            xpathReg = './/div/h4/a/@href'
            href=s.xpath(xpathReg)
            # if len(href)>0:
            #     href_list.append(href[0])
            print('href_list size:')
            print(len(href))
            href_list = href
            for nhref in href_list:
                url2="http://appstore.huawei.com"+nhref
                print('open url:'+url2)
                try:
                    data2 = opener.open(url2).read()
                except:
                    continue
                s2=etree.HTML(data2)
                # print('open url success')
                try:
                    # print('get apk info:')
                    #//*[@id="bodyonline"]/div/div[4]/div[1]/div/div/div[1]/ul[1]/li[2]/p[1]/span[1]
                    name=s2.xpath('.//div/div/div/ul/li/p/span/text()')[0]
                    print('name:'+name)
                    #//*[@id="bodyonline"]/div/div[4]/div[1]/div/div/div[1]/ul[2]/li[1]/span
                    size=s2.xpath('.//div/div/div/ul/li/span/text()')[0]
                    print('size:'+size)
                    #//*[@id="bodyonline"]/div/div[4]/div[1]/div/div/div[1]/ul[2]/li[2]/span
                    updataTime=s2.xpath('.//div/div/div/ul/li/span/text()')[1]
                    print('uptime:'+updataTime)
                    #//*[@id="bodyonline"]/div/div[4]/div[1]/div/div/div[1]/ul[2]/li[3]/span
                    company=s2.xpath('.//div/div/div/ul/li/span[@title]/@title')[0]
                    print('company:'+company)
                    #//*[@id="bodyonline"]/div/div[4]/div[1]/div/div/div[1]/ul[2]/li[4]/span
                    version=s2.xpath('.//div/div/div/ul/li/span/text()')[3]
                    print('version:'+version)
                    #//*[@id="bodyonline"]/div/div[4]/div[1]/div/div/div[1]/ul[1]/li[2]/p[1]/span[2]
                    downloadNum=s2.xpath('.//div/div/div/ul/li/p/span/text()')[1]
                    strNum=downloadNum.lstrip('下载：')
                    print('downloadNum:' + strNum)
                    #//*[@id="bodyonline"]/div/div[4]/div[1]/div/div/div[1]/ul[1]/li[2]/p[2]/span
                    #//*[@id="bodyonline"]/div/div[4]/div[1]/div/div/div[1]/ul[1]/li[2]/p[2]/span
                    ranking = s2.xpath('.//div/div/div/ul/li/p/span[@class]/@class')[2]
                    print('ranking:'+ranking)
                    introduct=s2.xpath('//*[@id="app_strdesc"]/text()')[0]
                    print('introduct:'+introduct)
                    # csv是用英文逗号来区分一列的，所以如果应用介绍中有英文逗号需要替换成空格，要不然应用介绍会分成好几列
                    if ',' in introduct:
                        introduct=introduct.replace(',','  ')
                    updataTime=updataTime.strip()#去掉字符串前后空格
                
                    if updataTime not in currTime and not debug:
                        print('not today')
                        continue
                    company=company.strip()#去掉字符串前后空格
                    version=version.strip()#去掉字符串前后空格
                    strNum=strNum.strip()#去掉字符串前后空格
                    introduct=introduct.split()[0].strip()#去掉字符串前后空格
                    # print(introduct)
                    #//*[@id="bodyonline"]/div/div[4]/div[1]/div/div/div[1]/ul[1]/li[1]/img
                    picture=s2.xpath('.//div/div/div/ul/li/img/@src')[0]
                    print('picture url:'+picture)
                    #//*[@id="bodyonline"]/div/div[4]/div[1]/div/div/div[2]/a
                    infor=s2.xpath('.//div/div/div/div/div/div/a/@onclick')[0]

                    allInfor=re.findall(r"['](.*?)[']",infor)#取出下载地址
                    appCode = allInfor[0]                                                     
                    appType = allInfor[4]
                    downaddr = allInfor[5]
                    print('downloadUrl:'+downaddr)

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
                    f.flush()
                    if debug and len(testedList)>testAmount:
                        sys.exit(0)


                except IndexError as e:#出现异常跳出，防止程序崩溃
                    print('indexerror')
                    print(e)
                    pass
            # print("{},{}".format(dev,page))

