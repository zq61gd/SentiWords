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
from configure import cpu_num,thread_num_per_cpu

p2peye_website = "https://www.p2peye.com/shuju/ptsj/"

def get_review_info(review_dic):
    link_review = review_dic["website"]
    print("抓取内容:" + link_review)
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(link_review)
    review_web = BeautifulSoup(driver.page_source, "html.parser")
    review_df = pd.DataFrame(
        columns=["review_user", "review_time", "review_core", "review_content", "review_impression","review_repo_num","review_repo"])

    ##抓取评论信息
    review_tags = review_web.findAll("li", "feed-detail clearfix")
    for idx, tag in enumerate(review_tags):
        review_content = tag.find("div", "link").text
        review_user = tag.find("a", "qt-gl username")["title"]
        review_time = tag.find("div", "qt-gl time").text
        review_core = tag.find("div", "info clearfix").text
        try:
            review_impression = reduce(lambda x,y:x+" "+y,[x.text for x in tag.find_all("ul", "qt-gl")])
        except :
            review_impression = None
        ##分为有回复和无回复
        try:
            repo_list = [x.text for x in tag.findAll("li")]
            review_repo_num = len(repo_list)
            review_repo = reduce(lambda x, y: x + ";#;" + y, repo_list)
        except:
            review_repo_num = 0
            review_repo = None
        review_df.loc[idx, :] = [review_user, review_time, review_core, review_content,
                                 review_impression,review_repo_num,review_repo]
    review_df["platform"] = review_dic["platform"]
    review_df["website"] = link_review
    driver.close()
    return review_df

def get_review_link(platform_link):
    review_link_ori = platform_link + "comment/"
    print("抓取平台:" + review_link_ori)
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    ##爬取平台名称
    driver.get(review_link_ori)
    web = BeautifulSoup(driver.page_source, "html.parser")
    try:
        platform = web.find_all("div", "name")[0].text
    except:
        time.sleep(2)
        driver.close()
        return "空平台"

    page_num = len(web.find(name="div", attrs="c-page").findAll("a"))
    if page_num > 1000:
        time.sleep(2)
        driver.close()
        return "review 数据异常"

    review_link_list = []
    for idx in range(page_num) :
        review_link_dic ={}
        review_link_dic["platform"] = platform
        if idx == 0 :
            review_link_dic["website"] = review_link_ori
        else :
            review_link_dic["website"] = review_link_ori+"list-0-0-{}.html".format(idx)
        review_link_list.append(review_link_dic)
    driver.close()
    time.sleep(2)
    return review_link_list

def get_link_thread(link_list):
    tpool = Tpool(thread_num_per_cpu)
    data_list = tpool.map(get_review_link, link_list)
    return data_list

def get_review_thread(dic_list):
    tpool = Tpool(thread_num_per_cpu)
    data_list = tpool.map(get_review_info, dic_list)
    return data_list

if __name__ == "__main__":

    ##获取平台的链接
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(p2peye_website)
    web = BeautifulSoup(driver.page_source, "html.parser")

    link_list = []
    link_tag = web.body.find_all(name="tr", attrs="bd")
    for x in range(len(web.body.find_all("tr", "bd"))):
        link_list.append("http:"+link_tag[x].a["href"][:-6])
    ptsjlink = pd.DataFrame(link_list,columns=["link"])
    driver.close()

    ##爬取平台review信息
    pool = Pool(cpu_num)
    palt_list = []
    ##多线程 多进程 抓取链接
    for x in range(1,int(len(ptsjlink)/thread_num_per_cpu)) :
        palt_list.append(list(ptsjlink["link"][thread_num_per_cpu*x:thread_num_per_cpu*x+thread_num_per_cpu]))
    review_link_list_ori = pool.map(get_link_thread,palt_list)
    print("抓取review链接成功")
    review_link_list_ori = reduce(lambda x,y:x+y,review_link_list_ori)
    review_link_list_ori = [x for x in review_link_list_ori if type(x) != str]
    review_link_list_ori = reduce(lambda x, y: x + y, review_link_list_ori)
    test_df = pd.DataFrame(review_link_list_ori)
    test_df.to_csv("review_dir/review_link_list_ori.csv",encoding="utf-8")

    review_link_list_ori = pd.read_csv("review_dir/review_link_list_ori.csv",index_col=0).to_dict(orient="records")
    start = 0
    while start < len(review_link_list_ori)-1:
        try:
            review_link_list = review_link_list_ori[start:start + 500]
            review_list = []
            for x in range(0, int(len(review_link_list) / thread_num_per_cpu)):
                review_list.append(list(review_link_list[thread_num_per_cpu * x:thread_num_per_cpu * x + thread_num_per_cpu]))
            data_list = pool.map(get_review_thread, review_list)
            data_list = reduce(lambda x, y: x + y, data_list)
            data_list = [x for x in data_list if type(x) != str]
            data = pd.concat(data_list,sort=True,ignore_index=True)
            ##保存论坛信息
            data.to_excel("DataDone/review_dir/{}_{}review.xlsx".format(start, start + 500),encoding="utf-8")
            del (data)
        except:
            print("爬取{}-{}未成功".format(start, start + 500))
        time.sleep(30)
        start += 500


