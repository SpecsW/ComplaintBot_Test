#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import os
import platform
import requests
import re

from bs4 import BeautifulSoup
from pprint import pprint
from selenium import webdriver #載入 selenium 這個可以冒充瀏覽器的 BigGun!

quotePat = re.compile(b"<blockquote>.+</blockquote>")

osDICT = {"Linux":"linux",
          "Darwin":"macos",
          "Windows":"windows"}

def fakeBrowser(urlSTR):
    resultDICT = {"msg":"", "success":None}
    browserDIR = "./fake_browsers/{}/chromedriver".format(osDICT[platform.system()])
    if os.path.isfile(browser) == False: #沒有裝 broswer driver
        resultDICT["msg"] = """
        Bot 需要 chromedriver 以便擷取網頁內容，但 chromedriver 並沒有安裝到 bot 裡！
        請到 https://chromedriver.storage.googleapis.com/index.html?path=94.0.4606.41/
        下載相應作業系統的 cromedriver 版本，並解壓縮到 tools/fake_browsers 下相應的作業系統目錄裡"""
        return resultDICT
    else:
        browser = webdriver.Chrome(browserDIR)
        browser.get(urlSTR)
        topicArticle = browser.find_element_by_css_selector("[itemprop='articleBody']")
        resultDICT["article"] = topicArticle.text.replace("\n", "")
        browser.close()
        return resultDICT


def crawler(urlSTR):
    '''
    依指定 urllSTR 抓取 mobile01 的內容。
    如果 request 回傳非 200 的內容，則會改用 selenium 再試一次。
    '''

    if urlSTR.startswith("https://www.mobile01.com/topicdetail.php?"):
        resultDICT = {"msg":"", "success":None}
    elif urlSTR.startswith("https://m.mobile01.com/topicdetail.php?"):
        resultDICT = {"msg":"", "success":None}
    else:
        return {"msg": "網址不是 mobile01 的討論串！", "success":False}

    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36',}
    if "&p=" in urlSTR: #如果發現是第 2 頁以後的 url，則要回到第 1 頁去取得討論串的初始貼文。
        page1 = urlSTR.split("&p=")[0]
        webpage = requests.get(page1, headers=headers)
        if webpage.status_code == requests.status_codes.codes["ok"]:
            page1soup = BeautifulSoup(webpage.content,"html.parser")
            topicArticle = page1soup.find("div", {"itemprop":"articleBody"})
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
        else:
            resultDICT = fakeBrowser(urlSTR)

    else: #如果不是第 2 頁以後的 url，則在這一頁裡就能找到討論串的初始貼文了。
        webpage = requests.get(urlSTR, headers=headers)
        if webpage.status_code == requests.status_codes.codes["ok"]:
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
        else:
            resultDICT = fakeBrowser(urlSTR)




    resultDICT["success"] = True
    return resultDICT

if __name__ == "__main__":
    urlSTR = "https://m.mobile01.com/topicdetail.php?f=741&t=6458797"
    urlSTR = "https://m.mobile01.com/topicdetail.php?f=741&t=6437324&p=2"
    urlSTR = "https://m.mobile01.com/topicdetail.php?f=741&t=6453454"
    pageContentDICT = crawler(urlSTR)
    pprint(pageContentDICT)
    #print(pageContentDICT["article"])