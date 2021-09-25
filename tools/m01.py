#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
from pprint import pprint
import re

quotePat = re.compile(b"<blockquote>.+</blockquote>")

def crawler(urlSTR):
    '''
    依指定 urllSTR 抓取 mobile01 的內容。
    '''

    if urlSTR.startswith("https://www.mobile01.com/topicdetail.php?"):
        resultDICT = {"msg":"", "success":None}
    else:
        return {"msg": "網址不是 mobile01 的討論串！", "succeess":False}

    headers = {'user-agent': 'Mozilla/5.0'}
    if "&p=" in urlSTR: #如果發現是第 2 頁以後的 url，則要回到第 1 頁去取得討論串的初始貼文。
        page1 = urlSTR.split("&p=")[0]
        webpage = requests.get(page1, headers=headers)
        page1soup = BeautifulSoup(webpage.content,"html.parser")
        topicArticle = page1soup.find("div", {"itemprop":"articleBody"})
        resultDICT["article"] = topicArticle.get_text().replace("\n", "")
        #取得第 1 頁的初始貼文後，再回到指定的 url 裡取得指定的網頁內容。
        webpage = requests.get(urlSTR, headers=headers)
        soup = BeautifulSoup(webpage.content,"html.parser")
    else: #如果不是第 2 頁以後的 url，則在這一頁裡就能找到討論串的初始貼文了。
        webpage = requests.get(urlSTR, headers=headers)
        soup = BeautifulSoup(webpage.content,"html.parser")
        topicArticle = soup.find("div", {"itemprop":"articleBody"})
        resultDICT["article"] = topicArticle.get_text().replace("\n", "")

    #擷取回覆貼文
    replyLIST = soup.findAll("article", {"class":"u-gapBottom--max"})
    for r in replyLIST:
        try:
            r.find("blockquote").decompose() #把 quotation 刪掉
            r.find("br").decompose()
        except:
            pass
        resultDICT[r.get('id')] = r.get_text().replace("\n", "")
    resultDICT["success"] = True
    return resultDICT

if __name__ == "__main__":
    urlSTR = "https://www.mobile01.com/topicdetail.php?f=741&t=6458797"
    urlSTR = "https://www.mobile01.com/topicdetail.php?f=741&t=6437324&p=2"
    urlSTR = "https://www.mobile01.com/topicdetail.php?f=741&t=6453454"
    pageContentDICT = crawler(urlSTR)
    pprint(pageContentDICT)
    print(pageContentDICT["article"])