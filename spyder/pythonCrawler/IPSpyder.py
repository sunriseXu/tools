import urllib
import urllib.request
import urllib.parse


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

if __name__ == '__main__':
    #无法爬取这个网站的
    url = 'https://free-proxy-list.net/'
    # url = 'http://www.baidu.com'
    url ='http://www.gatherproxy.com/'
    url = 'http://www.goubanjia.com/'
    url = 'https://www.xicidaili.com/wt/'
    IPSpy = MySpyder(url)
    response = IPSpy.requestByGet()
    content = response.read().decode()
    # print(content)
