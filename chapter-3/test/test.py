#!/usr/bin/python
# -*- coding: utf-8 -*-
# 测试脚本

from SinaWeibo import WeiBo

if __name__ == '__main__':
    we = WeiBo('account', 'password')
    we.login()
    we.sendText("测试1")
