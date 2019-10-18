#coding=utf8
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import logging
from lxml import etree
import uuid
from bs4 import BeautifulSoup

pwd = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.dirname(pwd)
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)

logging.basicConfig(level=logging.DEBUG)
l = logging.getLogger("spyderlib")
class MySpyder:
    def __init__(self, *args, **kwargs):
        self.url = args[0]
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cache-Control': 'max-age=0',
            'Connection': 'keep-alive',
            # 'Host': 'duanziwang.com',
            'Upgrade-Insecure-Requests': 1,
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
        }
        #Request对象，包含请求的完整url，参数，头部等信息，建议将所以url都封装成request对象，加上头部，统一标准
        self.request = urllib.request.Request(self.url,headers=self.headers)

    def createHandlerOpener(self,type='http',proxies={}):
        '''
        handle现在的作用是构造请求的ip,代理,cookie等信息,cookie还没加入
        :param type:
        :param proxies:
        :return:
        '''
        self.opener = None
        self.handler = None
        if type in 'http':
            self.handler = urllib.request.HTTPHandler()
        elif type in 'proxy':
            self.handler = urllib.request.ProxyHandler(proxies)
        self.opener = urllib.request.build_opener(handler)
        return self.opener

    def requestByGet(self, opener=False):
        try:
            if opener:
            # response is a handle, after reading, the handle will close automatically，接受url字符串或者Request对象
                response = self.opener.open(self.request)
            else:
                response = urllib.request.urlopen(url=self.request)
        except urllib.error.URLError as e:
            print(e)
            return ''
        return response

    def requestByPost(self, postDict, opener=False):
        try:
            postBytes = urllib.parse.urlencode(postDict).encode()
            response = urllib.request.urlopen(url=self.request, data=postBytes)
        except urllib.error.URLError as e:
            print(e)
            return ''
        return response

    def getUrl(self):
        return self.response.geturl()
    def getHeaders(self):
        return self.response.getheaders()
    def getCode(self):
        # return code, like 404 or something
        return self.response.getcode()
    def getUrlContentBinary(self):
        return self.response.read()
    def getUrlContentUTF8(self):
        '''
        read() return the bin stream
        decode() transfer the bin to string
        default coding type: utf-8
        '''
        retContent = self.response.read().decode()
        return retContent
    def writeHtml(self,response,myPath):
        with open(myPath,'w',encoding='utf8') as f:
            f.write(response.read().decode())
    def writeBinary(self, response ,myPath):
        # 也能够写字符串
        with open(myPath,'wb') as f:
            res = response.read()
            if not res:
                print('no content to be written')
            else:
                f.write(res)



def downloadFile(url, fileName):
    urllib.request.urlretrieve(url,fileName)


def parseUrl(url,type='quote'):
    '''
    解析与反解析url中的非法字符串，如中文，%，空格，斜杠等
    '''
    if type in 'quote':
        return urllib.parse.quote(url)
    elif type in 'unquote':
        return urllib.parse.unquote(url)
def genUrlParam(myDict):
    '''
    根据字典构造url参数，即?后的查询参数
    中文，空格等自动转码
    '''
    return urllib.parse.urlencode(myDict)
def ipTest(urlForTest, ipList):
    '''
    测试爬取得ip是否合法
    :param urlForTest:
    :param ipInfo:
    :return:
    '''
    for i in range(1, len(ipList)+1):
        print('******%d*******' %i)
        ipInfo = ipList[i]
        proxies = {
            'http':'http://'+ipInfo,
            'https':'https://'+ipInfo,
        }
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",

        }
        handler = urllib.request.ProxyHandler(proxies)
        opener = urllib.request.build_opener(handler)
        request = urllib.request.Request(urlForTest, headers=headers)
        try:
            response=opener.open(request,timeout=1)
            content = response.read().decode()
            return ipInfo
        except Exception as e:
            print(e)
            print('timeout')
            pass
def scrawlXiciIp(num, xiciUrl='https://www.xicidaili.com/wt/'):
    '''
    爬去xici网的代理ip列表
    :param num:
    :param xiciUrl:
    :return:
    '''
    ipList = []
    for i in range(1,num+1):

        url = xiciUrl + str(i)
        IPSpy = MySpyder(url)
        response = IPSpy.requestByGet()
        resultCode = response.getcode()
        if resultCode != 200:
            continue
        content = response.read().decode()
        soup = BeautifulSoup(content, 'lxml')
        trs = soup.find_all('tr')

        for i in range(1, len(trs)):
            tr = trs[i]
            tds = tr.find_all('td')
            ip_item = tds[1].text + ':' + tds[2].text
            ipList.append(ip_item)
        time.sleep(5)
    ipList = list(set(ipList))
    return ipList
