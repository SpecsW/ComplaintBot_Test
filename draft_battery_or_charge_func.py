＃ draft of battery_or_charge function

#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from collections import Counter
from ArticutAPI import Articut
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

def battery_or_charge(input_string):
    if __name__ == "__main__":
        with open("C:\\Users\\admin\\Documents\\NLP_Training-main\\Work1\\account_info.py", encoding="utf-8") as f:
            userinfoDICT = json.loads(f.read())

    articut = Articut(username=userinfoDICT["username"], apikey=userinfoDICT["apikey"])

    #  [baseball = battery; basketball = charge] 
    batterySTR = """電動車最常被拿來比較的是「續航里程」，若要衝高續航里程的數字，基本上只要增加電池容量就好，所以續航里程並不是一個適合拿來比較的指標，每一度電可跑幾公里的「電耗」才是技術力的展現，因為電池成本高昂，車廠要盡量做出較低的電耗，售價才有競爭力。某些人講到中共換電池的方式，這方式看似不錯，可是中共的充電站也曾發生換到電量不夠或者沒有充滿電的電池可更換，所以更換式根本不切實際，以gogoro來說A的充電站沒充滿的電池很多，我可以把其它充電站充滿電的電池送過來，汽車的電池有可能這麼送嗎？可別忘了汽車的電池會比機車來得大
    """.replace(" ", "").replace("\n", "")

    chargeSTR = """為了打通電動車最重要一哩路「充電焦慮」，行政院召集各部會，由經濟部規畫國內首份「公共充電樁建置」藍圖，以短中長三階段全面推動。首階段到2025年，預計結合中央與地方力量，在公有停車場、大賣場、加油站、台鐵高鐵站，大量建置公共充電樁，慢充、快充兩者總數要達7800座 ，讓車輛不斷電。充電焦慮 困擾民眾。國內電動汽車目前僅1.5萬輛，但去年呈倍增成長，雖然電動車時代來臨，但要全面普及仍有重重障礙，影響最大的是民眾的「充電焦慮」。
    """.replace(" ", "").replace("\n", "")
    
    batteryResultDICT = articut.parse(batterySTR)
    chargeResultDICT = articut.parse(chargeSTR)
    
    clean_string = input_string.replace(" ", "").replace("\n", "")
    
    newResultDICT = articut.parse(clean_string)
    newVerbLIST = articut.getVerbStemLIST(newResultDICT)
    
    batteryCOUNT = Counter(wordExtractor(batteryVerbLIST, unify=False))
    chargeCOUNT = Counter(wordExtractor(chargeVerbLIST, unify=False))
    newSTRCOUNT = Counter(wordExtractor(newVerbLIST, unify=False))
    
    battery2newSIM = counterCosineSimilarity(batteryCOUNT, newSTRCOUNT)
    charge2newSIM = counterCosineSimilarity(chargeCOUNT, newSTRCOUNT)
    
    if battery2newSIM > charge2newSIM:
        final_decision = battery
    elif battery2newSIM < charge2newSIM:
        final_decision = battery
    else:
        finally_decision = None
    
    return final_decision