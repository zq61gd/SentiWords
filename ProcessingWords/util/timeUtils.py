# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@Time    : 2018/12/20 11:03
@Author  : suojijun1994@gmail.com
@Site    : 
@File    : timeUtils.py
@Software: PyCharm
'''
import time

def current_time():
    return time.strftime('%Y%m%d_%H%M%S', time.localtime())