def html2Xpath(srcPath=None):
    if not os.path.exists(srcPath):
        l.warning("srcPath does not exist!")
        return None
    parser = etree.HTMLParser(encoding="utf-8")
    tree = etree.parse(srcPath, parser=parser)
    return tree

def getAllLink(element=None, rex=None):
    if not element:
        l.warning("element is none!")
        return None
    links = element.xpath("//@href")
    return links


if __name__ == "__main__":

    htmlPath = '/home/limin/Desktop/afs_cs_academic_class_15745-s16_www_lectures.html'
    le = html2Xpath(htmlPath)
    #/html/body/pre/a[22]
    # / html / body / pre / a[1]
    # /html/body/table/tbody/tr[5]/td[2]/a
    # /html/body/table/tbody/tr[4]/td[2]/a
    # /html/body/table/tbody/tr[6]/td[2]/a
    xp = '/html/body/table/tbody/tr/td/a/@href'
    links = le.xpath(xp)
    links = [i for i in links if '.pdf' in i]
    print(links)
    # baselink = 'https://www.cs.cmu.edu/afs/cs/academic/class/15745-s12/public/lectures/'
    baselink = ''
    baseDir = '/home/limin/Documents/jianguoyun/Nutstore/papers/cmu-llvm-compiler-pdf-2'
    # os.makedirs(baseDir)
    for link in links:
        fileName = os.path.basename(link)
        fLink = baselink + link
        dst = os.path.join(baseDir,fileName)
        l.debug('src: {}\ndst: {}'.format(fLink,dst))
        downloadFile(fLink, dst)
        l.debug('download {} done!'.format(fLink))

    url = 'http://www.baidu.com'

    # myDict = {
    #     'name':'xcz',
    #     'age':18,
    #     'sex':'male',
    #     'Chinese':'//许朝智'

    # }
    # print('generate url param:')
    # print(genUrlParam(myDict))


    # post_url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
    # form_data = {
    #     'cname': '深圳',
    #     'pid': '',
    #     'pageIndex': '2',
    #     'pageSize': '10',
    # }
    # spyder = MySpyder()
    # response = spyder.requestByPost(form_data)
    # #返回的是json格式的结果
    # try:
    #     spyder.writeHtml(response, 'testingKfc.json')
    # finally:
    #     pass


    # 高级请求手段 handle来更加个性化制定请求行为
    # 通常是通过
    # urllib.request.urlopen来打开请求报文
    # 但是可以通过
    # urllib.request.build_opener().open(request)来打开报文
    #handle生成,httpHandle ProxyHandle生成普通handle和代理handle
    handler = urllib.request.HTTPHandler()
    #通过如下方法构造匿名ip,可以从西刺网爬取可用的ip,现在就不爬了,但是可以爬一下,网上有教程,爬一下吧,也可以将结果存入数据库,找到一个很好的博客,多练
    #西刺网 https://www.xicidaili.com/nn/
    #国外: https://free-proxy-list.net/ 质量更高
    #https://stackoverflow.com/questions/48426624/scraping-free-proxy-listing-website
    #https://forum.agenty.com/t/how-to-scrape-free-proxy-list-from-internet/19

    # handler = urllib.request.ProxyHandler({'http':'203.77.239.18:37002'})
    # opener = urllib.request.build_opener(handler)
    #
    # url = 'http://ip111.cn/'
    # #http://httpbin.org/get 更好
    # headers = {
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    # }
    # spyder = MySpyder(url)
    # request = urllib.request.Request(url,headers=headers)
    # response = opener.open(request)
    # spyder.writeHtml(response,'testingIp.html')

    # ipList = scrawlXiciIp(1)
    # ipInfo = ipTest('http://httpbin.org/get',ipList)
    # print(ipInfo)
    # url = 'https://baidu.com/s?'
    # headers = {
    #     'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
    # }
    # data = {
    #     'ie': 'utf-8',
    #     'wd': 'ip',
    # }
    # proxies = {
    #     'http': 'http://' + ipInfo,
    #     'https': 'https://' + ipInfo,
    # }
    #
    # handler = urllib.request.ProxyHandler(proxies)
    # opener = urllib.request.build_opener(handler)
    # url = url + urllib.parse.urlencode(data)
    # request = urllib.request.Request(url, headers=headers)
    # response = opener.open(request)
    # with open('testingProxy.html','w') as f:
    #     f.write(response.read().decode())


















