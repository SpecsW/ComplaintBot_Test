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
userDefinedDICT = {"car": ["電車", "油車"], "花": ["用"], "tesla": ["特斯拉", "台特"], "price ": ["收費", "以價制量", "收", "免費", "吃到飽", "限制", "成本", "費用", "累進", "充電費", "佔用費", "以價制量", "車價", "錢"], "充電": ["充"], "program": ["月租型", "方案", "月租電池", "車電分離", "買斷", "租"], "charging": ["充電", "充", "功率", "補充", "補電", "中繼補充"], "equipment": ["充電槍", "超充站", "家充", "第三代超級充電站", "超級充電站", "充電設備", "充電樁", "超充", "充電站"], "batteryfunct": ["電池組", "電池", "預熱功能", "電量", "長效電池", "大電池", "小電池", "長效電池"], "relatedgroups": ["社區管委會"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_charge:
        print("[charge] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)
    resultDICT["on_charging"] = 0
    #用 args 的數量來決定要給它的積分，故稍後會用 len(args) 來計分

    if utterance == "[充電]免費":
        if args[0] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)


    if utterance == "[充電]很[花][時間]":
        if args[0] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    if utterance == "[充電]要[時間]":
        if args[0] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    if utterance == "[充電]要[花][時間]":
        if args[0] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    if utterance == "[充電]要排隊":
        if args[0] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    if utterance == "[自宅][充電]":
        if args[1] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    if utterance == "來不及[充電]":
        if args[0] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    if utterance == "如果[不急]那就使用目的地[充電]就[好]":
        if args[1] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    if utterance == "安排好行程對[充電]計畫的最佳化":
        if args[0] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    if utterance == "從早到晚排隊等[充電]":
        if args[0] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    if utterance == "想[充]就去[充]":
        if args[0] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    if utterance == "排隊[充電]":
        if args[0] in userDefinedDICT["charging"]:
            resultDICT["on_charging"] = resultDICT["on_charging"] + len(args)

    return resultDICT