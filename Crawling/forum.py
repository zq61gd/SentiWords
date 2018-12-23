#coding:utf-8
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

def get_forum_info(forum_dic) :
    link_forum = "http:"+forum_dic["website"]
    print("抓取内容:" +link_forum)
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(link_forum)
    forum_web = BeautifulSoup(driver.page_source, "html.parser")
    forum_df = pd.DataFrame(
        columns=["forum_com_user", "forum_com_time", "forum_com_content", "forum_com_repo_num", "forum_com_repo"])
    try :
        context = forum_web.find("td","t_f").text
        ##让页面加载完全
        len_ori = len(forum_web.findAll("td", "plc"))
        driver.execute_script("window.scrollBy(0,100000)")
        time.sleep(1)
        forum_web = BeautifulSoup(driver.page_source, "html.parser")
        len_now = len(forum_web.findAll("td", "plc"))
        while len_ori != len_now:
            driver.execute_script("window.scrollBy(0,20000)")
            time.sleep(1)
            forum_web = BeautifulSoup(driver.page_source, "html.parser")
            len_ori = len_now
            len_now = len(forum_web.findAll("td", "plc"))
    
        ##抓取评论信息
        response_tags = forum_web.findAll("div", "replayTab")
        for idx,tag in enumerate(response_tags):
            try :
                forum_com_content = tag.find("div", "t_fsz").text
            except :
                forum_com_content = tag.find("td", "t_f").text
            forum_com_user = tag.find("a","avtm")["title"]
            forum_com_time = re.search(string=tag.find("p","pl_r").text,pattern="\d{4}-\d{2}-\d{2} \d{2}:\d{2}")[0]
            ##分为有回复和无回复
            try :
                repo_list = [x.text for x in tag.findAll("li")]
                forum_com_repo_num = len(repo_list)
                forum_com_repo = reduce(lambda x,y:x+";#;"+y,repo_list)
            except :
                forum_com_repo_num = 0
                forum_com_repo = None
            forum_df.loc[idx,:] = [forum_com_user,forum_com_time,forum_com_content,forum_com_repo_num,forum_com_repo]
    
        ##无评论
        if len(forum_df) == 0 :
            forum_df.loc[0, :] = [None, None, None, None, None]
    
        forum_df["website"] = link_forum
        forum_df["platform"] = forum_dic["platform"]
        forum_df["forum_title"] = forum_dic["forum_title"]
        forum_df["forum_time"] = forum_dic["forum_time"]
        forum_df["forum_vol"] = forum_dic["forum_vol"]
        forum_df["forum_com_num"] = forum_dic["forum_com_num"]
        forum_df["forum_type"] = forum_dic["forum_type"]
        forum_df["forum_article"] = context
        time.sleep(2)
        driver.close()
        return forum_df
    except :
        forum_df.loc[0, :] = [None, None, None, None, None]
        forum_df["website"] = link_forum
        forum_df["platform"] = forum_dic["platform"]
        forum_df["forum_title"] = forum_dic["forum_title"]
        forum_df["forum_time"] = forum_dic["forum_time"]
        forum_df["forum_vol"] = forum_dic["forum_vol"]
        forum_df["forum_com_num"] = forum_dic["forum_com_num"]
        forum_df["forum_type"] = forum_dic["forum_type"]
        forum_df["forum_article"] = None
        time.sleep(2)
        driver.close()
        return forum_df

