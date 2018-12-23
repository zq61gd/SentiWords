import re
import xlrd


xl_file = xlrd.open_workbook('review.xlsx')

sheet = xl_file.sheet_by_index(0)


# 换行的话要写‘\n’
with open('new_review.csv', 'w',encoding='gbk') as f:
    f.write(',platform,review_content,review_core,review_impression,review_repo,review_repo_num,review_time，review_user，website\n')

# 这里是从第二行开始逐行处理，因为第一行为标题
for i in range(1, sheet.nrows):
    # 这里获取的是第i行的数据，返回的是一个数组，里面元素对应每一列
    line = sheet.row_values(i)
    # 这里对读出的这一行的每一个元素进行操作，一共有8个元素
    for j in range(10):
        content = line[j]
        # 因为第一列的元素是浮点型，所以这里把他转化成字符串
        if j==0:
            content = str(content)
        if j==6:
            content = str(content)
        if j==2:
            content=re.sub('更多','',line[2])

        if j==3:         
            content=re.sub(line[8],'',line[3])
        if j==5:
            content=re.sub(';#;','',line[5])
            content=re.sub(line[4],'',content)
                   
        content = re.sub('\n',' ', content)
        content = re.sub(',','，', content)
       
        # 这里就是将读取出来并经过处理的数据写入前面创建好的csv文件，除了最后一个元素之外，每个元素后面都要加一个逗号用来隔开
        if j!=9:
            # print(content)
            try:
                with open('new_review.csv', 'a', encoding='gbk') as f:
                    f.write(content + ',')
            except:
                print('line %d is invalid'%(i+1))
                with open('new_review.csv', 'a', encoding='gbk') as f:
                    f.write(',')
        else:
            with open('new_review.csv', 'a', encoding='gbk') as f:
                f.write(content + '\n')
