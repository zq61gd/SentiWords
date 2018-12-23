#coding:utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from functools import reduce
import time
import re
from multiprocessing import Pool
from configure import cpu_num,thread_num_per_cpu

p2peye_website = "https://www.p2peye.com/shuju/ptsj/"

##爬取平台新闻
def get_news_info(link) :
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    news_link = link + "news/"
    # try :
    driver.get(news_link)
    web_news_list = BeautifulSoup(driver.page_source, "html.parser")


    ##获取平台名称，同时排除空网站
    try:
        platform = web_news_list.find_all("div", "name")[0].text
    except:
        driver.close()
        return "平台无数据"

    ##获取新闻页数，同时排除新闻异常的网站
    news_page_num = int(web_news_list.find_all(name="div", attrs="c-page")[0]["pn"])
    if news_page_num > 500 :
        driver.close()
        return "新闻异常"

    ##开始按页抓取
    news_df_list = []

    for page_idx in range(1,news_page_num+1) :
        if page_idx == 1:
            news_link = link + "news/"
        else:
            news_link = link + "news/" + "p%d" % page_idx
        print(news_link)

        driver.get(news_link)
        web_news_list = BeautifulSoup(driver.page_source, "html.parser")
        ##爬取新闻标题和新闻网页
        for news_idx in range(len(web_news_list.findAll("div", "mc-hd"))):
            print(news_idx)
            news_website = "http:" + web_news_list.findAll("div", "mc-hd")[news_idx].a["href"]
            print(news_website)
            news_title = web_news_list.findAll("div", "mc-hd")[news_idx].a["title"]
            news_time = web_news_list.findAll("div", "mc-ft clearfix")[news_idx].find("span", "mc-ft-l time").text
            news_vol = int(web_news_list.findAll("div", "mc-ft clearfix")[news_idx].find("span", "ft-see").text)
            news_comment_num = int(web_news_list.findAll("div", "mc-ft clearfix")[news_idx].find("span", "ft-comment").text)

            ##进新闻网页爬取内容和评论
            try :
                driver.get(news_website)
                web = BeautifulSoup(driver.page_source, "html.parser")
            except :
                driver.close()
                return (news_website,news_title,news_time,news_vol,news_comment_num)

            context_list = web.findAll(name="td", id="article_content")
            if context_list != [] :
                context = reduce(lambda x, y: x + y, [x.text for x in context_list])
            else :
                context =  "该页为图片"

            news_df = pd.DataFrame(
                columns=["news_comment_user", "news_comment_time", "news_comment_content",
                         "news_ori_comment_user",
                         "news_ori_comment"])
            ##加载所有评论
            try :
                if len(web.findAll("a", "more")[0]["data-url"])!= 0 :
                    while web.findAll("a", "more")[0] == "加载更多&gt;&gt;":
                        webdriver.ActionChains(driver).double_click(
                            driver.find_elements_by_class_name("more")[0]).perform()
                        web = BeautifulSoup(driver.page_source, "html.parser")
            except :
                print("只有一页评论")
            response_tags = web.findAll("div", "record")
            ##抓取评论信息
            for idx, tag in enumerate(response_tags):
                context_list = re.findall(pattern="\S+", string=tag.text)
                news_comment_user = context_list[0]
                news_comment_time = context_list[1] + context_list[2]

                ##无原回复型
                if tag.find_all("blockquote") == []:
                    news_comment_content = context_list[3]
                    news_df.loc[idx, :] = [news_comment_user, news_comment_time, news_comment_content, None,
                                           None]
                ##有原回复型
                else:
                    news_ori_comment = tag.find("blockquote").text.split(":")[-1]
                    try:
                        news_ori_comment_user = reduce(lambda x, y: x + y, context_list[3].split(":")[:-1])
                    except:
                        news_ori_comment_user = context_list[3]
                    news_comment_content = tag.find("div", "record-con").text[
                                           len(tag.find("blockquote").text) + 1:]
                    news_df.loc[idx, :] = [news_comment_user, news_comment_time, news_comment_content,
                                           news_ori_comment_user, news_ori_comment]

            if len(news_df)==0 :
                news_df.loc[0, :] = [None, None, None, None,
                                       None]
            news_df["website"] = news_website
            news_df["news_title"] = news_title
            news_df["news_time"] = news_time
            news_df["news_vol"] = news_vol
            news_df["news_comment_num"] = news_comment_num
            news_df["news_article"] = context

            news_df_list.append(news_df)
            time.sleep(2)

    if news_df_list != [] :
        news_df_all = pd.concat(news_df_list)
        news_df_all["platform"] = platform
    else :
        news_df_all = "平台无新闻数据"
    driver.close()
    return news_df_all



