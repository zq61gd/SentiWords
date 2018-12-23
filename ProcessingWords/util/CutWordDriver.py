# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@Time    : 2018/12/20 15:50
@Author  : suojijun1994@gmail.com
@Site    : 
@File    : CutWordDriver.py
@Software: PyCharm
'''
from builtins import object

import jieba
from FileUtil import PathHelper


class SplitSentence(object):
    def __init__(self, Blogs = []):
        self.blogs = Blogs

    def split_sentences_to_words(self, str):
        return jieba.lcut(str)

    def cut_article(self, article):
        if self.is_legeal_sentence(article.forum_article):
            article.cut_article = \
                self.split_sentences_to_words(article.forum_article)
        if self.is_legeal_sentence(article.forum_title):
            article.cut_title = \
                self.split_sentences_to_words(article.forum_title)
        for comment in article.comments:
            self.cut_comment(comment)

    def cut_comment(self, comment):
        if self.is_legeal_sentence(comment.forum_com_content):
            comment.cut_comment = \
                self.split_sentences_to_words(comment.forum_com_content)
        if self.is_legeal_sentence(comment.forum_com_real_content):
            comment.cut_real_comment = \
                self.split_sentences_to_words(comment.forum_com_real_content)
        if self.is_legeal_sentence(comment.forum_com_content_ori_content):
            comment.cut_ori_comment = \
                self.split_sentences_to_words(comment.forum_com_content_ori_content)
        for reply in comment.replies:
            self.cut_reply(reply)

    def cut_reply(self, reply):
        if self.is_legeal_sentence(reply.forum_com_repo):
            reply.cut_repo_content = \
                self.split_sentences_to_words(reply.forum_com_repo)
        if self.is_legeal_sentence(reply.forum_com_repo_content):
            reply.cut_real_repo_content = \
                self.split_sentences_to_words(reply.cut_real_repo_content)

    def is_legeal_sentence(self, sentence):
        if not sentence:
            return False
        if sentence == "":
            return False
        return True

    def driver(self):
        for blog in self.blogs:
            self.cut_article(blog)

    def run(self):
        self.driver()
        PathHelper.save_to_json(self.blogs)

# just for testing
if __name__ == '__main__':
    objArr = PathHelper.get_array_from_json("result_20181221_100606.json")
    SplitSentence(objArr).run()