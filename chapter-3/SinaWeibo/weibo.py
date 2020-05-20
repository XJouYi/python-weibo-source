#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import json
import base64
import re
import time
from .utils import WbUtils

sso_login = 'ssologin.js(v1.4.19)'
# 模拟客户端
user_agent = (
    'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.11 (KHTML, like Gecko) '
    'Chrome/20.0.1132.57 Safari/536.11'
)


class WeiBo(object):
    # 账号
    account = ""
    # 密码
    password = ""
    # 会话
    session = None
    # 用户ID
    uid = ''

    def __init__(self, account, password):
        self.account = account
        self.password = password
        # 建立新的会话
        self.session = requests.session()
        # 设置请求头
        self.session.headers = {
            "User-Agent": user_agent
        }

    def login(self):
        # PreLogin
        resp = self.session.get(
            'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=%s&rsakt=mod&checkpin=1&client=%s' %
            (base64.b64encode(self.account.encode('utf-8')), sso_login)
        )
        pre_login = json.loads(re.match(r'[^{]+({.+?})', resp.text).group(1))
        # Login
        resp = self.session.post('https://login.sina.com.cn/sso/login.php?client=%s' %
                                 sso_login, data=WbUtils.getLoginStructure(self.account, self.password, pre_login)
                                 )
        # CrossDomain

        crossdomain2 = re.search('(https://[^;]*)', resp.text).group(1)
        resp = self.session.get(crossdomain2)
        # Passport
        passporturl = re.search("(https://passport[^\"]*)", resp.text.replace('\/', '/')).group(0)
        resp = self.session.get(passporturl)
        # 获取登录信息
        login_info = json.loads(re.search('\((\{.*\})\)', resp.text).group(1))
        self.uid = login_info["userinfo"]["uniqueid"]
        print(self.uid)

    def sendText(self, content):
        curr_time = "%d" % (time.time() * 1000)
        self.session.headers["Host"] = "weibo.com"
        self.session.headers["Origin"] = "https://weibo.com"
        referer = "https://www.weibo.com/u/%s/home?wvr=5" % self.uid
        self.session.headers["Referer"] = referer
        resp = self.session.post(
            'https://weibo.com/aj/mblog/add?ajwvr=6&__rnd=%s' % curr_time, data=WbUtils.getTextStructure(content)
        )
        try:
            json_object = json.loads(resp.content)
            if json_object['code'] == '100000':
                print("消息发送成功:%s" % content)
            else:
                print("消息发送失败:%s" % json_object['msg'])
        except Exception as e:
            print("消息发送失败:%s" % content)
            raise e

