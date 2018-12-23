
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import re
import xlrd


# In[2]:


df=pd.read_csv(r'fourm.csv',encoding='utf-8')
pd.set_option('display.max_colwidth',1000)
pd.set_option('display.max_columns', None)


# In[3]:


df[2:3]


# 1、把总文件里面没有的forum_content_order合并起来
# 

# In[42]:


#df=df.rename(columns={'Unnamed: 0':'forum_com_content_order'})


# In[4]:


df=df.drop('Unnamed: 0',axis=1,inplace=False)


# In[5]:


dforder=pd.read_excel(r'forum_content_order.xlsx',encoding='utf-8')
c=pd.merge(df,dforder,how='outer',right_index=True,left_index=True)


# In[6]:


len(c)


# In[9]:


c=c.drop(['forum_com_user_y','forum_com_time_y'],axis=1)
c=c.rename(columns={'forum_com_user_x':'forum_com_user'})
c=c.rename(columns={'forum_com_time_x':'forum_com_time'})
df=c


# In[10]:


df[1200:1202]


# 2、重整列顺序

# In[11]:


order=['forum_com_content_order', 'forum_com_user', 'forum_com_time',
       'forum_com_content', 'forum_com_repo_num', 'forum_com_repo', 'website',
       'platform', 'forum_title', 'forum_time', 'forum_vol', 'forum_com_num',
       'forum_type', 'forum_article']
df=df[order]


# In[12]:


df['index_0']=df.index
df['forum_repo_order']=1
df.insert(7,'forum_com_repo_content',df.forum_com_repo)


# In[13]:


df[2:3]


# 3、把第一层评论的内容细分：把第一层评论跟评的time\id\原始content，评论的real content细分。Forum_com_content保留原始的格式，便于后面新的处理需要。
# 

# In[14]:


df.insert(4,'forum_com_content_ori_time','')
df.insert(5,'forum_com_content_ori_ID','')
df.insert(6,'forum_com_content_ori_content','')
df.insert(7,'forum_com_real_content','')


# In[15]:


for i in range(len(df)):
    a=str(df['forum_com_content'].values[i])
    if ('编辑' in a)==True:
        a=a.split('编辑')[1]
    try:
        if ('发表于' in a)==True:
            df['forum_com_content_ori_time'].values[i]=a.split('发表于')[1][:17]
            b=a.split('发表于')[0]
            b.replace(' ','')
            df['forum_com_content_ori_ID'].values[i]=re.sub('\r\n','',b)
            df['forum_com_content_ori_content'].values[i]=re.sub('\r\n','',a.split('发表于')[1].split('\r\n')[1])
            df['forum_com_real_content'].values[i]=re.sub('\r\n','',a.split('发表于')[1].split('\r\n')[2])

        else:
            df['forum_com_real_content'].values[i]=re.sub('\r\n','',a)
    except IndexError:
        continue


# In[19]:


df[2562:2569]


# 3、第二层：第一层评论的回复分成好几行

# In[20]:


df1=df[:20000]
df2=df[20000:40000]
df3=df[40000:60000]
df4=df[60000:80000]
df5=df[80000:100000]
df6=df[100000:120000]
df7=df[120000:140000]
df8=df[140000:160000]
df9=df[160000:]


# In[21]:


for i in range(len(df1)):
        a=str(df1['forum_com_repo_content'].values[i])
        a=re.sub('\r\n','',a)
        a.replace(' ','')
        
        if a=='我也说两句...;#;发表':
            df1['forum_repo_order'].values[i]=0
            
        a=re.sub('回复;#;我也说两句...;#;发表','',a)
        a=re.sub('我也说两句...;#;发表','',a)
        
        s=a.split('回复;#;')
        df1['forum_com_repo_content'].values[i]=s[0]
    
        
        for j in range(1,len(s)):
            new=df1[i:i+1]
            df1=df1.append(new,ignore_index=True)
            df1['forum_com_repo_content'].values[-1:]=s[j]
            df1['forum_repo_order'].values[-1:]=j+1
        


