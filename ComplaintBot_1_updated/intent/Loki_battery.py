#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    Loki module for battery

    Input:
        inputSTR      str,
        utterance     str,
        args          str[],
        resultDICT    dict

    Output:
        resultDICT    dict
"""

DEBUG_battery = True
userDefinedDICT = {"car": ["電車", "油車"], "花": ["用"],
                   "tesla": ["特斯拉", "台特"],
                   "price ": ["收費", "以價制量", "收", "免費", "吃到飽", "限制", "成本", "費用", "累進", "充電費", "佔用費", "以價制量", "車價", "錢"],
                   "充電": ["充"],
                   "program": ["月租型", "方案", "月租電池", "車電分離", "買斷", "租"],
                   "charging": ["充電", "充", "功率", "補充", "補電", "中繼補充"],
                   "equipment": ["充電槍", "超充站", "家充", "第三代超級充電站", "超級充電站", "充電設備", "充電樁", "超充", "充電站"],
                   "batteryfunct": ["電池組", "電池", "預熱功能", "電量", "長效電池", "大電池", "小電池", "長效電池"],
                   "relatedgroups": ["社區管委會"]}

# 將符合句型的參數列表印出。這是 debug 或是開發用的。
def debugInfo(inputSTR, utterance):
    if DEBUG_battery:
        print("[battery] {} ===> {}".format(inputSTR, utterance))

def getResult(inputSTR, utterance, args, resultDICT):
    debugInfo(inputSTR, utterance)

    #用 args 的數量來決定要給它的積分，故稍後會用 len(args) 來計分

    if utterance == "[乾脆]買[油車]":
        if args[1] in userDefinedDICT["car"] or args[1] in userDefinedDICT["equipment"] or args[1] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "[充電][功率]峰值":
        if args[0] in userDefinedDICT["equipment"] or args[0] in userDefinedDICT["batteryfunct"] or args[1] in userDefinedDICT["equipment"] or args[1] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "[充電槍]插下去":
        if args[0] in userDefinedDICT["car"] or args[0] in userDefinedDICT["equipment"] or args[0] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "[充電設備]商":
        if args[0] in userDefinedDICT["car"] or args[0] in userDefinedDICT["equipment"] or args[0] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "[我]找不到[充電站]":
        if args[1] in userDefinedDICT["equipment"] or args[1] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "[我]沒辦法裝[家充]怎麼辦":
        if args[1] in userDefinedDICT["equipment"] or args[1] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "[早上][90％][電量]出門":
        if args[2] in userDefinedDICT["car"] or args[2] in userDefinedDICT["equipment"] or args[2] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "[長效電池]":
        if args[0] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "[電池]衰退":
        if args[0] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "打算把[超充]當[家充]":
        if args[0] in userDefinedDICT["equipment"] or args[0] in userDefinedDICT["batteryfunct"] or args[1] in userDefinedDICT["equipment"] or args[1] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "會不[會]傷[電池]":
        if args[1] in userDefinedDICT["equipment"] or args[1] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "沒[家充]怎麼了":
        if args[0] in userDefinedDICT["equipment"] or args[0] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "用[超充]當[中繼補充]":
        if args[0] in userDefinedDICT["equipment"] or args[0] in userDefinedDICT["batteryfunct"] or args[1] in userDefinedDICT["equipment"] or args[1] in userDefinedDICT["batteryfunct"]:
            resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    if utterance == "長途[補電]":
        if "長途" in inputSTR:
            if args[0] in userDefinedDICT["equipment"] or args[0] in userDefinedDICT["batteryfunct"]:
                resultDICT["on_battery"] = resultDICT["on_battery"] + len(args)

    return resultDICT