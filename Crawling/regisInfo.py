#coding:utf-8
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
from copy import deepcopy
import re
from configure import cpu_num,thread_num_per_cpu

# output=sys.stdout
# outputfile=open("F:\\田\学习文档\\python_code\\python_code\\log_dir\\regisinfo.txt","w")
# sys.stdout=outputfile

p2peye_website = "https://www.p2peye.com/shuju/ptsj/"

##爬取平台首页
def get_regisinfo_info(link) :
    regisinfo_link = link+"beian"
    print("爬取平台注册信息 ：{}".format(regisinfo_link))
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    regisinfo_dic = {}
    ##爬取基础内容
    driver.get(regisinfo_link)
    web = BeautifulSoup(driver.page_source, "html.parser")
    try :
        regisinfo_dic["platform"] = web.find_all("div", "name")[0].text
    except :
        driver.close()
        time.sleep(2)
        return ("无平台信息"+link)
    try :
        regisinfo_dic["website"] = regisinfo_link
        info_tag_list = web.findAll("div", "detail")
        gsinfo_list = info_tag_list[0].find("div", "account").find_all("div", "item_top")
        regisinfo_dic["change_num"] = int(gsinfo_list[0].text)
        regisinfo_dic["abnormal_oper_num"] = int(gsinfo_list[1].text)
        regisinfo_dic["dishonest_num"] = int(gsinfo_list[2].text)
        regisinfo_df = pd.DataFrame(columns=["abnormal_date", "abnormal_reason", "abnormal_instit", "abnormal_remove_date",
                     "abnormal_remove_reason", "abnormal_remove_intit"])
        for idx,info_tag in enumerate(info_tag_list) :
            if info_tag.find("div", "stit").text[:4] in ["工商信息","备案信息"]  :
                for tag in info_tag.find("div", "kvs").findAll("div"):
                    try :
                        regisinfo_dic[tag.find("div", "k").text] = tag.find("div", "v").text
                    except :
                        continue
            elif info_tag.find("div", "stit").text[:4] == "主要人员" :
                regisinfo_dic["exacutives_num"] = int(re.search(string=info_tag.find("div", "stit").text, pattern="\d+")[0])

        ##异常信息
            if info_tag.find("div", "stit").text[:4] == "经营异常" :
                abnormal_detail = info_tag.find("table","myTable_jyyc").find("tbody").findAll("tr")
                for idx,tag in enumerate(abnormal_detail):
                    regisinfo_df.loc[idx, :] = [x.text for x in tag.findAll("td")[1:]]
        if len(regisinfo_df) == 0 :
            regisinfo_df.loc[0,:] = [None, None, None, None,None, None]

        for k,v in regisinfo_dic.items() :
            regisinfo_df[k] = v
        time.sleep(2)
        driver.close()
        return regisinfo_df
    except :
        print("爬取不成功 ："+regisinfo_link)
        time.sleep(2)
        driver.close()
        return "爬取不成功"+link


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
    driver.close()

    ##爬取平台注册信息
    pool = Pool(cpu_num)
    data_list = pool.map(get_regisinfo_info,list(ptsjlink["link"]))
    data_list = [x for x in data_list if type(x)!=str]
    regisinfo = pd.concat(data_list,sort=True,ignore_index=True)

    ##保存首页信息
    regisinfo.to_excel("DataDone/regisinfo.xlsx",encoding="utf-8")