# In[24]:


df1[df1.index_0==2]


# In[25]:


for i in range(len(df2)):
        a=str(df2['forum_com_repo_content'].values[i])
        a=re.sub('\r\n','',a)
        a.replace(' ','')
        
        if a=='我也说两句...;#;发表':
            df2['forum_repo_order'].values[i]=0
            
        a=re.sub('回复;#;我也说两句...;#;发表','',a)
        a=re.sub('我也说两句...;#;发表','',a)
        
        s=a.split('回复;#;')
        df2['forum_com_repo_content'].values[i]=s[0]
    
        
        for j in range(1,len(s)):
            new=df2[i:i+1]
            df2=df2.append(new,ignore_index=True)
            df2['forum_com_repo_content'].values[-1:]=s[j]
            df2['forum_repo_order'].values[-1:]=j+1


# In[26]:


for i in range(len(df3)):
        a=str(df3['forum_com_repo_content'].values[i])
        a=re.sub('\r\n','',a)
        a.replace(' ','')
        
        if a=='我也说两句...;#;发表':
            df3['forum_repo_order'].values[i]=0
            
        a=re.sub('回复;#;我也说两句...;#;发表','',a)
        a=re.sub('我也说两句...;#;发表','',a)
        
        s=a.split('回复;#;')
        df3['forum_com_repo_content'].values[i]=s[0]
    
        
        for j in range(1,len(s)):
            new=df3[i:i+1]
            df3=df3.append(new,ignore_index=True)
            df3['forum_com_repo_content'].values[-1:]=s[j]
            df3['forum_repo_order'].values[-1:]=j+1
        


# In[27]:


for i in range(len(df4)):
        a=str(df4['forum_com_repo_content'].values[i])
        a=re.sub('\r\n','',a)
        a.replace(' ','')
        
        if a=='我也说两句...;#;发表':
            df4['forum_repo_order'].values[i]=0
            
        a=re.sub('回复;#;我也说两句...;#;发表','',a)
        a=re.sub('我也说两句...;#;发表','',a)
        
        s=a.split('回复;#;')
        df4['forum_com_repo_content'].values[i]=s[0]
    
        
        for j in range(1,len(s)):
            new=df4[i:i+1]
            df4=df4.append(new,ignore_index=True)
            df4['forum_com_repo_content'].values[-1:]=s[j]
            df4['forum_repo_order'].values[-1:]=j+1      


# In[28]:


for i in range(len(df5)):
        a=str(df5['forum_com_repo_content'].values[i])
        a=re.sub('\r\n','',a)
        a.replace(' ','')
        
        if a=='我也说两句...;#;发表':
            df5['forum_repo_order'].values[i]=0
            
        a=re.sub('回复;#;我也说两句...;#;发表','',a)
        a=re.sub('我也说两句...;#;发表','',a)
        
        s=a.split('回复;#;')
        df5['forum_com_repo_content'].values[i]=s[0]
    
        
        for j in range(1,len(s)):
            new=df5[i:i+1]
            df5=df5.append(new,ignore_index=True)
            df5['forum_com_repo_content'].values[-1:]=s[j]
            df5['forum_repo_order'].values[-1:]=j+1


# In[29]:


for i in range(len(df6)):
        a=str(df6['forum_com_repo_content'].values[i])
        a=re.sub('\r\n','',a)
        a.replace(' ','')
        
        if a=='我也说两句...;#;发表':
            df6['forum_repo_order'].values[i]=0
            
        a=re.sub('回复;#;我也说两句...;#;发表','',a)
        a=re.sub('我也说两句...;#;发表','',a)
        
        s=a.split('回复;#;')
        df6['forum_com_repo_content'].values[i]=s[0]
    
        
        for j in range(1,len(s)):
            new=df6[i:i+1]
            df6=df6.append(new,ignore_index=True)
            df6['forum_com_repo_content'].values[-1:]=s[j]
            df6['forum_repo_order'].values[-1:]=j+1


