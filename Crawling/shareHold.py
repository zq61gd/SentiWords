#coding:utf-8
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing import Pool
from configure import cpu_num,thread_num_per_cpu
import sys

# output=sys.stdout
# outputfile=open(".\\log_dir\\shareHold.txt","w")
# sys.stdout=outputfile

p2peye_website = "https://www.p2peye.com/shuju/ptsj/"

##爬取平台首页
def get_shareHold_info(link) :
    shareHold_link = link+"beian"
    print("爬取平台股东信息 ：{}".format(shareHold_link))
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    shareHold_dic = {}
    ##爬取基础内容
    driver.get(shareHold_link)
    web = BeautifulSoup(driver.page_source, "html.parser")
    try :
        shareHold_dic["platform"] = web.find_all("div", "name")[0].text
    except :
        driver.close()
        time.sleep(2)
        return ("暂无平台信息")
    try :
        shareHold_dic["website"] = shareHold_link
        ##股东信息
        shareHold_df = pd.DataFrame(columns=["shareholder_name", "shareholding_ratio", "contribution"])
        for gd_tag in web.findAll("div", "detail") :
            if gd_tag.find("div","stit").text[:4] =="股东信息" :
                shareHold_detail = gd_tag.find("div", "tbl_body").findAll("div","tbl_tr")
                for idx, tag in enumerate(shareHold_detail):
                    shareHold_df.loc[idx, :] = [x.text for x in tag.findAll("div","tbl_td")]

        for k,v in shareHold_dic.items() :
            shareHold_df[k] = v

        shareHold_df["shareholder_num"] = len(shareHold_df)


        time.sleep(2)
        driver.close()
        return  shareHold_df
    except :
        print("爬取不成功:"+shareHold_link)
        time.sleep(2)
        driver.close()
        return ("爬取不成功")

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

    ##爬取平台股东信息
    pool = Pool(cpu_num)
    data_list = pool.map(get_shareHold_info,list(ptsjlink["link"]))
    data_list = [x for x in data_list if type(x) != str]
    shareHold = pd.concat(data_list,sort=True)

    ##保存首页信息

    shareHold.to_excel("DataDone/shareHold.xlsx",encoding="utf-8")

