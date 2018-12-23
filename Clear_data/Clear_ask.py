import re
import xlrd

xl_file = xlrd.open_workbook('ask1.xlsx')

sheet = xl_file.sheet_by_index(0)

# 这里我不是在源文件上写，而是重新写在另一个csv文件中，这里先把第一行标题写上去，注意csv文件每一列之间要用逗号隔开
# 换行的话要写‘\n’
with open('new_ask.csv', 'w') as f:
    f.write(',ask_time,ask_title,ask_repo_user,ask_repo_content,ask_repo_time,platform,website\n')

# 这里是从第二行开始逐行处理，因为第一行为标题
for i in range(1, sheet.nrows):
    # 这里获取的是第i行的数据，返回的是一个数组，里面元素对应每一列
    line = sheet.row_values(i)
    # 这里对读出的这一行的每一个元素进行操作，一共有8个元素
    for j in range(8):
        content = line[j]
        # 因为第一列的元素是浮点型，所以这里把他转化成字符串
        if j==0:
            content = str(content)
        if j==4:
            # 这里开始用很多正则表达式
            content=re.sub(line[3],'',line[4])
            content=re.sub(line[5],'',content)
            content=re.sub('size=\w','',content)
            content=re.sub('/size','',content)
            content=re.sub('color=#595959','',content)
            content=re.sub('color=#','',content)
            content=re.sub('/color','',content)
            content = re.sub('\[[^\[]*\]', '', content)
            
        
 
        content = re.sub('\n', ' ', content)
        content = re.sub(',', '，', content)
        content = re.sub('提交回复 还可输入2000字','',content)
        content = re.sub(' 0  0', '，', content)
        content = re.sub('0  1 ', '，', content)
        # 这里就是将读取出来并经过处理的数据写入前面创建好的csv文件，除了最后一个元素之外，每个元素后面都要加一个逗号用来隔开
        if j!=7:
            # print(content)
            try:
                with open('new_ask.csv', 'a', encoding='gbk') as f:
                    f.write(content + ',')
            except:
                print('line %d is invalid'%(i+1))
                with open('new_ask.csv', 'a', encoding='gbk') as f:
                    f.write(',')
        else:
            with open('new_ask.csv', 'a', encoding='gbk') as f:
                f.write(content + '\n')
