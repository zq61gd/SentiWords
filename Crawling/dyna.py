# coding:utf-8
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from copy import deepcopy
from functools import reduce
from multiprocessing.dummy import Pool as Tpool
from multiprocessing import Pool
from configure import cpu_num,thread_num_per_cpu

p2peye_website = "https://www.p2peye.com/shuju/ptsj/"

def get_dyna_info(dyna_dic):
    link_dyna = "http:" + dyna_dic["website"]
    print("抓取官方信息内容:" + link_dyna)
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(link_dyna)
    dyna_web = BeautifulSoup(driver.page_source, "html.parser")
    dyna_df = pd.DataFrame(
        columns=["dyna_com_user", "dyna_com_content", "dyna_com_time", "dyna_article", "dyna_ori_com_user","dyna_ori_com"])
    try:
        try:
            dyna_article = dyna_web.find("div", "文章内容").text
        except :
            dyna_article = dyna_web.find(name="td", id="article_content").text
        ##让页面加载完全
        # len_ori = len(dyna_web.findAll("div", "record"))
        # driver.execute_script("window.scrollBy(0,100000)")
        # time.sleep(1)
        # dyna_web = BeautifulSoup(driver.page_source, "html.parser")
        # len_now = len(dyna_web.findAll("div", "record"))
        # while len_ori != len_now:
        #     driver.execute_script("window.scrollBy(0,20000)")
        #     time.sleep(1)
        #     dyna_web = BeautifulSoup(driver.page_source, "html.parser")
        #     len_ori = len_now
        #     len_now = len(dyna_web.findAll("div", "div"))

        ##抓取评论信息
        response_tags = dyna_web.findAll("div", "record")
        for idx, tag in enumerate(response_tags):
            dyna_com_content = tag.find("div", "record-con").text
            dyna_com_user = tag.find("div", "record-hd-ri-top").text
            dyna_com_time = tag.find("div", "record-hd-ri-bot").text
            ##分为有回复和无回复
            try:
                response_ori = tag.findAll("blockquote").text
                dyna_ori_com_user = response_ori.split(":")[0]
                dyna_ori_com = reduce(lambda x, y: x + ";#;" + y,response_ori.split(":")[1:])
            except:
                dyna_ori_com_user = None
                dyna_ori_com = None

            dyna_df.loc[idx, :] = [dyna_com_user, dyna_com_content, dyna_com_time, dyna_article, dyna_ori_com_user,dyna_ori_com]

        ##无评论
        if len(dyna_df) == 0:
            dyna_df.loc[0, :] = [None, None, None, None, None,None]

        dyna_df["website"] = link_dyna
        dyna_df["platform"] = dyna_dic["platform"]
        dyna_df["dyna_title"] = dyna_dic["dyna_title"]
        dyna_df["dyna_time"] = dyna_dic["dyna_time"]
        dyna_df["dyna_vol"] = dyna_dic["dyna_vol"]
        dyna_df["dyna_com_num"] = dyna_dic["dyna_com_num"]
        dyna_df["dyna_article"] = dyna_article
        time.sleep(5)
        driver.close()
        return dyna_df
    except:
        dyna_df.loc[0, :] = [None, None, None, None, None,None]
        dyna_df["website"] = link_dyna
        dyna_df["platform"] = dyna_dic["platform"]
        dyna_df["dyna_title"] = dyna_dic["dyna_title"]
        dyna_df["dyna_time"] = dyna_dic["dyna_time"]
        dyna_df["dyna_vol"] = dyna_dic["dyna_vol"]
        dyna_df["dyna_com_num"] = dyna_dic["dyna_com_num"]
        dyna_df["dyna_article"] = None
        time.sleep(5)
        driver.close()
        return dyna_df

def get_dyna_link(platform_link):
    dyna_link_ori = platform_link + "gfdt/"
    print("抓取平台:" + dyna_link_ori)
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    dyna_data = []
    ##爬取平台名称
    try :
        driver.get(dyna_link_ori)
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
            dyna_link = dyna_link_ori
        else:
            dyna_link = dyna_link_ori + "/p%d" % page_idx
        print("抓取官方动态链接：" + dyna_link)
        print("####################")

        driver.get(dyna_link)
        dyna_web = BeautifulSoup(driver.page_source, "html.parser")
        dyna_tag = dyna_web.find("div", "mod-list").findAll("li", "item clearfix")
        for tag in dyna_tag:
            dyna_dic = {}
            dyna_dic["platform"] = platform
            hd = tag.find("div", "mc-hd")
            ft = tag.find("div", "mc-ft clearfix")
            dyna_dic["website"] = hd.find("a")["href"]
            dyna_dic["dyna_title"] = hd.find("a").text
            dyna_dic["dyna_time"] = ft.find("span", "mc-ft-l time").text
            dyna_dic["dyna_vol"] = int(ft.find("span", "ft-see").text)
            dyna_dic["dyna_com_num"] = int(ft.find("span", "ft-comment").text)
            dyna_data.append(dyna_dic)
        time.sleep(5)
    driver.close()
    return dyna_data

def get_link_thread(link_list):
    tpool = Tpool(thread_num_per_cpu)
    data_list = tpool.map(get_dyna_link, link_list)
    return data_list

def get_dyna_thread(dic_list):
    tpool = Tpool(thread_num_per_cpu)
    data_list = tpool.map(get_dyna_info, dic_list)
    return data_list

if __name__ == "__main__":

    ###获取平台的链接
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
    pool = Pool(cpu_num)
    palt_list = []
    ##多线程 多进程 抓取链接
    for x in range(0, len(ptsjlink)):
        palt_list.append(list(ptsjlink["link"][thread_num_per_cpu * x:thread_num_per_cpu * x + thread_num_per_cpu]))
    dyna_link_list = pool.map(get_link_thread, palt_list)
    print("抓取论坛链接成功")
    dyna_link_list = reduce(lambda x, y: x + y, dyna_link_list)
    dyna_link_list = [x for x in dyna_link_list if type(x)!=str]
    dyna_link_list_ori = reduce(lambda x, y: x + y, dyna_link_list)
    test_df = pd.DataFrame(dyna_link_list_ori)
    test_df.to_csv("dyna_dir/dyna_link_list.csv")

    dyna_link_list_ori = pd.read_csv("dyna_dir/dyna_link_list.csv", index_col=0).to_dict(orient="records")
    ##多线程 多进程 抓取内容
    start = 0
    while start < len(dyna_link_list_ori):
        try:
            dyna_link_list = dyna_link_list_ori[start:start + 500]
            dyna_list = []
            for x in range(0, int(len(dyna_link_list) / thread_num_per_cpu)):
                dyna_list.append(dyna_link_list[thread_num_per_cpu * x:thread_num_per_cpu * x + thread_num_per_cpu])

            data_list = pool.map(get_dyna_thread, dyna_list)
            data_list = reduce(lambda x, y: x + y, data_list)
            data_list = [x for x in data_list if type(x) != str]
            data = pd.concat(data_list,sort=True,ignore_index=False)
            ##保存论坛信息
            data.to_excel("DataDone/dyna_dir/{}_{}dyna.xlsx".format(start, start + 500))
            del (data)
        except:
            print("爬取{}-{}未成功".format(start, start + 500))
        time.sleep(30)
        start += 500

