#!/usr/bin/env python
# -*- coding:utf-8 -*-

import discord
import json

from ComplaintBot_1_updated.Complaint_Loki_NLU import runLoki

from ArticutAPI import Articut
with open("account_info_articut.json", encoding="utf-8") as f:
    userinfoDICT = json.loads(f.read())
articut = Articut(username=userinfoDICT["username"], apikey=userinfoDICT["apikey"])

with open("account.info.json", encoding="utf-8") as f:
    accountDICT = json.loads(f.read())
    
from collections import Counter
from ArticutAPI import Articut
from battery_or_charge_func import battery_or_charge
import json
import math
    
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
    
    
def lengthSimilarity(counter01, counter02):
    '''
    計算 counter01 和 counter02 兩者在長度上的相似度
    '''
    
    lenc1 = sum(iter(counter01.values()))
    lenc2 = sum(iter(counter02.values()))
    return min(lenc1, lenc2) / float(max(lenc1, lenc2))

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
            if msg == 'ping':
                await message.reply('pong')
            elif msg == "<@!{}>".format(self.user.id):
                await message.reply('您好，請輸入您的問題')
            elif msg == 'ping ping':
                await message.reply('pong pong')
            else:
                #從這裡開始接上 NLU 模型
                responseSTR = "我是預設的回應字串…你會看到我這串字，肯定是出了什麼錯！"
                inputLIST = [msg]
                filterLIST = []
                resultDICT = runLoki(inputLIST, filterLIST)
                print("Result => {}".format(resultDICT))
                
                final_decision = battery_or_charge(msg)
                
                if final_decision == "battery":
                    complaint_type = "電池"
                elif final_decision == "charge":
                    complaint_type = "充電"
                else:
                    complaint_type = "無法辨識"
                
                total = resultDICT["on_battery"] + resultDICT["on_charging"]
                
                if total != 0:
                    battery_percentage = resultDICT["on_battery"] / total * 100
                    charge_percentage = resultDICT["on_charging"] / total * 100
                    responseSTR = "謝謝您提出對Tesla相關問題的寶貴意見，本公司會做為改進參考。問題種類：{} ; 相關比例：電池{}, 充電{}".format(complaint_type, str(battery_percentage) + "%", str(charge_percentage) + "%" )
                else:
                    responseSTR = "抱歉，我好像沒看懂 :c"
                
                await message.reply(responseSTR)

if __name__ == "__main__":
    client = BotClient()
    client.run(accountDICT["discord_token"])