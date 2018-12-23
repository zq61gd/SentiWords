#coding:utf-8
from selenium import webdriver
import time
from bs4 import BeautifulSoup
import pandas as pd
from multiprocessing.dummy import Pool as Tpool
from multiprocessing import Pool
from configure import cpu_num,thread_num_per_cpu
p2peye_website = "https://www.p2peye.com/shuju/ptsj/"

##爬取平台变更信息
def get_change_info(link) :
    change_website = link + "beian"
    print("爬取："+change_website)
    driver = webdriver.Firefox(executable_path="geckodriver-v0.23.0-win64\geckodriver.exe")
    driver.get(change_website)
    change_df = pd.DataFrame(columns=["change_date","change_program","beforechange","afterchange"])

    ##爬取平台名字
    change_web = BeautifulSoup(driver.page_source, "html.parser")
    try :
        platform = change_web.find_all("div", "name")[0].text
    except :
        time.sleep(2)
        driver.close()
        return change_df

    #爬取变更信息
    idx = 0
    while True :
        try :
            change_tag_list = change_web.find(name="tbody",id="tbl_bgjl").findAll("tr")
        except :
            driver.close()
            time.sleep(2)
            return change_df
        for tag in change_tag_list :
            com_list = [x.text for x in tag.findAll("td") ]
            change_df.loc[idx,:] = com_list
            idx += 1
        try :
            driver.execute_script("window.scrollBy(0,10000)")
            time.sleep(1)
            webdriver.ActionChains(driver).double_click(driver.find_element_by_link_text("下一页")).perform()
            change_web = BeautifulSoup(driver.page_source, "html.parser")
        except :
            break

    change_df["platform"] = platform
    change_df["website"] = change_website
    change_df["change_num"] = len(change_df)

    driver.close()
    time.sleep(2)
    return change_df

def get_change_thread(link_list) :
    pool = Tpool(thread_num_per_cpu)
    data = pool.map(get_change_info,link_list)
    return data

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

    ##爬取平台变更信息
    data_list = []
    pool = Pool(cpu_num)
    link_pair_list = []
    for x in range(0, int(len(ptsjlink)/ thread_num_per_cpu)):
        link_pair_list.append(ptsjlink["link"][thread_num_per_cpu * x:thread_num_per_cpu * x + thread_num_per_cpu])
    change_df_pair_list = pool.map(get_change_thread,link_pair_list)
    change_df_list = [y for x in change_df_pair_list for y in x]
    data = pd.concat(change_df_list)
    print("爬取成功")
    print("######################################################")

    ##保存首页信息
    # homePage = pd.DataFrame(data)
    data.to_excel("DataDone/change.xlsx")