# In[30]:


for i in range(len(df7)):
        a=str(df7['forum_com_repo_content'].values[i])
        a=re.sub('\r\n','',a)
        a.replace(' ','')
        
        if a=='我也说两句...;#;发表':
            df7['forum_repo_order'].values[i]=0
            
        a=re.sub('回复;#;我也说两句...;#;发表','',a)
        a=re.sub('我也说两句...;#;发表','',a)
        
        s=a.split('回复;#;')
        df7['forum_com_repo_content'].values[i]=s[0]
    
        
        for j in range(1,len(s)):
            new=df7[i:i+1]
            df7=df7.append(new,ignore_index=True)
            df7['forum_com_repo_content'].values[-1:]=s[j]
            df7['forum_repo_order'].values[-1:]=j+1


# In[31]:


for i in range(len(df8)):
        a=str(df8['forum_com_repo_content'].values[i])
        a=re.sub('\r\n','',a)
        a.replace(' ','')
        
        if a=='我也说两句...;#;发表':
            df8['forum_repo_order'].values[i]=0
            
        a=re.sub('回复;#;我也说两句...;#;发表','',a)
        a=re.sub('我也说两句...;#;发表','',a)
        
        s=a.split('回复;#;')
        df8['forum_com_repo_content'].values[i]=s[0]
    
        
        for j in range(1,len(s)):
            new=df8[i:i+1]
            df8=df8.append(new,ignore_index=True)
            df8['forum_com_repo_content'].values[-1:]=s[j]
            df8['forum_repo_order'].values[-1:]=j+1


# In[32]:


for i in range(len(df9)):
        a=str(df9['forum_com_repo_content'].values[i])
        a=re.sub('\r\n','',a)
        a.replace(' ','')
        
        if a=='我也说两句...;#;发表':
            df9['forum_repo_order'].values[i]=0
            
        a=re.sub('回复;#;我也说两句...;#;发表','',a)
        a=re.sub('我也说两句...;#;发表','',a)
        
        s=a.split('回复;#;')
        df9['forum_com_repo_content'].values[i]=s[0]
    
        
        for j in range(1,len(s)):
            new=df9[i:i+1]
            df9=df9.append(new,ignore_index=True)
            df9['forum_com_repo_content'].values[-1:]=s[j]
            df9['forum_repo_order'].values[-1:]=j+1


# In[33]:


df = pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9], axis = 0,ignore_index = True)


# In[66]:


len(df9)


# In[ ]:


#for i in range(len(df)):
        a=str(df['forum_com_repo_content'].values[i])
        a=re.sub('\r\n','',a)
        a.replace(' ','')
        
        if a=='我也说两句...;#;发表':
            df['forum_repo_order'].values[i]=0
            
        a=re.sub('回复;#;我也说两句...;#;发表','',a)
        a=re.sub('我也说两句...;#;发表','',a)
        
        s=a.split('回复;#;')
        df['forum_com_repo_content'].values[i]=s[0]
    
        
        for j in range(1,len(s)):
            new=df[i:i+1]
            df=df.append(new,ignore_index=True)
            df['forum_com_repo_content'].values[-1:]=s[j]
            df['forum_repo_order'].values[-1:]=j+1
        


# In[80]:


df[df.index_0==100]


# In[34]:


df=df.sort_values(by=['index_0','forum_repo_order'])


# In[35]:


len(df)


# In[38]:


df[15000:15030]


# 5、第二层：第一层评论的回复
# 细分为回复的time\id\content
# 如果有回复的回复：取出被回复的id (forum_com_re_repo_ID)
# 对于原始的forum_com_repo, 这里的换行符对于分割不太需要，为了便于分割就去掉了，我也说两句之类的也去掉了
# 

# In[39]:


df.insert(10,'forum_com_repo_time','')
df.insert(11,'forum_com_repo_ID','')
df.insert(12,'forum_com_re_repo_ID','')


