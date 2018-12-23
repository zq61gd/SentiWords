# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@Time    : 2018/12/17 15:20
@Author  : suojijun1994@gmail.com
@Site    : 
@File    : OriComm.py
@Software: PyCharm
'''


class OriComm(object):

    def __init__(self):
        self.forum_com_order = -1
        self.forum_com_user = ''
        self.forum_com_time = None
        self.forum_com_content = ''
        self.forum_com_repo_num = -1
        # 分词后的字段
        self.cut_comment = ''
