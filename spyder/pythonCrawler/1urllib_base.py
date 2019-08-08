"""
code by python 3.7.2
utf-8
caixiaoxin
index: 1
"""


"""
urllib.request:
    urlopen:打开url
    urlretrieve(url,file_name)：打开并保存url内容
urllib.parse:
    quote(): url编码函数，将中文进行转化为%xxx
    unquote()：url解码函数，将%xxx转化为指定字符
    urlencode()：非法字符转码
response:
    read()  读取字节类型
    geturl()    获取请求url
    getheaders()
    getcode()
    readlines()
"""
"""
字符串->二进制：encode()
二进制->字符串：decode()
默认utf8
"""




import urllib.request
url = 'http://www.baidu.com/'
response = urllib.request.urlopen(url=url)
"""
print(response)
print(response.geturl())
print(response.getheaders())
print(response.getcode())
"""
# print(response.read().decode())
# 读取的url内容存储
with open('baidu.html','w',encoding='utf8') as file:
    file.write(response.read().decode())
"""
等同上方
只不过上述用utf8写入
在此用二进制写入
图片用这个！
with open('baidu_1.html','wb') as flie:
    file.write(response.read())
"""






# urlretrieve(url,file_name)
picurl = "https://timgsa.baidu.com/timg?image&quality=80&" \
         "size=b9999_10000&sec=1551421909555&di=9f9d69abb9fe596f493f9c6e3e52f08e&imgtype=0&" \
         "src=http%3A%2F%2Fgss0.baidu.com%2F9vo3dSag _xI4khGko9WTAnF6hhy%2Fzhidao%2Fpic%2Fitem%" \
         "2Fb151f8198618367a039b78422c738bd4b31ce51b.jpg"

"""
# 创建写入文件一条龙服务
# urllib.request.urlretrieve(picurl,'ironMan.jpg')
"""







import urllib.parse

# url中若出现 $ 空格 中文等，就要对其进行编码
url = 'http://www.baidu/index.html?name=钢铁侠&pwd=123456'
ret = urllib.parse.quote(url)
re = urllib.parse.unquote(url)
re_1 = urllib.parse.unquote(picurl)
print(ret)
print(re)
print(re_1)

"""
urllib.parse.urlencode 的应用！
"""
url = 'http://www.baidu.com/index.html'
# 构造 http://www.baidu.co/index.html?name=goudan&age=18&sex=nv&height=180
name = '钢铁侠'
age = 18
sex = 'nv'
height = "180"

data = {
    'name' : name,
    'age' : age,
    'sex' : sex,
    'height' : height,
    'weight' : 180,
}
# 具有非法字符的自动转换功能
construct_url = urllib.parse.urlencode(data)
print(construct_url)
construct_url = url + '?' + construct_url
print(construct_url)

# example：植入搜索关键字
import urllib.parse
baidu = 'http://www.baidu.com/s?'
word = input('input the key you want:')
_data = {
    'ie' : 'utf-8',
    'wd' : word,
}
# 非法字符转码
query_string = urllib.parse.urlencode(_data)
baidu += query_string
response = urllib.request.urlopen(baidu)
filename = word + '.html'
with open(filename,'wb') as file:
    file.write(response.read())







# 伪装UA
# 构建请求对象:urllib.request.Request(self,url,data=None,headers={},...)
url = 'http://www.baidu.com/'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
}
request = urllib.request.Request(url = url, headers=headers)

response = urllib.request.urlopen(request)