# In[40]:


for i in range(len(df)):
    a=str(df['forum_com_repo_content'].values[i])
    a=re.sub('\xa0','',a)
    a=re.sub(' ','',a)
    if a!='':
        df['forum_com_repo_time'].values[i]=a[-15:]
        df['forum_com_repo_ID'].values[i]=a.split(':')[0]
        try:
            if ('回复' in a)==True: 
                df['forum_com_re_repo_ID'].values[i]=a.split('回复')[1].split(':')[0]
                df['forum_com_repo_content'].values[i]=a[:-15].split('回复')[1].split(':')[1]
            else:
                df['forum_com_repo_content'].values[i]=a[:-15].split(':')[1]
        except IndexError:
            continue


# In[41]:


df[16000:16030]


# 6、其他

# In[44]:


for i in range(len(df)):
        b=str(df['forum_com_repo'].values[i])
        b=re.sub('\r\n','',b)
        b=re.sub('回复;#;我也说两句...;#;发表','',b)
        b=re.sub('我也说两句...;#;发表','',b)
        df['forum_com_repo'].values[i]=b
        
        c=str(df['forum_article'].values[i])
        c=re.sub('\r\n','',c)
        df['forum_article'].values[i]=c
        
        df['forum_repo_order'].values[i]-=1


# In[49]:


df[170000:170070]


# 7、重新调一下顺序

# In[47]:


df.columns


# In[50]:


df=df.rename(columns={'forum_com_content_order':'forum_com_order'})


# In[53]:


order=['index_0',
       'forum_type','forum_title','forum_time', 'forum_vol','platform','website','forum_article', 
       'forum_com_num','forum_com_order', 'forum_com_user', 'forum_com_time','forum_com_content',
       'forum_com_content_ori_time', 'forum_com_content_ori_ID', 'forum_com_content_ori_content', 'forum_com_real_content',
       'forum_com_repo_num', 'forum_repo_order', 'forum_com_repo','forum_com_repo_time', 'forum_com_repo_ID', 'forum_com_re_repo_ID','forum_com_repo_content']
df=df[order]


# In[57]:


for i in range(len(df)):
    df['forum_com_repo_num'].values[i]-=2


# In[58]:


df[2:5]


# In[62]:


df['forum_com_repo_num'].unique()


# In[66]:


df[df['forum_com_repo_num']>=5]


# In[67]:


len(df)


# In[59]:


df.to_excel('forum_deal1.xlsx',encoding='utf-8')


# In[60]:


df.to_csv('forum_deal1.csv',encoding='utf-8')


# 8、打开文件，忽视缺失值

# In[ ]:


dff=pd.read_csv('forum_deal1.csv',encoding='utf-8', keep_default_na=False)


# 9、下面是无关的代码

# In[93]:


dforder=pd.read_excel(r'forum_content_order.xlsx',encoding='utf-8')


# In[88]:


dforder[1400:1402]


# In[107]:


len(dforder)


# In[108]:


df=df.drop('forum_com_content_order',axis=1,inplace=False)


# In[131]:



c=pd.merge(df,dforder,how='outer',right_index=True,left_index=True)


# In[132]:


len(c)


# In[133]:


c[4000:4001]


# In[134]:


c_id = c.forum_com_content_order
c =c.drop('forum_com_content_order',axis=1)
c.insert(0,'forum_com_content_order',c_id)


# In[136]:


c=c.drop(['forum_com_user_y','forum_com_time_y'],axis=1)


# In[137]:


c[40000:40001]


# In[138]:


df=c


# In[61]:


df[170000:170030]


# In[86]:


for i in range(len(df)):
    if (df.forum_com_user.values[i]==dforder.forum_com_user.values[i]) and (df.forum_com_time.values[i]==dforder.forum_com_time.values[i]):
        df.forum_com_content_order.values[i]=dforder.forum_com_content_order.values[i]


# In[92]:


help(pd.merge)


# In[140]:


df2[2:3]

