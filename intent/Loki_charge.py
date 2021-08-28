#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for charge

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_charge = True
userDefinedDICT = {"花": ["用"], "充電": ["充"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_charge:
        print("[charge] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    if utterance == "[充電]免費":
        # write your code here
        pass

    if utterance == "[充電]很[花][時間]":
        # write your code here
        pass

    if utterance == "[充電]要[時間]":
        # write your code here
        pass

    if utterance == "[充電]要[花][時間]":
        # write your code here
        pass

    if utterance == "[充電]要排隊":
        # write your code here
        pass

    if utterance == "[自宅][充電]":
        # write your code here
        pass

    if utterance == "來不及[充電]":
        # write your code here
        pass

    if utterance == "如果[不急]那就使用目的地[充電]就[好]":
        # write your code here
        pass

    if utterance == "安排好行程對[充電]計畫的最佳化":
        # write your code here
        pass

    if utterance == "從早到晚排隊等[充電]":
        # write your code here
        pass

    if utterance == "想[充]就去[充]":
        # write your code here
        pass

    if utterance == "排隊[充電]":
        # write your code here
        pass

    return resultDICT