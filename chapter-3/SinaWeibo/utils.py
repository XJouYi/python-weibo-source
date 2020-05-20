#!/usr/bin/python
# -*- coding: utf-8 -*-
import binascii
import rsa
import base64
import requests
import json

class WbUtils(object):
    # RSA加密
    @staticmethod
    def encrypt_passwd(passwd, pubkey, servertime, nonce):
        key = rsa.PublicKey(int(pubkey, 16), int('10001', 16))
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(passwd)
        passwd = rsa.encrypt(message.encode('utf-8'), key)
        return binascii.b2a_hex(passwd)

    # 登录参数
    @staticmethod
    def getLoginStructure(account, password, pre_login):
        data = {
            'entry': 'weibo',
            'gateway': 1,
            'from': '',
            'savestate': 7,
            'userticket': 1,
            'ssosimplelogin': 1,
            'su': base64.b64encode(requests.utils.quote(account).encode('utf-8')),
            'service': 'miniblog',
            'servertime': pre_login['servertime'],
            'nonce': pre_login['nonce'],
            'vsnf': 1,
            'vsnval': '',
            'pwencode': 'rsa2',
            'sp': WbUtils.encrypt_passwd(password, pre_login['pubkey'], pre_login['servertime'], pre_login['nonce']),
            'rsakv': pre_login['rsakv'],
            'encoding': 'UTF-8',
            'prelt': '53',
            'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.si' 'naSSOController.feedBackUrlCallBack',
            'returntype': 'META'
        }
        return data

    @staticmethod
    def getTextStructure(message):
        data = {
            'location': 'v6_content_home',
            'text': message,
            'appkey': '',
            'style_type': 1,
            'pic_id': '',
            'pdetail': '',
            'rank': 0,
            'rankid': '',
            'module': 'stissue',
            'pub_source': 'main_',
            'pub_type': 'dialog',
            'isPri': 0,
            '_t': 0
        }
        return data

    @staticmethod
    def checkResultMessage(resultJson):
        flag = False
        json_object = json.loads(resultJson)
        try:
            code = json_object['code']
            msg = json_object['msg']
            data = json_object['data']
            if code == '100000':
                flag = True
            return flag, msg, data
        except Exception as e:
            raise e
