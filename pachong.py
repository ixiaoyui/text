﻿#-*- coding: utf-8 -*-
import re
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import pandas
import os
import threading
from IPython.utils.path import link

liebiao = []
huizong = []


#def hqlianjie():#取得新闻链接
    #res2 = requests.get('http://www.sdjtu.edu.cn/channels/ch01410/')
    #res2.encoding = 'utf=8'
    #soup2 = BeautifulSoup(res2.text,'html.parser')
    #lianjie = []
    #for new in soup2.select('.pagedContent'):
        #lianjie.append(new.select('a')[0]['href'])
    #return lianjie

def yuedushuhq(newsurl):#获取新闻阅读数
    
    res3 = requests.get(newsurl)
    res3.encoding = 'utf=8'
    soup3 = BeautifulSoup(res3.text,'html.parser')
    fangwenshulink = soup3.select('script')[-5].text#取得含有阅读数id的链接
    urlmuban = 'http://www.sdjtu.edu.cn/InterFront/embedservice/count.shtml?method=count&articleId={}&channelId=b395b5bd-91b3-42fc-b8ce-19e06703e915&siteId=12590635-85fe-408e-ad99-c812962f0fa2'
    m = re.search('articleId=(.+)&channelId',fangwenshulink)#取得新闻阅读数id
    plurl = urlmuban.format(m[1])#组成获取阅读数的链接
    json2 = requests.get(plurl)

    yuedu = json.loads(json2.text)
    yuedushu= str(yuedu['result']).lstrip('[').rstrip(']')#取得阅读数
    return yuedushu

def liebiaolink():#取得新闻链接
    res2 = requests.get('http://www.sdjtu.edu.cn/channels/ch01410/')
    res2.encoding = 'utf=8'
    soup2 = BeautifulSoup(res2.text,'html.parser')
    #for news in soup.select
    
    #news = soup2.select('.pagedContent')
    for new in soup2.select('.pagedContent'):
        xwlianjie = new.select('a')[0]['href']
        liebiao.append(xwlianjie)
        #liebiao['lianjie'] = 
    print('我执行了一次！')    
    return liebiao

jishu = 0
    
def neirong(args):#获取新闻内容
    global jishu
    global huizong
    #print(jishu)  
    jieguo = {}
    #liebiao = {}
   
    try:
        jieguo = {}
            #liebiao = {}
        res = requests.get(args)
        res.encoding = 'utf=8'
        soup = BeautifulSoup(res.text,'html.parser')
        duanluo = (soup.select('#content p'))
        ceshi = len(soup.select('#content p'))
        #print(ceshi)
        
        if ceshi > 1:
            
            n = 0
            jieguotext = ''
            for pp in duanluo:
                ppp = re.search('(src=")(.+)"',str(pp))
                if ppp:
                    #print(ppp[2])
                    tplink = 'http://www.sdjtu.edu.cn' + ppp[2]
                    print(tplink)
                    mulu1 = 'D:\\workspace\\123\\12\\pachong2\\'
                    #mulu1 = ('D:\\workspace\\123\\12\\pachong\\' + str(jishu))
                    #if os.path.exists(mulu1) == False:#判断存放图片的文件夹是否存在
                        #os.makedirs(mulu1)
                        #print('创建文件夹' + str(jishu))
                    #newmulu = os.path.join('D:\\workspace\\123\\12',str(jishu))
                    tpwenjian = open(os.path.join(mulu1,os.path.basename(ppp[2])),'wb')
                    #print(tplink)
                    tpdata = requests.get(tplink)
                    for data in tpdata.iter_content(100000):#保存图片
                        tpwenjian.write(data)
                    tpwenjian.close()
                    n = n + 1
                    #jishu = jishu + 1
                    #print(n)
                else:
                    jieguo = {'neirong':''}
                    #jieguo2 = {}
                    
                    duanluo1 = str(soup.select('#content p')[n].text.replace('\xa0',''))
                    #print(duanluo1)
                    if len(duanluo1) > 0:
                        jieguotext = jieguotext + duanluo1
                        #print(jieguotext)
                        n = n + 1
                        #jishu = jishu + 1
                    else:
                        n = n + 1
                        #jishu = jishu + 1
            jieguo['neirong'] = jieguotext            
            jieguo['yuedushu'] = yuedushuhq(args)
            shijian = soup.select('div[align="center"]')[2]
            shijian2 = str(shijian)
            m = re.search('    (.+)    ',shijian2)
            jieguo['time'] = m[1]
            jieguo['laiyuan'] = soup.select('a[target="_blank"]' )[-2].text
            jieguo['biaoti'] = soup.select('td[align="center"] p')[0].text
    
        if ceshi == 1:
                jieguo['neirong'] = str(soup.select('#content p')[0].text.replace('\xa0',''))            
                jieguo['yuedushu'] = yuedushuhq(args)
                shijian = soup.select('div[align="center"]')[2]
                shijian2 = str(shijian)
                m = re.search('    (.+)    ',shijian2)
                jieguo['time'] = m[1]
                jieguo['laiyuan'] = soup.select('a[target="_blank"]' )[-2].text
                jieguo['biaoti'] = soup.select('td[align="center"] p')[0].text
    
    except: 
            pass
    #jishu = jishu + 1
    huizong.append(jieguo)
    

lianjie = liebiaolink()
#print(len(lianjie))
#print(lianjie[0])

'''
neirong(lianjie[0])
print(huizong)
'''


xzxc = []
for i in range(0,1900):
    xz1 = threading.Thread(target=neirong(lianjie[i]))
    xzxc.append(xz1)
    xz1.start()
    
for xz1 in xzxc:
    xz1.join()
df = pandas.DataFrame(huizong)
df.to_excel('news88.xlsx')
print('已生成Excel文档！')