def get_forum_link(platform_link) :
    forum_link_ori = platform_link + "forum"
    print("抓取平台:"+forum_link_ori)
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    forum_data = []
    ##爬取平台名称
    driver.get(forum_link_ori)
    web = BeautifulSoup(driver.page_source, "html.parser")
    try :
        platform= web.find_all("div", "name")[0].text
    except :
        time.sleep(2)
        driver.close()
        return "空平台"

    page_num = int(web.find_all(name="div", attrs="c-page")[0]["pn"])
    if page_num > 500 :
        time.sleep(2)
        driver.close()
        return "论坛数据异常"

    for page_idx in range(1,page_num+1) :

        if page_idx == 1:
            forum_link = forum_link_ori
        else:
            forum_link = forum_link_ori + "/p%d" % page_idx
        print("抓取论坛链接："+forum_link)
        print("####################")

        driver.get(forum_link)
        forum_web = BeautifulSoup(driver.page_source, "html.parser")
        forum_tag = forum_web.find("div", "mod-list").findAll("li", "item clearfix")
        for tag in forum_tag :
            forum_dic = {}
            forum_dic["platform"] = platform
            hd = tag.find("div","mc-hd")
            ft = tag.find("div","mc-ft clearfix")
            forum_dic["website"] = hd.find_all("a")[1]["href"]
            forum_dic["forum_type"]  = hd.find_all("a")[0].text
            forum_dic["forum_title"] = hd.find_all("a")[1].text
            forum_dic["forum_time"] = ft.find("span","mc-ft-l").text
            forum_dic["forum_vol"] = int(ft.find("span","ft-see").text)
            forum_dic["forum_com_num"] = int(ft.find("span","ft-comment").text)
            forum_data.append(forum_dic)
        time.sleep(2)
    driver.close()
    return forum_data

def get_link_thread(link_list):
    tpool = Tpool(thread_num_per_cpu)
    data_list = tpool.map(get_forum_link,link_list)
    return data_list

def get_forum_thread(dic_list):
    tpool = Tpool(thread_num_per_cpu)
    data_list = tpool.map(get_forum_info,dic_list)
    return data_list


if __name__ == "__main__" :

    ###获取平台的链接
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(p2peye_website)
    web = BeautifulSoup(driver.page_source, "html.parser")

    link_list = []
    link_tag = web.body.find_all(name="tr", attrs="bd")
    for x in range(len(web.body.find_all("tr", "bd"))):
        link_list.append("http:"+link_tag[x].a["href"][:-6])
    ptsjlink = pd.DataFrame(link_list,columns=["link"])
    driver.close()

    # ##爬取平台论坛信息
    pool = Pool(cpu_num)
    palt_list = []
    ##多线程 多进程 抓取链接
    for x in range(0,int(len(ptsjlink)/thread_num_per_cpu)) :
        palt_list.append(list(ptsjlink["link"][thread_num_per_cpu*x:thread_num_per_cpu*x+thread_num_per_cpu]))
    forum_link_list = pool.map(get_link_thread,palt_list)
    print("抓取论坛链接成功")
    forum_link_list = reduce(lambda x,y:x+y,forum_link_list)
    for data in deepcopy(forum_link_list):
        if type(data) == str:
            forum_link_list.remove(data)
    forum_link_list_ori = reduce(lambda x, y: x + y, forum_link_list)
    test_df = pd.DataFrame(forum_link_list)
    test_df.to_csv("forum_dir/forum_link_list.csv")

    forum_link_list_ori = pd.read_csv("forum_dir/forum_link_list.csv",index_col=0).to_dict(orient="records")
    ##多线程 多进程 抓取内容
    start = 0
    while start < len(forum_link_list_ori):
        try :
            forum_link_list = forum_link_list_ori[start:start+500]
            forum_list = []
            for x in range(0,int(len(forum_link_list)/thread_num_per_cpu)):
                forum_list.append(forum_link_list[thread_num_per_cpu*x:thread_num_per_cpu*x+thread_num_per_cpu])

            data_list = pool.map(get_forum_thread,forum_list)
            data_list = reduce(lambda x,y:x+y,data_list)
            data_list = [x for x in data_list if type(x) != str]
            data = pd.concat(data_list,sort=True,ignore_index=True)
            ##保存论坛信息
            data.to_excel("DataDone/forum_dir/{}_{}forum.xlsx".format(start,start+500))
            del(data)
        except :
            print("爬取{}-{}未成功".format(start,start+500))
        time.sleep(30)
        start += 500

