#!/usr/bin/python
# -*- coding: utf-8 -*-
# @time  2018-08-17
import urllib
import http.cookiejar
import sys
import json
import re
from user import *
 
 
class MyHTTPRedirectHandler(urllib.request.HTTPRedirectHandler):
    def http_error_302(self, req, fp, code, msg, headers):
        return 300
        #return urllib.request.HTTPRedirectHandler.http_error_302(self, req, fp, code, msg, headers)
    http_error_301 = http_error_303 = http_error_307 = http_error_302


class sign:
    def __init__(self, username, password):
        self.cookie = http.cookiejar.MozillaCookieJar()  # 构造一个CookieJar对象
        self.cookieUrl='sucaihuo_cookie.txt'
        self.postdata = urllib.parse.urlencode({
            'username':username,
            'pwd':password
            }).encode('utf-8')
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0',
                        'Host': 'www.sucaihuo.com',
                        }
        self.getCookie()

    def getCookie(self):
        try:
            self.cookie.load(self.cookieUrl, ignore_discard=True, ignore_expires=True)  # 加载cookie
        except Exception as err:
            self.login()
            self.cookie.load(self.cookieUrl, ignore_discard=True, ignore_expires=True)  # 加载cookie

    def login(self):
        self.cookie = http.cookiejar.MozillaCookieJar(self.cookieUrl)
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie))
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0')]
        opener.addheaders = [('Host','www.sucaihuo.com')]
        loginURL = 'http://www.sucaihuo.com/Login/check'
        result = opener.open(loginURL,self.postdata).read()
        error = json.loads(result)['error']
        if error != '':
            print('登录失败')
            print(error)
            sys.exit()
        self.cookie.save(ignore_discard=True,ignore_expires=True)

    def checkin(self):
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie),MyHTTPRedirectHandler)
        signURL = 'http://www.sucaihuo.com/Member/sign.html'
        opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0')]
        opener.addheaders = [('Host','www.sucaihuo.com')]
        req = urllib.request.Request(signURL)
        response = opener.open(req)
        if response==300:
            self.login()
            opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(self.cookie),MyHTTPRedirectHandler)
            signURL = 'http://www.sucaihuo.com/Member/sign.html'
            opener.addheaders = [('User-Agent','Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0')]
            opener.addheaders = [('Host','www.sucaihuo.com')]
            req = urllib.request.Request(signURL)
            response = opener.open(req)
        da=response.read().decode()
        matchObj = re.search( r'data-key="(.*?)"',da, re.M|re.I)
        key=matchObj.group(1)
        data=urllib.parse.urlencode({
            'key':key
        }).encode('utf-8')
        signURLS = 'http://www.sucaihuo.com/Member/signDay'
        req = urllib.request.Request(signURLS)
        response = opener.open(req,data).read()
        return response.decode('utf-8')

        
if __name__ == "__main__":
    sucaihuoLogin = sign(sucaihuo_user, sucaihuo_pass)
    checkinData=sucaihuoLogin.checkin()
    if checkinData=='-1':
        print ('已签到或签到失败，请检查')
    else:
        print ('签到成功')
