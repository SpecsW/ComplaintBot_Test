#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki 2.0 Template For Python3

    [URL] https://api.droidtown.co/Loki/BulkAPI/

    Request:
        {
            "username": "your_username",
            "input_list": ["your_input_1", "your_input_2"],
            "loki_key": "your_loki_key",
            "filter_list": ["intent_filter_list"] # optional
        }

    Response:
        {
            "status": True,
            "msg": "Success!",
            "version": "v223",
            "word_count_balance": 2000,
            "result_list": [
                {
                    "status": True,
                    "msg": "Success!",
                    "results": [
                        {
                            "intent": "intentName",
                            "pattern": "matchPattern",
                            "utterance": "matchUtterance",
                            "argument": ["arg1", "arg2", ... "argN"]
                        },
                        ...
                    ]
                },
                {
                    "status": False,
                    "msg": "No Match Intent!"
                }
            ]
        }
"""

import json
import math
import re
from requests import post
from requests import codes

try:
    from intent import Loki_charge
    from intent import Loki_battery
except:
    from .intent import Loki_charge
    from .intent import Loki_battery

try:
    with open("account.info", encoding="utf-8") as f:
        accountDICT = json.loads(f.read())
    #單獨測試這個檔案時，試試看 account.info 是不是擺在本檔案的旁邊？
except:
    with open("../account.info", encoding="utf-8") as f:
        accountDICT = json.loads(f.read())
    #如果本檔案的旁邊沒有 account.info，就再試著往上一層目錄 (../) 去找看看有沒有 account.info 這個檔。

LOKI_URL = "https://api.droidtown.co/Loki/BulkAPI/"
USERNAME = accountDICT["username"]
LOKI_KEY = accountDICT["loki_key"]
# 意圖過濾器說明
# INTENT_FILTER = []        => 比對全部的意圖 (預設)
# INTENT_FILTER = [intentN] => 僅比對 INTENT_FILTER 內的意圖
INTENT_FILTER = []

class LokiResult():
    status = False
    message = ""
    version = ""
    balance = -1
    lokiResultLIST = []

    def __init__(self, inputLIST, filterLIST):
        self.status = False
        self.message = ""
        self.version = ""
        self.balance = -1
        self.lokiResultLIST = []
        # filterLIST 空的就採用預設的 INTENT_FILTER
        if filterLIST == []:
            filterLIST = INTENT_FILTER

        try:
            result = post(LOKI_URL, json={
                "username": USERNAME,
                "input_list": inputLIST,
                "loki_key": LOKI_KEY,
                "filter_list": filterLIST
            })

            if result.status_code == codes.ok:
                result = result.json()
                self.status = result["status"]
                self.message = result["msg"]
                if result["status"]:
                    self.version = result["version"]
                    self.balance = result["word_count_balance"]
                    self.lokiResultLIST = result["result_list"]
            else:
                self.message = "Connect failed."
        except Exception as e:
            self.message = str(e)

    def getStatus(self):
        return self.status

    def getMessage(self):
        return self.message

    def getVersion(self):
        return self.version

    def getBalance(self):
        return self.balance

    def getLokiStatus(self, index):
        rst = False
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["status"]
        return rst

    def getLokiMessage(self, index):
        rst = ""
        if index < len(self.lokiResultLIST):
            rst = self.lokiResultLIST[index]["msg"]
        return rst

    def getLokiLen(self, index):
        rst = 0
        if index < len(self.lokiResultLIST):
            if self.lokiResultLIST[index]["status"]:
                rst = len(self.lokiResultLIST[index]["results"])
        return rst

    def getLokiResult(self, index, resultIndex):
        lokiResultDICT = None
        if resultIndex < self.getLokiLen(index):
            lokiResultDICT = self.lokiResultLIST[index]["results"][resultIndex]
        return lokiResultDICT

    def getIntent(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["intent"]
        return rst

    def getPattern(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["pattern"]
        return rst

    def getUtterance(self, index, resultIndex):
        rst = ""
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["utterance"]
        return rst

    def getArgs(self, index, resultIndex):
        rst = []
        lokiResultDICT = self.getLokiResult(index, resultIndex)
        if lokiResultDICT:
            rst = lokiResultDICT["argument"]
        return rst

def runLoki(inputLIST, filterLIST=[]):
    resultDICT = {"on_charging":0, "on_battery":0}
    lokiRst = LokiResult(inputLIST, filterLIST)
    if lokiRst.getStatus():
        for index, key in enumerate(inputLIST):
            for resultIndex in range(0, lokiRst.getLokiLen(index)):
                # charge
                if lokiRst.getIntent(index, resultIndex) == "charge":
                    resultDICT = Loki_charge.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

                # battery
                if lokiRst.getIntent(index, resultIndex) == "battery":
                    resultDICT = Loki_battery.getResult(key, lokiRst.getUtterance(index, resultIndex), lokiRst.getArgs(index, resultIndex), resultDICT)

    else:
        resultDICT = {"msg": lokiRst.getMessage()}
    return resultDICT

def testLoki(inputLIST, filterLIST):
    INPUT_LIMIT = 20
    for i in range(0, math.ceil(len(inputLIST) / INPUT_LIMIT)):
        resultDICT = runLoki(inputLIST[i*INPUT_LIMIT:(i+1)*INPUT_LIMIT], filterLIST)


def botRunLoki(inputSTR, filterLIST=[]):
    '''
    給 bot 呼叫用的 runLoki()。最大的不同在於，它多了一個段落是把 inputSTR 的字串，切分成 inputLIST 列表，然後再傳給 runLoki()
    '''
    punctuationPat = re.compile("[,\.\?:;，。？、：；\n]+")
    inputLIST = punctuationPat.sub("\n", inputSTR).split("\n")

    resultDICT = runLoki(inputLIST, filterLIST)
    print("Loki Result => {}".format(resultDICT))

    if "msg" in resultDICT.keys() and resultDICT["msg"] == "No Intent Matched!":
        return False
    else:
        return totalDICT

if __name__ == "__main__":
    # charge
    #print("[TEST] charge")
    #inputLIST = ['充電免費','排隊充電','自宅充電','來不及充電','充電要排隊','充電要時間','想充就去充','充電很花時間','充電要花時間','從早到晚排隊等充電','安排好行程對充電計畫的最佳化','如果不急那就使用目的地充電就好']
    #testLoki(inputLIST, ['charge'])
    #print("")

    # battery
    #print("[TEST] battery")
    #inputLIST = ['長效電池','長途補電','電池衰退','乾脆買油車','充電設備商','充電功率峰值','充電槍插下去','會不會傷電池','沒家充怎麼了','我找不到充電站','早上90％電量出門','打算把超充當家充','用超充當中繼補充','我沒辦法裝家充怎麼辦']
    #testLoki(inputLIST, ['battery'])
    #print("")

    # 輸入其它句子試看看
    inputLIST = ['長效電池','長途補電','電池衰退','乾脆買油車','充電設備商','充電功率峰值','充電槍插下去','會不會傷電池','沒家充怎麼了','我找不到充電站','早上90％電量出門','打算把超充當家充','用超充當中繼補充','我沒辦法裝家充怎麼辦']
    filterLIST = []
    resultDICT = runLoki(inputLIST, filterLIST)
    print("Result => {}".format(resultDICT))