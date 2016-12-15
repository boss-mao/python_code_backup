#  -*- coding: utf-8 -*-
import cookielib
import gzip
import json
import random
import urllib
import urllib2
import StringIO
import time

def parseGizpBody(response):
    data = response.read()
    headers = response.info()
    if ('Content-Encoding' in headers and headers['Content-Encoding'])\
            or ('content-encoding' in headers and headers['content-encoding']):
        try:
            gz = gzip.GzipFile(fileobj=StringIO.StringIO(data))
            return gz.read()
        finally:
            gz.close()
    else:
        return data
pass


def sendVote():
    publicHeaders = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate, sdch",
        "Accept-Language": "zh-CN,zh;q=0.8",
        "Cache-Control": "max-age=0",
        "Host": "www.xiniugushi.com",
        "Origin": "http://www.xiniugushi.com",
        "User-Agent": 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        "X-Requested-With": "XMLHttpRequest"
    }
    cookieJar = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookieJar))
    urllib2.install_opener(opener)

    username = ''.join([random.choice('0123456789abcdegf') for i in range(11)]) + "@" + random.choice(["qq", "hotmail", "163"]) + ".com"
    password =  "".join([random.choice('AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz012345678') for i in range(11)])
    requestData = urllib.urlencode({"account": username, "passwd": password, "accounttype": 1})
    headers = publicHeaders.copy()
    headers["Referer"] = "http://www.xiniugushi.com/register.html",

    request = urllib2.Request(url="http://www.xiniugushi.com/function/account.inc.php?action=register",
                              headers=headers,
                              data=requestData)

    response = opener.open(request)
    response_data = parseGizpBody(response)
    json_data = json.loads(response_data)
    time.sleep(random.randint(1, 2))
    if (json_data.get("success") == 1):
        print u"注册成功"
        headers = publicHeaders.copy()
        headers[
            "Referer"] = "http://www.xiniugushi.com/read/read.html?CZZg0oMONHFt2Qohdgqo=&from=groupmessage&isappinstalled=0"
        voteRequest = urllib2.Request(url="http://www.xiniugushi.com/function/story.inc.php?action=voting",
                                      headers=headers,
                                      data=urllib.urlencode({"storyid": 273438}))

        voteResponse = opener.open(voteRequest)
        vote_data = parseGizpBody(voteResponse)
        vote_json_data = json.loads(vote_data)
        if (vote_json_data.get("success") == 1):
            print "voete成功"
        else:
            print "vote失败:" + vote_json_data
    else:
        print u"注册失败:" + json_data.get("message")

    time.sleep(random.randint(1, 2))

if __name__ == '__main__':
    counter=0
    for index in range(1,20):
        counter=counter+1
        print counter
        sendVote()



