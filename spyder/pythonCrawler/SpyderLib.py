#coding=utf8
import os
import sys
import time
import urllib.error
import urllib.parse
import urllib.request

from bs4 import BeautifulSoup

pwd = os.path.dirname(os.path.realpath(__file__))
pwd = os.path.dirname(pwd)
ppwd = os.path.dirname(pwd)
sys.path.append(ppwd)
class MySpyder:
    def __init__(self, *args, **kwargs):
        self.url = args[0]
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36",
        }
        #Request对象，包含请求的完整url，参数，头部等信息，建议将所以url都封装成request对象，加上头部，统一标准
        self.request = urllib.request.Request(self.url,headers=self.headers)


    def requestByGet(self):
        try:
            # response is a handle, after reading, the handle will close automatically，接受url字符串或者Request对象
            response = urllib.request.urlopen(url=self.request)
        except urllib.error.URLError as e:
            print(e)
            return ''
        return response

    def requestByPost(self, postDict):
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

if __name__ == "__main__":
    url = 'http://www.baidu.com'
    # spyder = MySpyder(url)
    # retCode = spyder.getUrl()
    # print(retCode)
    # myPath = 'testingBaidu.html'
    # spyder.writeHtml(myPath)
    # spyder.updateResponseByUrl()

    # myPath = 'testingBaidu.txt'
    # spyder.writeBinary(myPath)
    # picPath = 'testingPic.jpg'
    # picUrl = 'http://s16.sinaimg.cn/orignal/003uYUOmzy7nd6dTtCfcf'
    # downloadFile(picUrl,picPath)

    # url = 'http://www.baidu/index.html?name=钢铁侠&pwd=123456'
    # print('origin url:')
    # print(url)
    # print('quote url:')
    # ret = parseUrl(url)
    # print(ret)
    # print('unquote url:')
    # print(parseUrl(ret, 'unquote'))

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

    ipList = scrawlXiciIp(1)
    ipInfo = ipTest()














