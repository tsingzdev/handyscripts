#!/usr/local/bin/python3
from bs4 import BeautifulSoup
import re
import time
import requests

headers0 = {'User-Agent':"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.62 Safari/537.36"}

def BWappend(BWdict,Items):
    for i in range(len(Items)):
        try:
            title=Items[i](href=re.compile('subject'))[0].get_text(strip=True)
            intro=Items[i](class_='intro')[0].get_text(strip=True).split('/')
            author=intro[0]
            publisher=intro[-3]
            translater='/'.join(intro[1:-3])
            BWdict[title]=[author,translater,publisher]
        except:
            try:
                title=Items[i](href=re.compile('subject'))[0].get_text(strip=True)
                intro=Items[i](class_='intro')[0].get_text(strip=True).split(';')
                author=intro[0]
                publisher=intro[-1]
                translater='/'.join(intro[1:-1])
                BWdict[title]=[author,translater,publisher]
            except:
                BWdict[title]=['格式过于诡异','nah','nah']

def bookwish(doubanid):
    firstpage='https://book.douban.com/people/'+doubanid+'/wish?sort=time&start=0&filter=all&mode=list&tags_sort=count'
    sess = requests.Session()
    sess.headers.update(headers0)
    request=sess.get(firstpage)
    soup=BeautifulSoup(request.text,'html.parser')
    page=1
    print(f'第{page}页',request.reason)
    bookwishdict={}
    items=soup.find_all(class_='item')
    BWappend(BWdict=bookwishdict,Items=items)
    while 1:
        try:
            Nextpage='https://book.douban.com'+soup.find(class_='next').link.get('href')
        except:
            print('已到最终页')
            break
        else:
            request=sess.get(Nextpage)
            soup=BeautifulSoup(request.text,'html.parser')
            page+=1
            print(f'第{page}页',request.reason)
            items2=soup.find_all(class_='item')
            BWappend(BWdict=bookwishdict,Items=items2)
            time.sleep(1)
    fw=open(doubanid+'_TOread_List.csv','w',encoding='utf-8_sig')
    fw.write('书名,作者,译者,出版社\n')
    for title in bookwishdict.keys():
        fw.write(title.replace(',','、').replace('，','、')+','+bookwishdict[title][0]+\
                 ','+bookwishdict[title][1]+','+bookwishdict[title][2].replace(',','、').replace('，','、')+'\n')
    fw.close()

def BRappend(BRdict,Items):
    for i in range(len(Items)):
        title=Items[i]('a')[0].get_text(strip=True)
        date=Items[i](class_=re.compile('date'))[0].get_text(strip=True)
        try:
            intro=Items[i](class_=re.compile('intro'))[0].get_text(strip=True).split('/')
            author=intro[0]
            publisher=intro[-3]
            translater='/'.join(intro[1:-3])
        except:
            try:
                intro=Items[i](class_=re.compile('intro'))[0].get_text(strip=True).replace(';','/').split('/')
                author=intro[0]
                publisher=intro[-1]
                translater='/'.join(intro[1:-1])
            except:
                intro='格式过于诡异'
                author='nah'
                publisher='nah'
                translater='nah'
        try:
            comment=Items[i](class_=re.compile('comm'))[0].get_text(strip=True).replace('\n','-')
        except:
            comment='Nah'
        try:
            stars=Items[i](class_=re.compile('rat'))[0]['class'][0][6]
        except:
            stars='Nah'
        BRdict[title]=[author,translater,publisher,stars,date,comment]

def ReadBookList(doubanid):
    mainpage='https://book.douban.com/people/'+doubanid
    firstpage='https://book.douban.com/people/'+doubanid+'/collect?sort=time&start=0&filter=all&mode=list&tags_sort=count'
    s=requests.Session()
    s.headers.update(headers0)
    s.get(mainpage)
    res2=s.get(firstpage)
    soup=BeautifulSoup(res2.text,"html.parser")
    items=soup.find_all(class_=re.compile('item'),id=re.compile('li'))
    read_book={}
    BRappend(BRdict=read_book,Items=items)
    page=1
    print(f"第{page}页",res2.reason)
    while 1:
        time.sleep(2)
        try:
            NextPage='https://book.douban.com'+soup.find(class_='next').link.get('href')
        except:
            print('已到最终页')
            break
        else:
            res=s.get(NextPage)
            soup=BeautifulSoup(res.text,"html.parser")
            items=soup.find_all(class_=re.compile('item'),id=re.compile('li'))
            page+=1
            print(f"第{page}页",res.reason)
            BRappend(BRdict=read_book,Items=items)
    fw=open(doubanid+'_READ_List.csv','w',encoding='utf-8_sig')
    fw.write('书名,作者,译者,出版社,评分,日期,短评\n')
    for title in read_book.keys():
        fw.write(title.replace(',','、').replace('，','、')+','+read_book[title][0]+\
                 ','+read_book[title][1]+','+read_book[title][2].replace(',','、').replace('，','、')+\
                 ','+read_book[title][3]+','+read_book[title][4]+','+read_book[title][5].replace(',','、').replace('，','、')+'\n')
    fw.close()
    return read_book


def main():
    print('注意：本脚本将会爬取已读list')
    choice=input('请确定你要运行此脚本(yes/no):')
    if choice=='yes':
        douid=input('请输入想备份的豆瓣id：')
        print('开始备份-想读-列表')
        bookwish(doubanid=douid)
        time.sleep(2)
        print('开始备份-已读-列表')
        ReadBookList(doubanid=douid)
        print('程序结束，文件已存在该exe目录中')
        input('按任意键退出')
    else:
        print('bye')

main()
