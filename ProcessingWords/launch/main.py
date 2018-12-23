#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/12/17 14:53
# @Author  : suojijun1994@gmail.com
# @Site    :
# @File    : Reply.py
# @Software: PyCharm
import os
import util.FileUtil as ftools
import openpyxl
import json
from DataStructure.Article import Article
from DataStructure.Comment import Comment
from DataStructure.Reply import Reply

class ParseContent(object):
    def __init__(self):
        self.last_content = ''

    def reset(self):
        self.last_content = ''

    def set_last_content(self, content):
        self.last_content = content

    def is_new_article(self, row):
        # print(self.last_content)
        content = split_table(row[8].value)
        if content != self.last_content:
            self.last_content = content
            return True
        return False

def load_raw_datas(filename, sheet='Sheet1'):
    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    parsetools = ParseContent()
    parsetools.reset()
    for row in ws.rows:
        if parsetools.is_new_article(row):
            print("---------------------------------")
            print(row[8].value)

def extract_article(filename):
    articleFile = r"E:\\PythonProjects\\ProcessingWords\\resources\\test.json"
    articles = []
    wb = openpyxl.load_workbook(filename)
    ws = wb.active
    parsetools = ParseContent()
    parsetools.reset()
    comm_num = 1
    comments = []
    replies = []
    article = None
    for row in ws.rows:
        if row[1].value == "index_0":
            article = Article()
            continue
        if parsetools.is_new_article(row):
            article.index_0 = row[1].value
            article.forum_type = row[2].value
            article.forum_title = row[3].value
            article.forum_time = row[4].value
            article.forum_vol = row[5].value
            article.platform = row[6].value
            article.website = row[7].value
            article.forum_article = split_table(row[8].value)
            articles.append(article)
            # 设置article的评论数，第一个article评论未统计完，所以不计入
            arrlen = len(articles)
            if arrlen > 1:
                articles[arrlen - 2].forum_com_num = comm_num
                articles[arrlen - 2].comments = comments
                articles[arrlen - 2].replies = replies
            article = Article()
            comments = []
            replies = []
            comm_num = 1
        else:
            comm_num += 1
        comments.append(extract_comment(row))
        replies.append(extract_reply(row))
    # 最后一篇文章设置评论数
    articles[len(articles) - 1].forum_com_num = comm_num

    with open(articleFile, "w+") as artfile:
        for item in articles:
            tmp = json.dumps(item, ensure_ascii=False, default = lambda x: x.__dict__)
            artfile.writelines(tmp.encode('utf8') + '\n')

def split_table(strval):
    if strval:
        return strval.replace(' ', '')

def extract_comment(row):
    comm = Comment()
    comm.forum_com_order = row[10].value
    comm.forum_com_user = split_table(row[11].value)
    comm.forum_com_time = row[12].value
    comm.forum_com_content = split_table(row[13].value)
    comm.forum_com_repo_num = row[18].value

    comm.forum_com_content_ori_time = row[14].value
    comm.forum_com_content_ori_ID = row[15].value
    comm.forum_com_content_ori_content = split_table(row[16].value)
    comm.forum_com_real_content = split_table(row[17].value)
    comm.replies = []
    return comm

def extract_reply(row):
    reply = Reply()
    reply.forum_repo_order = row[19].value
    reply.forum_com_repo = split_table(row[20].value)
    reply.forum_com_repo_time = row[21].value
    reply.forum_com_repo_ID = row[22].value
    reply.forum_com_re_repo_ID = row[23].value
    reply.forum_com_repo_content = split_table(row[24].value)
    return reply

if __name__ == "__main__":
    filename = r"E:\\PythonProjects\\ProcessingWords\\resources\\test.xlsx"
    # load_raw_datas(filename)
    # content = "                我投资 我理财 关你屁事 哈哈哈哈     "
    # print(content)
    # print(content.replace(' ', ''))
    # print(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    # extract_article(filename)
    # with open (r"E:\\PythonProjects\\ProcessingWords\\resources\\char.json", "w") as jsonfile:
        # ss = {
        #     "test": "我在测试中文分词",
        #     "index": 22
        # }
        # jsonfile.write(json.dumps(ss).decode('utf8'))

        # ls = []
        # tmp1 = {
        #     "test1": "哈哈哈哈",
        #     "test2": "abc",
        #     "test3": 12,
        #     "test4": []
        # }
        # ls.append(tmp1)
        # tmp2 = {
        #     "test1": "呵呵呵呵",
        #     "test2": "def",
        #     "test3": 13,
        #     "test4": []
        # }
        # ls.append(tmp2)
        # tmp3 = {
        #     "test1": "嘻嘻嘻嘻",
        #     "test2": "xyz",
        #     "test3": 14,
        #     "test4": []
        # }
        # ls.append(tmp3)
        # ss = json.dumps(ls, ensure_ascii=False)
        # print(ss)
        # jsonfile.write(ss)

    tests = []
    tests.append(ATest())
    tests.append(BTest())
    tests.append(CTest())
    for test in tests:
        test.prepare()
