# -*- coding: utf-8 -*-
#!/usr/bin/env python
'''
@Time    : 2018/12/21 15:50
@Author  : suojijun1994@gmail.com
@Site    :
@File    : ExcelExtractor.py
@Software: PyCharm
'''
from builtins import object

from DataStructure.Article import Article
from DataStructure.Comment import Comment
from DataStructure.Reply import Reply
from FileUtil import PathHelper
import openpyxl


class ExcelExtractor(object):
    def __init__(self, filepath, sheetname = None):
        self._filepath = filepath
        self._sheetname = sheetname
        self.is_first_row = True
        self.blogs = []
        self.last_article = None
        self.last_comm = None
        self.last_reply = None
        self.comms_tmp = []
        self.reps_tmp = []

    def prepare(self, row):
        self.set_article(row)
        self.set_comment(row)
        self.set_reply(row)
        self.is_first_row = False

    def set_article(self, row):
        if row == None:
            return
        self.last_article = Article()
        self.last_article.index_0 = row[1].value
        self.last_article.forum_type = row[2].value
        self.last_article.forum_title = self.split_table(row[3].value)
        self.last_article.forum_time = row[4].value
        self.last_article.forum_vol = row[5].value
        self.last_article.platform = row[6].value
        self.last_article.website = row[7].value
        self.last_article.forum_article = self.split_table(row[8].value)
        self.last_article.forum_com_num = row[9].value

    def set_comment(self, row):
        if row == None:
            return
        self.last_comm = Comment()
        self.last_comm.forum_com_order = row[10].value
        self.last_comm.forum_com_user = row[11].value
        self.last_comm.forum_com_time = row[12].value
        self.last_comm.forum_com_content = self.split_table(row[13].value)
        self.last_comm.forum_com_content_ori_time = row[14].value
        self.last_comm.forum_com_content_ori_ID = row[15].value
        self.last_comm.forum_com_content_ori_content = self.split_table(row[16].value)
        self.last_comm.forum_com_real_content = self.split_table(row[17].value)
        self.last_comm.forum_com_repo_num = row[18].value

    def set_reply(self, row):
        if row == None:
            return
        self.last_reply = Reply()
        self.last_reply.forum_repo_order = row[19].value
        self.last_reply.forum_com_repo = self.split_table(row[20].value)
        self.last_reply.forum_com_repo_time = row[21].value
        self.last_reply.forum_com_repo_ID = row[22].value
        self.last_reply.forum_com_re_repo_ID = row[23].value
        self.last_reply.forum_com_repo_content = self.split_table(row[24].value)

    def is_new_article(self, row):
        if row == None:
            return False
        if self.last_article.forum_article != self.split_table(row[8].value):
            return True
        else:
            return False

    def is_new_comment(self, row):
        if row == None:
            return False
        if self.last_comm.forum_com_content != self.split_table(row[13].value):
            return True
        else:
            return False

    def add_comment(self, row):
        if self.last_comm.forum_com_repo_num != 0:
            self.reps_tmp.append(self.last_reply)
        self.last_comm.replies = self.reps_tmp
        self.comms_tmp.append(self.last_comm)
        self.set_reply(row)
        self.set_comment(row)
        self.reps_tmp = []

    def add_article(self, row):
        self.last_article.comments = self.comms_tmp
        self.blogs.append(self.last_article)
        self.set_article(row)
        self.comms_tmp = []

    def add_blog(self, row):
        self.add_comment(row)
        self.add_article(row)

    def update_reply(self, row):
        self.reps_tmp.append(self.last_reply)
        self.set_reply(row)

    def update_comment(self, row):
        if self.is_new_comment(row):
            self.add_comment(row)
        else:
            self.update_reply(row)

    def extract(self, row):
        if self.is_first_row:
            self.prepare(row)
            return
        if self.is_new_article(row):
            self.add_blog(row)
        else:
            self.update_comment(row)

    def split_table(self, strval):
        if strval:
            return strval.replace(' ', '')

    def get_excel_sheet(self):
        wb = openpyxl.load_workbook(self._filepath)
        if self._sheetname:
            ws = wb.get_sheet_by_name(self._sheetname)
        else:
            ws = wb.active
        return ws

    def save(self):
        PathHelper.save_to_json(self.blogs)

    def start(self):
        ws =self.get_excel_sheet()
        for row in ws.rows:
            self.extract(row)
        self.add_blog(None)
        self.save()

# just for testing
if __name__ == "__main__":
    filepath = PathHelper.get_resource_abs_path("test1.xlsx")
    ExcelExtractor(filepath).start()



