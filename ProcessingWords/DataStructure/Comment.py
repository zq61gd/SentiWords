# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@Time    : 2018/12/17 15:03
@Author  : suojijun1994@gmail.com
@Site    : 
@File    : Comment.py
@Software: PyCharm
'''
from OriComm import OriComm


class Comment(OriComm):

    def __init__(self):
        self.forum_com_content_ori_time = None
        self.forum_com_content_ori_ID = ''
        self.forum_com_content_ori_content = ''
        self.forum_com_real_content = ''
        self.replies = []
        # 分词后的字段
        self.cut_ori_comment = ''
        self.cut_real_comment = ''

