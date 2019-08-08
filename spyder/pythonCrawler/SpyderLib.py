#coding=utf8
import urllib.request
import urllib.parse
import urllib.error
import os
import sys
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

from modules import FileUtils

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
    post_url = 'http://www.kfc.com.cn/kfccda/ashx/GetStoreList.ashx?op=cname'
    form_data = {
        'cname': '深圳',
        'pid': '',
        'pageIndex': '2',
        'pageSize': '10',
    }
    spyder = MySpyder(post_url)
    response = spyder.requestByPost(form_data)
    #返回的是json格式的结果
    spyder.writeHtml(response, 'testingKfc.json')
    

    








