import os
import pandas as pd

path_list = ["./DataDone/ask_dir/","./DataDone/dyna_dir/",
             "./DataDone/fourm_dir/","./DataDone/news_dir/","./DataDone/review_dir/"]

for path in path_list :
    data_name_list = os.listdir(path)
    data_list = []
    for data_name in data_name_list :
        print(path + data_name)
        try:
            data_list.append(pd.read_csv(path+data_name,index_col=0,encoding="utf-8",engine="python"))
        except :
            data_list.append(pd.read_excel(path + data_name, index_col=0, encoding="utf-8"))
    pd.concat(data_list,ignore_index=True,sort=True).to_csv(path+path[11:].split("_")[0]+".csv",encoding="utf-8")