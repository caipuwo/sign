#!/usr/bin/python
# -*- coding: utf-8 -*-
# @time  2018-08-17
import requests
from bs4 import BeautifulSoup
import sys,json
import re
from user import *

class sign:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0',
                        'Host': 'www.sucaihuo.com',
                        }
        self.session = requests.session()

    def login(self):
        data={}
        data['username'] = self.username
        data['pwd'] = self.password
        loginURL = 'http://www.sucaihuo.com/Login/check'
        try:
            req = self.session.post(loginURL, data=data, headers=self.headers,verify=False)
            return req.json()['error']
        except :
            print ('登录失败')
            sys.exit()

    def checkin(self):
        signURL = 'http://www.sucaihuo.com/Member/sign.html'
        self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:41.0) Gecko/20100101 Firefox/41.0',
                        'Host': 'www.sucaihuo.com','Referer':'http://www.sucaihuo.com/',
                        }
        checkinREQ = self.session.get(signURL, headers=self.headers,verify=False)
        matchObj = re.search( r'data-key="(.*?)"', checkinREQ.text, re.M|re.I)
        data={}
        data['key']=matchObj.group(1)
        print (data['key'])
        signURLS='http://www.sucaihuo.com/Member/signDay'
        checkinREQ2 = self.session.post(signURLS,data=data ,headers=self.headers,verify=False)
                        
        print (checkinREQ2.text)
        return checkinREQ2.text

    def start(self):
        loginData = self.login()
        if loginData != '':
            print ('登陆失败')
            print (loginData)
            sys.exit()
        checkinData = self.checkin()
        if checkinData=='-1':
            print ('已签到或签到失败，请检查')
        else:
            print ('签到成功')

if __name__ == "__main__":
    sucaihuoLogin = sign(sucaihuo_user, sucaihuo_pass)
    sucaihuoLogin.start()
