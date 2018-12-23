#coding:utf-8
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from functools import reduce
import sys

p2peye_website = "https://www.p2peye.com/shuju/ptsj/"

##爬取平台首页
def get_homePage_info(link,driver) :

    platform_dic = {}

    ##爬取基础内容
    driver.get(link)
    web = BeautifulSoup(driver.page_source, "html.parser")
    try :
        platform_dic["platform"] = web.find_all("div", "name")[0].text
    except :
        print("暂无平台信息")
    platform_dic["website"] = link

    try:
        platform_dic["credit_grade"] = web.find_all("i", "head-info-rank-value-italic")[0].text
    except :
        print("平台无评级信息")

    try :
        platform_dic["launch_date"] = web.find_all("span", "online-time")[0].text.split("：")[1]
    except :
        print("平台无上线时间信息")

    try :
        platform_dic["rate"] = web.find_all("a", "head-info-value head-info-value-red")[0].text
    except :
        print("平台无利率信息")

    try :
        platform_dic["praise_percent"] = web.find_all("p", "ui-gzbtnbox-text-top")[0].text.split(" ")[0]
    except :
        print("平台无好评度信息")

    try :
        ##爬取公司背景
        for tag in web.find_all("div", "strength-item"):
            key = tag.find_all("span", "strength-key")[0].text
            value = reduce(lambda x, y: x + ";" + y, [x.text for x in tag.find_all("span", "strength-value")])
            platform_dic[key] = value
    except :
        print("平台无背景信息")

    try :
        ##爬取公司简介
        platform_dic["intro"] = reduce(lambda x, y: x + ";" + y,
                                       [x.text for x in
                                        web.find_all(name="div", id="pingtaijianjie")[0].find_all(name="td", attrs="desc")])
    except :
        print("平台无简介信息")

    try :
        ##爬取资费情况
        for tag in web.find_all(name="div", attrs="bd", id="zifeishuoming")[0].find_all("tr"):
            platform_dic[tag.find("td", "tit").text[1:]] = tag.find("td", "desc").text
    except :
        print("平台无资费信息")

    try:
        ##爬取高管信息
        platform_dic["ececutive"] = reduce(lambda x, y: x + ";" + y,
                                           [x.text for x in web.find_all("dd", "describe")[0].find_all("p")])
    except :
        print("平台无高管信息")

    try:
        ##爬取照片信息
        platform_dic["picture"] = web.find_all("div", "hd-s")[0].text
    except :
        print("平台无照片信息")

    try:
        ##爬起产品信息
        for tag in web.find_all(name="div", attrs="bd product-info-bd", id="chanpinxinxi")[0].find_all("li"):
            platform_dic[tag.find("span", "product-info-key").text] = tag.find("span", "product-info-value").text
    except :
        print("平台无产品信息")

    try :
        ##爬取联系方式
        for tag in web.find_all(name="div", attrs="bd", id="lianxipingtai")[0].find_all("tr"):
            platform_dic[tag.find("td", "tit").text[1:]] = tag.find("td", "desc").text
    except :
        print("平台无联系方式")

    try:
        ##爬取用户印象
        platform_dic["impression"] = reduce(lambda x, y: x + ";" + y,
                                            [x.text for x in
                                             web.find_all(name="div", attrs="impression-bd")[1].find_all("a")])
    except :
        print("平台无用户印象信息")

    return  platform_dic

if __name__ == "__main__" :

    ###获取平台的链接
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(p2peye_website)
    web = BeautifulSoup(driver.page_source,"html.parser")
    link_list = []
    link_tag = web.body.find_all(name="tr", attrs="bd")
    for x in range(len(web.body.find_all("tr", "bd"))):
        link_list.append("http:"+link_tag[x].a["href"][:-6])
    ptsjlink = pd.DataFrame(link_list,columns=["link"])
    print(ptsjlink)

    ##爬取平台首页信息
    data_list = []
    for link in ptsjlink.link.unique() :
        print("爬取{}".format(link))
        platform_dic = get_homePage_info(link,driver)
        data_list.append(platform_dic)
        print("爬取成功")
        print("######################################################")

    ##保存首页信息
    homePage = pd.DataFrame(data_list)
    homePage.to_excel("DataDone/homePage.xlsx")

    driver.close()