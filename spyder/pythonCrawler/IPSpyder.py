import urllib
import urllib.request
import urllib.parse
import time
from bs4 import BeautifulSoup

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
            print(content)
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


if __name__ == '__main__':
    #无法爬取这个网站的
    url = 'https://free-proxy-list.net/'
    # url = 'http://www.baidu.com'
    url ='http://www.gatherproxy.com/'
    url = 'http://www.goubanjia.com/'
    url = 'http://www.gatherproxy.com/'
    url = 'https://www.xicidaili.com/wt/'

    ipList = scrawlXiciIp(2)
    print(len(ipList))
    ipVerify = 'http://httpbin.org/get'

    ipTest(ipVerify, ipList)

