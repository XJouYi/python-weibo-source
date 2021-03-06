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
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
    'Chrome/79.0.3945.130 Safari/537.36'
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

