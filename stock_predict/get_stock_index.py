# -*- coding: utf-8 -*-
"""
Created on Wed Dec 19 15:15:35 2018

@author: GRC
"""

import requests
from bs4 import BeautifulSoup
import bs4
import csv
import os


def getHTMLText(url):
    try:
        #账号密码15520452757
        #cookie={'Cookie':'UM_ distinctid= ;PHPSESSID=;CNZZDATA1256448133=; amvid = '}
        
        cookie={'Cookie':'UM_ distinctid= 167d389bc12988-061b3bd552ce1c-4d045769-1fa400-167d389bc13bec;PHPSESSID=3hgnsm2gm1lflj4eajve9abmf0;CNZZDATA1256448133=910336781-1545439520-http%253A%252F%252Fwww.gpdatacat.com%252F%7C1545451867; amvid = 8ae8715d4f2b52a2694e97b76aa06efd'}
        r = requests.get(url, headers=cookie, timeout = 30)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        return r.text
    except:
        return ""

def fillUnivList(ulist, html):
    soup = BeautifulSoup(html,"html.parser")
    #print(soup.text)
    #print(soup.find_all('tbody'))
    #print(soup.find_all(id='alldatatablelg')) #alldatatablelg
    
    table  = soup.find_all(id='alldatatablelg')[0]
    tbody = table.find_all('tbody')[0] 
    for tr in tbody.find_all('tr'):
        if isinstance(tr, bs4.element.Tag):
            tds = tr('td')
            #print(soup.find_all(tr('td')))
            #print(tds)

            ulist.append([tds[0].string, tds[4].string, tds[5].string, tds[6].string,tds[8].string, tds[9].string, tds[10].string, tds[11].string])

def printUnivList(ulist, stockcode, num):
    #tplt = "{0}\t{1}\t{2}\t{3}\t{4}\t{5}\t{6}\t{7}"
    #时间 综合 强度 资金 预期 转强 长预 近资 风险
    #print("时间   综合    强度     资金    转强    长预     近资    风险")
    shares = []   
    parent_dir = os.path.dirname(__file__)  # 父目录
    file_dir = os.path.join(parent_dir,"stock_index/")
    
    with open(os.path.join(file_dir,stockcode+'.csv'), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                            quotechar='\n', quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['ri_qi', 'zong_he', 'qiang_du', 'zi_jin', 'zhuan_qiang', 'chang_yu', 'jin_zi', 'feng_xian'])
        for i in range(num):
            u=ulist[i]
            #print(tplt.format(u[0], u[1], u[2], u[3], u[4], u[5], u[6], u[7]))
            dict = {'ri_qi': u[0], 'zong_he': u[1], 'qiang_du': u[2], 'zi_jin': u[3], 'zhuan_qiang': u[4], 'chang_yu': u[5], 'jin_zi': u[6], 'feng_xian': u[7]} 
            shares.append(dict)
            spamwriter.writerow(u)
    
    
def main(stockcode):
    uinfo = []
    url = 'http://www.gpdatacat.com/index.php?r=stock%2Fview&stockcode=' + stockcode
    html = getHTMLText(url)
    fillUnivList(uinfo, html)
    printUnivList(uinfo, stockcode, 10)  #10个日期，最大取值为50
    
main('000063')#中兴通讯
main('000066')#中国长城
main('000651')#格力电器
main('000768')#中航飞机
main('600320')#振华重工
main('600718')#东软集团
main('600839')#四川长虹
main('601390')#中国中铁
main('601766')#中国中车
main('601988')#中国银行
        
# =============================================================================
# def main():
#     uinfo = []
#     url = 'http://www.gpdatacat.com/index.php?r=stock%2Fview&stockcode=000063'
#     html = getHTMLText(url)
#     fillUnivList(uinfo, html)
#     printUnivList(uinfo, 10)  #50个日期
# main()
# =============================================================================