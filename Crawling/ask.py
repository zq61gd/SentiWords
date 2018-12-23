# coding:utf-8
from selenium import webdriver
import numpy as np
import time
from bs4 import BeautifulSoup
import pandas as pd
from copy import deepcopy
from functools import reduce
from multiprocessing.dummy import Pool as Tpool
from multiprocessing import Pool
import re
import sys

# output=sys.stdout
# outputfile=open(".\\log_dir\\ask.txt","w")
# sys.stdout=outputfile

p2peye_website = "https://www.p2peye.com/shuju/ptsj/"

def get_ask_info(ask_dic):
    link_ask = "http:" + ask_dic["website"]
    print("抓取问答内容:" + link_ask)
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(link_ask)
    ask_web = BeautifulSoup(driver.page_source, "html.parser")
    ask_df = pd.DataFrame(
        columns=["ask_repo_user", "ask_repo_time" , "ask_repo_content"])
    try:

        ##抓取评论信息
        response_tags = ask_web.findAll("ul", "reply-list")
        for idx, tag in enumerate(response_tags):
            ask_repo_user = tag.find("a", "reply-content-name qt-gl").text
            ask_repo_time = tag.find("span", "qt-gl").text
            ask_repo_content = tag.find("div", "reply-content qt-gl").text
            ask_df.loc[idx, :] = [ask_repo_user, ask_repo_time, ask_repo_content]

        ##无评论
        if len(ask_df) == 0:
            ask_df.loc[0, :] = [None, None, None]

        ask_df["website"] = link_ask
        ask_df["platform"] = ask_dic["platform"]
        ask_df["ask_title"] = ask_dic["ask_title"]
        ask_df["ask_time"] = ask_dic["ask_time"]
        ask_dic["ask_user"] = ask_dic["ask_user"]
        ask_dic["ask_repo_num"] = len(ask_df)

        time.sleep(5)
        driver.close()
        return ask_df
    except:
        ask_df.loc[0, :] = [None, None, None]
        ask_df["website"] = link_ask
        ask_df["platform"] = ask_dic["platform"]
        ask_df["ask_title"] = ask_dic["ask_title"]
        ask_df["ask_time"] = ask_dic["ask_time"]
        ask_dic["ask_user"] = ask_dic["ask_user"]
        ask_dic["ask_repo_num"] = len(ask_df)
        time.sleep(5)
        driver.close()
        return ask_df

def get_ask_link(platform_link):
    ask_link_ori = platform_link + "ask/"
    print("抓取平台:" + ask_link_ori)
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    ask_data = []
    ##爬取平台名称
    try :
        driver.get(ask_link_ori)
        web = BeautifulSoup(driver.page_source, "html.parser")
        platform = web.find_all("div", "name")[0].text
    except:
        time.sleep(5)
        driver.close()
        return "空平台"

    page_num = int(web.find_all(name="div", attrs="c-page")[0]["pn"])
    if page_num > 500:
        time.sleep(5)
        driver.close()
        return "官方动态数据异常"

    for page_idx in range(1, page_num + 1):

        if page_idx == 1:
            ask_link = ask_link_ori
        else:
            ask_link = ask_link_ori + "p%d" % page_idx
        print("抓取问答链接：" + ask_link)
        print("####################")

        driver.get(ask_link)
        ask_web = BeautifulSoup(driver.page_source, "html.parser")
        ask_tag = ask_web.find("ul", "list-ul").findAll("li")
        for tag in ask_tag:
            ask_dic = {}
            ask_dic["platform"] = platform
            ask_dic["website"] = tag.find("a")["href"]
            ask_dic["ask_title"] = tag.find("a").text
            ask_dic["ask_time"] = tag.findAll("span", "qt-gl")[0].text
            ask_dic["ask_user"] = tag.findAll("span", "qt-gl")[1].text
            ask_dic["ask_repo_num"] = tag.find("span",'qt - gr list - item - info - reply')
            ask_data.append(ask_dic)
        time.sleep(5)
    driver.close()
    return ask_data

def get_link_thread(link_list):
    tpool = Tpool(2)
    data_list = tpool.map(get_ask_link, link_list)
    return data_list

def get_ask_thread(dic_list):
    tpool = Tpool(2)
    data_list = tpool.map(get_ask_info, dic_list)
    return data_list

if __name__ == "__main__":

    ##获取平台的链接
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(p2peye_website)
    web = BeautifulSoup(driver.page_source, "html.parser")

    link_list = []
    link_tag = web.body.find_all(name="tr", attrs="bd")
    for x in range(len(web.body.find_all("tr", "bd"))):
        link_list.append("http:" + link_tag[x].a["href"][:-6])
    ptsjlink = pd.DataFrame(link_list, columns=["link"])
    driver.close()

    # ##爬取平台论坛信息
    pool = Pool(4)
    palt_list = []
    ##多线程 多进程 抓取链接
    # for x in range(0, len(ptsjlink)):
    for x in range(0, 10):
        palt_list.append(list(ptsjlink["link"][2 * x:2 * x + 2]))
    ask_link_list = pool.map(get_link_thread, palt_list)
    print("抓取论坛链接成功")
    ask_link_list = reduce(lambda x, y: x + y, ask_link_list)
    for data in deepcopy(ask_link_list):
        if type(data) == str:
            ask_link_list.remove(data)
    ask_link_list_ori = reduce(lambda x, y: x + y, ask_link_list)
    test_df = pd.DataFrame(ask_link_list_ori)
    test_df.to_csv("ask_dir/ask_link_list.csv")

    ask_link_list_ori = pd.read_csv("ask_dir/ask_link_list.csv", index_col=0).to_dict(orient="records")
    ##多线程 多进程 抓取内容
    start = 0
    while start < len(ask_link_list_ori):
        try:
            ask_link_list = ask_link_list_ori[start:start + 500]
            ask_list = []
            for x in range(0, int(len(ask_link_list) / 2)):
                ask_list.append(ask_link_list[2 * x:2 * x + 2])

            data_list = pool.map(get_ask_thread, ask_list)
            data_list = reduce(lambda x, y: x + y, data_list)
            data = pd.concat(data_list,ignore_index=True,sort=True)

            ##保存论坛信息
            data.to_excel("DataDone/ask_dir/{}_{}ask.xlsx".format(start, start + 500))
            del (data)
        except:
            print("爬取{}-{}未成功".format(start, start + 500))
        time.sleep(30)
        start += 500