def get_single_page(link) :
    link_news = link[0]
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(link_news)
    web_news = BeautifulSoup(driver.page_source, "html.parser")
    news_website = link_news
    news_title = link[1]
    news_time = link[2]
    news_vol = link[3]
    news_comment_num = link[4]
    context_list = web_news.findAll(name="td", id="article_content")

    if context_list != []:
        context = reduce(lambda x, y: x + y, [x.text for x in context_list])
    else:
        context = "该页为图片"

    news_df = pd.DataFrame(
        columns=["news_comment_user", "news_comment_time", "news_comment_content",
                 "news_ori_comment_user",
                 "news_ori_comment"])
    try:
        if len(web_news.findAll("a", "more")[0]["data-url"]) != 0:
            while web_news.findAll("a", "more")[0] == "加载更多&gt;&gt;":
                webdriver.ActionChains(driver).double_click(
                    driver.find_elements_by_class_name("more")[0]).perform()
                web_news = BeautifulSoup(driver.page_source, "html.parser")
    except :
        print("只有一页评论")
    response_tags = web_news.findAll("div", "record")
    for idx, tag in enumerate(response_tags):
        ##无原回复型
        context_list = re.findall(pattern="\S+", string=tag.text)
        if tag.find_all("blockquote") == []:
            news_comment_user = context_list[0]
            news_comment_time = context_list[1] + context_list[2]
            news_comment_content = context_list[3]
            news_df.loc[idx, :] = [news_comment_user, news_comment_time, news_comment_content, None,
                                   None]

        ##有原回复型
        else:
            news_comment_user = context_list[0]
            news_comment_time = context_list[1] + context_list[2]
            news_ori_comment = tag.find("blockquote").text.split(":")[-1]
            try:
                news_ori_comment_user = reduce(lambda x, y: x + y, context_list[3].split(":")[:-1])
            except:
                news_ori_comment_user = context_list[3]
            news_comment_content = tag.find("div", "record-con").text[
                                   len(tag.find("blockquote").text) + 1:]
            news_df.loc[idx, :] = [news_comment_user, news_comment_time, news_comment_content,
                                   news_ori_comment_user, news_ori_comment]

    news_df["website"] = news_website
    news_df["news_title"] = news_title
    news_df["news_time"] = news_time
    news_df["news_vol"] = news_vol
    news_df["news_comment_num"] = news_comment_num
    news_df["news_article"] = context
    time.sleep(1)
    driver.close()
    return news_df

if __name__ == "__main__" :

    ###获取平台的链接
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(p2peye_website)
    web = BeautifulSoup(driver.page_source,"html.parser")
    print("解析成功")
    link_list = []
    link_tag = web.body.find_all(name="tr", attrs="bd")
    for x in range(len(web.body.find_all("tr", "bd"))):
        link_list.append("http:"+link_tag[x].a["href"][:-6])
    ptsjlink = pd.DataFrame(link_list,columns=["link"])
    print(ptsjlink)
    driver.close()

    ##爬取平台新闻信息
    pool = Pool(cpu_num)
    start = 0
    end = 40

    while start< len(ptsjlink) :
        print("start:"+str(start))
        try :
            data_list = pool.map(get_news_info,ptsjlink["link"][start:end])
            # data_list = []
            # for link in ptsjlink.link.unique():
            #     print("爬取{}".format(link))
            #     platform_df = get_news_info(link,driver)
            #     data_list.append(platform_df)
            #     print("爬取 "+ link + " 成功")
            #     print("######################################################")

            ##保存新闻信息
            res_list = []
            unsucceed = []
            for res in data_list :
                if type(res)!=str and type(res) != tuple :
                    res_list.append(res)
                elif type(res) == tuple :
                    unsucceed.append(res)

            unsucceed_df = []
            for link in unsucceed :
                try :
                    unsucceed_df.append(get_single_page(link))
                except :
                    continue

            news_info = pd.concat(res_list+unsucceed_df,ignore_index=True,sort=True)
            news_info.to_excel("DataDone/news_dir/{}_{}news.xlsx".format(start,end))
            start += 40
            end+= 40
            del(data_list)
            del(unsucceed_df)
            time.sleep(20)

        except :
            start += 40
            end += 40
            time.sleep(20)

