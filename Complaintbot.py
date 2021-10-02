#!/usr/bin/env python
# -*- coding:utf-8 -*-

import discord
import json
import math
import re

from battery_or_charge_func import battery_or_charge
from ComplaintBot_1_updated.Complaint_Loki_NLU import runLoki
from tools.m01 import crawler

from ArticutAPI import Articut

with open("account.info.json", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
articut = Articut(username=accountDICT["username"], apikey=accountDICT["apikey"])

def wordExtractor(inputLIST, unify=True):
    '''
    配合 Articut() 的 .getNounStemLIST() 和 .getVerbStemLIST() …等功能，拋棄位置資訊，只抽出詞彙。
    '''
    resultLIST = []
    for i in inputLIST:
        if i == []:
            pass
        else:
            for e in i:
                resultLIST.append(e[-1])
        if unify == True:
            return sorted(list(set(resultLIST)))
        else:
            return sorted(resultLIST)

def counterCosineSimilarity(counter01, counter02):
    '''
    計算 counter01 和 counter02 兩者的餘弦相似度
    '''
    terms = set(counter01).union(counter02)
    dotprod = sum(counter01.get(k, 0) * counter02.get(k, 0) for k in terms)
    magA = math.sqrt(sum(counter01.get(k, 0)**2 for k in terms))
    magB = math.sqrt(sum(counter02.get(k, 0)**2 for k in terms))
    return dotprod / (magA * magB)

def getLokiResult(inputSTR):
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")
    filterLIST = []
    resultDICT = {"on_battery":0, "on_charging":0}
    for i in range(0, len(inputLIST), 20):
        tmpDICT = runLoki(inputLIST[i:i+20], filterLIST)
        if "on_battery" in tmpDICT.keys():
            resultDICT["on_battery"] = resultDICT["on_battery"] + tmpDICT["on_battery"]
        if "on_charging" in tmpDICT.keys():
            resultDICT["on_charging"] = resultDICT["on_charging"] + tmpDICT["on_charging"]
    print("Loki Result => {}".format(resultDICT))
    return resultDICT

class BotClient(discord.Client):
    async def on_ready(self):
        print('Logged on as {} with id {}'.format(self.user, self.user.id))

    async def on_message(self, message):
        # Don't respond to bot itself. Or it would create a non-stop loop.
        # 如果訊息來自 bot 自己，就不要處理，直接回覆 None。不然會 Bot 會自問自答個不停。
        if message.author == self.user:
            return None

        print("到到來自 {} 的訊息".format(message.author))
        print("訊息內容是 {}。".format(message.content))
        if self.user.mentioned_in(message):
            print("本 bot 被叫到了！")
            msg = message.content.replace("<@!{}> ".format(self.user.id), "")

            if msg.startswith("https://www.mobile01.com/topicdetail.php?"):
                postDICT = crawler(msg)
                if postDICT["success"] == True:
                    msg = postDICT["article"]
                    await message.reply("將解析：\n{}".format(msg))
                else:
                    responseSTR = "網頁內容爬取失敗。你確定那是一個 mobile01.com 的討論串網址嗎？"
                    await message.reply(responseSTR)

            if msg == 'ping':
                await message.reply('pong')
            elif msg == "<@!{}>".format(self.user.id):
                await message.reply('您好，請輸入您的問題')
            elif msg == 'ping ping':
                await message.reply('pong pong')
            else:
                #從這裡開始接上 NLU 模型
                responseSTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"

                final_decision = battery_or_charge(msg)
                if final_decision == "battery":
                    complaint_type = "電池"
                elif final_decision == "charge":
                    complaint_type = "充電"
                else:
                    complaint_type = "未知"
                await message.reply("文本主要像是在討論「{}」問題".format(complaint_type))

                resultDICT = getLokiResult(msg)
                total = resultDICT["on_battery"] + resultDICT["on_charging"]


                if total != 0:
                    if complaint_type != "未知":
                        battery_percentage = resultDICT["on_battery"] / total * 100
                        charge_percentage = resultDICT["on_charging"] / total * 100
                        responseSTR = "謝謝您提出對Tesla相關問題的寶貴意見，本公司會做為改進參考。\n問題積分：{};\n 相關比例：電池{}%, 充電{}%".format(complaint_type, str(battery_percentage), str(charge_percentage))
                    else:
                        responseSTR = "未知的討論主題類型 (Sorry, 我現在只對電池和充電議題比較熟悉！)"
                else:
                    responseSTR = "抱歉，我會的句型太少，所以沒搞懂這篇文章在抱怨的重點 :c"

                await message.reply(responseSTR)

if __name__ == "__main__":
    client = BotClient()
    client.run(accountDICT["discord_token"])