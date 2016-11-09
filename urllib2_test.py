#  -*- coding: utf-8 -*-
#urlib2使用
import cookielib
import gzip
import json
import urllib
import urllib2
import StringIO


#解析响应报文
def parse_response_body(response):
    #读取响应报文
    data = response.read()
    headers = response.info()
    if ('Content-Encoding' in headers and headers['Content-Encoding']) or ('content-encoding' in headers and headers['content-encoding']):
        try:
            gz = gzip.GzipFile(fileobj=StringIO.StringIO(data))
            return gz.read()
        finally:
            if gz:
                gz.close()
    else:
        return data
pass

#模拟请求报文头
public_request_headers = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, sdch",
    "Accept-Language": "zh-CN,zh;q=0.8",
    "Cache-Control": "max-age=0",
    "Host": "www.xiniugushi.com",
    "Origin": "http://www.xiniugushi.com",
    "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
    "X-Requested-With": "XMLHttpRequest"
}

#安装cookie
cookieJar = cookielib.CookieJar()
opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
urllib2.install_opener(opener)

#发送post请求
headers = public_request_headers.copy()
headers["Referer"] = "",
#随机生成一个Email
email=''.join([random.choice('0123456789abcdegf') for i in range(11)]) + "@" + random.choice(["qq", "hotmail", "163"]) + ".com"
request_data = urllib.urlencode({"email": email, "passwd": "bbbb"})
request = urllib2.Request(url="",
                          headers=headers,
                          data=request_data)
response = opener.open(request)
#打印所有cookie
cookieJar._cookies.values()
data=parse_response_body(response)



###########################################################################
#另一种写法
try:
    mainResponse=urllib2.urlopen(urllib2.Request(url="http://wwww.baidu.com/", headers=public_request_headers))
    print mainResponse.info()
    print cookieJar._cookies.values()
    #urllib2请求错误时会抛出异常 
except urllib2.URLError as e:
    print u'异常了'
else: 
    pass

###########################################################################
#可用这个处理302，当异常抛出
class RedirctHandler(urllib2.HTTPRedirectHandler):
    def http_error_301(self, req, fp, code, msg, headers):
        pass
    def http_error_302(self, req, fp, code, msg, headers):
        pass