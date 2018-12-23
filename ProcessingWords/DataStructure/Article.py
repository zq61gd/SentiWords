# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@Time    : 2018/12/17 15:03
@Author  : suojijun1994@gmail.com
@Site    : 
@File    : Article.py
@Software: PyCharm
'''


class Article(object):
    def __init__(self):
        self.index_0 = -1
        self.forum_type = ''
        self.forum_title = ''
        self.forum_time = None
        self.forum_vol = -1
        self.platform = ''
        self.website = ''
        self.forum_article = ''
        self.forum_com_num = -1
        self.comments = []
        # 分词后的字段
        self.cut_title = ''
        self.cut_article = ''