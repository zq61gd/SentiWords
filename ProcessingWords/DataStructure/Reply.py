# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@Time    : 2018/12/17 15:04
@Author  : suojijun1994@gmail.com
@Site    : 
@File    : Reply.py
@Software: PyCharm
'''


class Reply(object):

    def __init__(self):
        self.forum_repo_order = -1
        self.forum_com_repo = ''
        self.forum_com_repo_time = None
        self.forum_com_repo_ID = ''
        self.forum_com_re_repo_ID = ''
        self.forum_com_repo_content = ''
        # 分词后的字段
        self.cut_repo_content = ''
        self.cut_real_repo_content = ''
