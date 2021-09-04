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

if __name__ == "__main__":
    with open("C:\\Users\\admin\\Documents\\NLP_Training-main\\Work1\\account_info.py", encoding="utf-8") as f:
        userinfoDICT = json.loads(f.read())

    articut = Articut(username=userinfoDICT["username"], apikey=userinfoDICT["apikey"])

    #  [baseball = battery; basketball = charge] 
    baseballSTR = """電動車最常被拿來比較的是「續航里程」，若要衝高續航里程的數字，基本上只要增加電池容量就好，所以續航里程並不是一個適合拿來比較的指標，每一度電可跑幾公里的「電耗」才是技術力的展現，因為電池成本高昂，車廠要盡量做出較低的電耗，售價才有競爭力。某些人講到中共換電池的方式，這方式看似不錯，可是中共的充電站也曾發生換到電量不夠或者沒有充滿電的電池可更換，所以更換式根本不切實際，以gogoro來說A的充電站沒充滿的電池很多，我可以把其它充電站充滿電的電池送過來，汽車的電池有可能這麼送嗎？可別忘了汽車的電池會比機車來得大
    """.replace(" ", "").replace("\n", "")

    basketballSTR = """為了打通電動車最重要一哩路「充電焦慮」，行政院召集各部會，由經濟部規畫國內首份「公共充電樁建置」藍圖，以短中長三階段全面推動。首階段到2025年，預計結合中央與地方力量，在公有停車場、大賣場、加油站、台鐵高鐵站，大量建置公共充電樁，慢充、快充兩者總數要達7800座 ，讓車輛不斷電。充電焦慮 困擾民眾。國內電動汽車目前僅1.5萬輛，但去年呈倍增成長，雖然電動車時代來臨，但要全面普及仍有重重障礙，影響最大的是民眾的「充電焦慮」。
    """.replace(" ", "").replace("\n", "")

    # 將 KNOWLEDGE_NBA_Teams.json 和 KNOWLEDGE_MLB_Teams.json 兩個體育類的字典讀取出來，合併成 mixedDICT 以後，寫入 mixedDICT.json 檔
   # with open("ArticutAPI-master/Public_UserDefinedDict/KNOWLEDGE_NBA_Teams.json", encoding="utf-8") as f:
   #     nbaDICT = json.loads(f.read())
   # with open("ArticutAPI-master/Public_UserDefinedDict/KNOWLEDGE_MLB_Teams.json", encoding="utf-8") as f:
   #     mlbDICT = json.loads(f.read())

  #  mixedDICT = {**nbaDICT, **mlbDICT}
   # with open("mixedDICT.json", mode="w", encoding="utf-8") as f:
   #     json.dump(mixedDICT, f, ensure_ascii=False)

    # 將 baseballSTR 和 basketballSTR 兩篇文本各自送入 articut.parse() 裡，同時指定 userDefinedDictFILE 為剛才產生的 mixedDICT.json
    baseballResultDICT = articut.parse(baseballSTR)
    basketballResultDICT = articut.parse(basketballSTR)

    # 取得「動詞」做為特徵列表
    baseballVerbLIST = articut.getVerbStemLIST(baseballResultDICT)
    print("battery：")
    print(wordExtractor(baseballVerbLIST, unify=False))
    print("\n")
    print("charge：")
    basketballVerbLIST = articut.getVerbStemLIST(basketballResultDICT)
    print(wordExtractor(basketballVerbLIST, unify=False))
    print("\n")


    # 未知類別的文本 (battery1)

    unknownSTR01 = """以我的用車習慣，可能20年都開不到10萬公里，TESLA號稱要打造壽命達 160 萬公里 (100 萬英里) 電池，這樣的長效電池對我來說是不切實際的，也有可能對一般使用者來說也是用不到這麼多，如果電池改成月租型，不但車價可以比較便宜，將來車子要報廢的時候，電池也可以回收再使用，兼具環保的好處，這樣有可能可以做到嗎？
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("battery1：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. battery1] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. battery1] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))


    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("battery：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("charge：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")



    # 未知類別的文本 (battery1)

    unknownSTR01 = """以我的用車習慣，可能20年都開不到10萬公里，TESLA號稱要打造壽命達 160 萬公里 (100 萬英里) 電池，這樣的長效電池對我來說是不切實際的，也有可能對一般使用者來說也是用不到這麼多，如果電池改成月租型，不但車價可以比較便宜，將來車子要報廢的時候，電池也可以回收再使用，兼具環保的好處，這樣有可能可以做到嗎？
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("battery1：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. battery1] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. battery1] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))



    # 取得「TF-IDF」做為特徵列表
    baseballTFIDFLIST = articut.analyse.extract_tags(baseballResultDICT)
    print("battery TF-IDF：")
    print(baseballTFIDFLIST)
    print("\n")
    print("charge TF-IDF：")
    basketballTFIDFLIST = articut.analyse.extract_tags(basketballResultDICT)
    print(basketballTFIDFLIST)
    print("\n")

    # 未知類別的文本 (battery1)
    unknownSTR01 = """以我的用車習慣，可能20年都開不到10萬公里，TESLA號稱要打造壽命達 160 萬公里 (100 萬英里) 電池，這樣的長效電池對我來說是不切實際的，也有可能對一般使用者來說也是用不到這麼多，如果電池改成月租型，不但車價可以比較便宜，將來車子要報廢的時候，電池也可以回收再使用，兼具環保的好處，這樣有可能可以做到嗎？
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("battery1 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. battery1] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. battery1] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))



    # 未知類別的文本(charge1)
    unknownSTR01 = """電動車發展速度與基礎充電設施是否普及有高度相關，台電發現，許多住戶現況多會直接裝設慢充型的充電樁，當電動車數量變多，又同時充電，會有超載並引發跳電的疑慮，因此，建議社區可專設一戶，不僅可申請快充型充電樁，也能確保社區供電穩定。過去，屢傳社區管委會怕電動車太耗電、電費難記算等，與電動車主因設置充電樁發生摩擦，甚至有民眾整理全國不同意充電樁社區名單，儼然已是電動車車主的購屋重要參考指標之一。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("charge1：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge1] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge1] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))


    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("battery：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("charge：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")



    # 未知類別的文本(charge1)
    unknownSTR01 = """電動車發展速度與基礎充電設施是否普及有高度相關，台電發現，許多住戶現況多會直接裝設慢充型的充電樁，當電動車數量變多，又同時充電，會有超載並引發跳電的疑慮，因此，建議社區可專設一戶，不僅可申請快充型充電樁，也能確保社區供電穩定。過去，屢傳社區管委會怕電動車太耗電、電費難記算等，與電動車主因設置充電樁發生摩擦，甚至有民眾整理全國不同意充電樁社區名單，儼然已是電動車車主的購屋重要參考指標之一。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("charge1：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")
    
    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge1] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge1] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))



    # 未知類別的文本 (charge1)
    unknownSTR01 = """電動車發展速度與基礎充電設施是否普及有高度相關，台電發現，許多住戶現況多會直接裝設慢充型的充電樁，當電動車數量變多，又同時充電，會有超載並引發跳電的疑慮，因此，建議社區可專設一戶，不僅可申請快充型充電樁，也能確保社區供電穩定。過去，屢傳社區管委會怕電動車太耗電、電費難記算等，與電動車主因設置充電樁發生摩擦，甚至有民眾整理全國不同意充電樁社區名單，儼然已是電動車車主的購屋重要參考指標之一。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("charge1 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge1] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge1] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))
    
    
    
    # 未知類別的文本(battery2)
    unknownSTR01 = """對岸的蔚來電動車就是這樣做的,車電分離，電池用月租,還可以依照需求租大電池或小電池,平時租小電池，長途再去換大電池,可以參考對岸實務上怎麼運作經營,月租型對大量生產的特斯拉來講,,要花費更多維護成本.還不如多設快充站.而且月租型會針對使用者設定里程.
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("battery2：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. battery2] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. battery2] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))



    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("battery：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("charge：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")



    # 未知類別的文本(battery2)
    unknownSTR01 = """對岸的蔚來電動車就是這樣做的,車電分離，電池用月租,還可以依照需求租大電池或小電池,平時租小電池，長途再去換大電池,可以參考對岸實務上怎麼運作經營,月租型對大量生產的特斯拉來講,,要花費更多維護成本.還不如多設快充站.而且月租型會針對使用者設定里程.
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("battery2：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")
    
    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. battery2] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. battery2] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))

    

    # 未知類別的文本 (battery2)
    unknownSTR01 = """對岸的蔚來電動車就是這樣做的,車電分離，電池用月租,還可以依照需求租大電池或小電池,平時租小電池，長途再去換大電池,可以參考對岸實務上怎麼運作經營,月租型對大量生產的特斯拉來講,,要花費更多維護成本.還不如多設快充站.而且月租型會針對使用者設定里程.
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("battery2 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[ battery vs. battery2] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. battery2] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))


    # 未知類別的文本(charge2)
    unknownSTR01 = """台灣地狹人稠，北部住家型態多是公寓、華廈等大社區，充電樁裝設爭議與亂象也多源自於此。根據台電瞭解，國內住戶多會在自己的電表後拉線，設置慢充型充電樁，現在電動車數量還不多，用電可以承受，不過，一旦上百戶住戶的社區若都汰換成電動車，同時充電的後果恐是超載跳電，衝擊整個社區用電安全。台電建議，戶數眾多的社區可「專設一戶」，就能專供大樓充電設施用電，且有利電纜線架規劃，也方便未來擴增充電設施；至於社區擔憂的計費問題，台電指出，專戶的電表會獨立計算電費，與社區的公共電力區隔，社區也能與車主協商，設計一套收費制度，且若導入能源管理，安排離峰充電等，反而能賺錢。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("charge2：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge2] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge2] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))


    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("battery：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("charge：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")



    # 未知類別的文本(charge2)
    unknownSTR01 = """台灣地狹人稠，北部住家型態多是公寓、華廈等大社區，充電樁裝設爭議與亂象也多源自於此。根據台電瞭解，國內住戶多會在自己的電表後拉線，設置慢充型充電樁，現在電動車數量還不多，用電可以承受，不過，一旦上百戶住戶的社區若都汰換成電動車，同時充電的後果恐是超載跳電，衝擊整個社區用電安全。台電建議，戶數眾多的社區可「專設一戶」，就能專供大樓充電設施用電，且有利電纜線架規劃，也方便未來擴增充電設施；至於社區擔憂的計費問題，台電指出，專戶的電表會獨立計算電費，與社區的公共電力區隔，社區也能與車主協商，設計一套收費制度，且若導入能源管理，安排離峰充電等，反而能賺錢。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("charge2：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")
    
    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge2] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge2] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))



    # 未知類別的文本 (charge2)
    unknownSTR01 = """台灣地狹人稠，北部住家型態多是公寓、華廈等大社區，充電樁裝設爭議與亂象也多源自於此。根據台電瞭解，國內住戶多會在自己的電表後拉線，設置慢充型充電樁，現在電動車數量還不多，用電可以承受，不過，一旦上百戶住戶的社區若都汰換成電動車，同時充電的後果恐是超載跳電，衝擊整個社區用電安全。台電建議，戶數眾多的社區可「專設一戶」，就能專供大樓充電設施用電，且有利電纜線架規劃，也方便未來擴增充電設施；至於社區擔憂的計費問題，台電指出，專戶的電表會獨立計算電費，與社區的公共電力區隔，社區也能與車主協商，設計一套收費制度，且若導入能源管理，安排離峰充電等，反而能賺錢。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("charge2 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge2] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge2] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))



    # ############################################
    # ####
    # 未知類別的文本(charge3/complaint)
    unknownSTR01 = """如果都像某些車主呼籲的超充留給長途使用者，那超充為什麼不都蓋在宜蘭 花蓮 台東 台南 墾丁這種觀光勝地就好 ? 超充最終就是要回歸收費，收費就是商業，到底蓋在哪裡的商業需求會最高，不就車主最多的地方 ? 如果買電車就得負責在家充電的責任，香港新加坡等等那些國土比台灣小的，車位價格比天高的是不是特斯拉都不要賣了? 說穿了某位車主自己家裡裝了就是見不得人家現在用免費的，然後自己有時間每天上網酸別人，卻沒時間去排隊，真的不要講得自己好像很關心其他電車車主的權益似的。打開plugshare地圖密密麻麻的各種目的地充電 ，都坐落在都會區，難道各家充電設備商跟特斯拉會想得比車主少嗎 ? 開始收充電費跟佔用費才是真的。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("charge3/complaint：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge3/complaint] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge3/complaint] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))
 
    
    # 未知類別的文本(charge3/complaint)
    unknownSTR01 = """如果都像某些車主呼籲的超充留給長途使用者，那超充為什麼不都蓋在宜蘭 花蓮 台東 台南 墾丁這種觀光勝地就好 ? 超充最終就是要回歸收費，收費就是商業，到底蓋在哪裡的商業需求會最高，不就車主最多的地方 ? 如果買電車就得負責在家充電的責任，香港新加坡等等那些國土比台灣小的，車位價格比天高的是不是特斯拉都不要賣了? 說穿了某位車主自己家裡裝了就是見不得人家現在用免費的，然後自己有時間每天上網酸別人，卻沒時間去排隊，真的不要講得自己好像很關心其他電車車主的權益似的。打開plugshare地圖密密麻麻的各種目的地充電 ，都坐落在都會區，難道各家充電設備商跟特斯拉會想得比車主少嗎 ? 開始收充電費跟佔用費才是真的。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("charge3/complaint：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge3/complaint] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge3/complaint] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))


    # 未知類別的文本(charge3/complaint)
    unknownSTR01 = """如果都像某些車主呼籲的超充留給長途使用者，那超充為什麼不都蓋在宜蘭 花蓮 台東 台南 墾丁這種觀光勝地就好 ? 超充最終就是要回歸收費，收費就是商業，到底蓋在哪裡的商業需求會最高，不就車主最多的地方 ? 如果買電車就得負責在家充電的責任，香港新加坡等等那些國土比台灣小的，車位價格比天高的是不是特斯拉都不要賣了? 說穿了某位車主自己家裡裝了就是見不得人家現在用免費的，然後自己有時間每天上網酸別人，卻沒時間去排隊，真的不要講得自己好像很關心其他電車車主的權益似的。打開plugshare地圖密密麻麻的各種目的地充電 ，都坐落在都會區，難道各家充電設備商跟特斯拉會想得比車主少嗎 ? 開始收充電費跟佔用費才是真的。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("charge3/complaint TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")

    # 取得「TF-IDF」做為特徵列表
    baseballTFIDFLIST = articut.analyse.extract_tags(baseballResultDICT)
    print("battery TF-IDF：")
    print(baseballTFIDFLIST)
    print("\n")
    print("charge TF-IDF：")
    basketballTFIDFLIST = articut.analyse.extract_tags(basketballResultDICT)
    print(basketballTFIDFLIST)
    print("\n")

    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge3/complaint] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge3/complaint] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))
    
    

    # 未知類別的文本 (charge4/complaint)
    unknownSTR02 = """但是不管是特斯拉還是車主本身都希望超充使用上有 priority的觀念，如果不急，那就使用目的地充電就好，這也是為何特斯拉除了超充還廣設目的地充電。緊急情況下，例如你還來不及充電，就馬上有接下來的行程要跑，再去使用超充，這也是希望車主能自己安排好行程對充電計畫的最佳化。再來前面所說的很多車主現在可以爽充，是建立在更多車主懂得做良好的充電計畫，儘量把優先度讓給其他有需要的人。如果你們認為自己的確有很高的優先度，那大可儘量使用，但是不要不負責任的去宣導想充就去充的概念，那畢竟是大多數車主把充電的優先權讓出來的。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("charge4/complaint：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[batterry vs. charge4/complaint] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge4/complaint] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))



    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("battery名詞：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("charge名詞：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")


    # 未知類別的文本(charge4/complaint)
    unknownSTR01 = """但是不管是特斯拉還是車主本身都希望超充使用上有 priority的觀念，如果不急，那就使用目的地充電就好，這也是為何特斯拉除了超充還廣設目的地充電。緊急情況下，例如你還來不及充電，就馬上有接下來的行程要跑，再去使用超充，這也是希望車主能自己安排好行程對充電計畫的最佳化。再來前面所說的很多車主現在可以爽充，是建立在更多車主懂得做良好的充電計畫，儘量把優先度讓給其他有需要的人。如果你們認為自己的確有很高的優先度，那大可儘量使用，但是不要不負責任的去宣導想充就去充的概念，那畢竟是大多數車主把充電的優先權讓出來的。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("charge4/complaint：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")
    
    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge4/complaint] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge4/complaint] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))



    # 未知類別的文本 (charge4/complaint)
    unknownSTR01 = """但是不管是特斯拉還是車主本身都希望超充使用上有 priority的觀念，如果不急，那就使用目的地充電就好，這也是為何特斯拉除了超充還廣設目的地充電。緊急情況下，例如你還來不及充電，就馬上有接下來的行程要跑，再去使用超充，這也是希望車主能自己安排好行程對充電計畫的最佳化。再來前面所說的很多車主現在可以爽充，是建立在更多車主懂得做良好的充電計畫，儘量把優先度讓給其他有需要的人。如果你們認為自己的確有很高的優先度，那大可儘量使用，但是不要不負責任的去宣導想充就去充的概念，那畢竟是大多數車主把充電的優先權讓出來的。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("charge4/complaint TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge4/complaint] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge4/complaint] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))



    # 未知類別的文本(包膜)
    unknownSTR01 = """在下訂Model 3之後，就開始思考交車後，要如何維持新車的亮度與漆面的保護，研究了很多資訊，也做了非常多的功課，發現眾多車友分為兩大派，「鍍膜派」與「包膜派」兩種，當然各有各的優缺點，要看自己的環境與需求，小弟就不在這評論與多加贅述，因應小弟主要停車大多室外為主，且常會跑國道，前一台車子也被小石頭擊落噴發過好幾個洞，心痛不已，所以就把目標設定為全車包膜，但不查則已，一查驚人，改色膜、TPH犀牛皮、TPU修復犀牛皮，價差也差異非常多，從整車不到5萬，到整車破10萬的價格都有，讓小弟整個頭痛不已，畢竟自己不是專業人士，坦白說，單看膜料的外觀，我也分不清哪種是大陸膜料，哪種是進口膜料，更別說無良的店家收進口料的錢，實際上貼的是哪種膜料，一般消費者也很難察覺，所以小弟走訪過許多店家，也會跟店家訴說自己的需求，最後選定台中這間店家來處理相關包膜事宜。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("包膜：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. 包膜] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. 包膜] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))
 
 
    
    # 未知類別的文本(包膜)
    unknownSTR01 = """在下訂Model 3之後，就開始思考交車後，要如何維持新車的亮度與漆面的保護，研究了很多資訊，也做了非常多的功課，發現眾多車友分為兩大派，「鍍膜派」與「包膜派」兩種，當然各有各的優缺點，要看自己的環境與需求，小弟就不在這評論與多加贅述，因應小弟主要停車大多室外為主，且常會跑國道，前一台車子也被小石頭擊落噴發過好幾個洞，心痛不已，所以就把目標設定為全車包膜，但不查則已，一查驚人，改色膜、TPH犀牛皮、TPU修復犀牛皮，價差也差異非常多，從整車不到5萬，到整車破10萬的價格都有，讓小弟整個頭痛不已，畢竟自己不是專業人士，坦白說，單看膜料的外觀，我也分不清哪種是大陸膜料，哪種是進口膜料，更別說無良的店家收進口料的錢，實際上貼的是哪種膜料，一般消費者也很難察覺，所以小弟走訪過許多店家，也會跟店家訴說自己的需求，最後選定台中這間店家來處理相關包膜事宜。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("包膜：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. 包膜] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. 包膜] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))



    # 未知類別的文本 (包膜)
    unknownSTR02 = """在下訂Model 3之後，就開始思考交車後，要如何維持新車的亮度與漆面的保護，研究了很多資訊，也做了非常多的功課，發現眾多車友分為兩大派，「鍍膜派」與「包膜派」兩種，當然各有各的優缺點，要看自己的環境與需求，小弟就不在這評論與多加贅述，因應小弟主要停車大多室外為主，且常會跑國道，前一台車子也被小石頭擊落噴發過好幾個洞，心痛不已，所以就把目標設定為全車包膜，但不查則已，一查驚人，改色膜、TPH犀牛皮、TPU修復犀牛皮，價差也差異非常多，從整車不到5萬，到整車破10萬的價格都有，讓小弟整個頭痛不已，畢竟自己不是專業人士，坦白說，單看膜料的外觀，我也分不清哪種是大陸膜料，哪種是進口膜料，更別說無良的店家收進口料的錢，實際上貼的是哪種膜料，一般消費者也很難察覺，所以小弟走訪過許多店家，也會跟店家訴說自己的需求，最後選定台中這間店家來處理相關包膜事宜。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR02, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("包膜 TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. 包膜] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. 包膜] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))


   
    # 未知類別的文本 (charge5/complaint)

    unknownSTR01 = """一般對充電的疑慮是什麼?電氣走火、充電異常危險吧。歸根究柢就是電流異常或電路問題。但一般家庭中最不缺的就是電器，冰箱會電線走火嗎?手機會充電到一半爆炸嗎?除濕機會開到一半自燃嗎?電磁爐、微波爐會使用到一半爆炸嗎?以上都會，也都確確實實發生過，但特斯拉好像還沒有充電起火的案例吧。有發生起火的沒要求要保險，沒發生起火的反而要求要保險?
    有住戶會要求，大樓只要有一個人買了一個電磁爐、一個冰箱。這個人就需要替整棟大樓投保保險，不然不可以買嗎?不然如果燒起來的話，整棟大樓火燒怎麼辦?誰要負責?如果燒起來，附近住戶也跟著遭殃，更慘的如果影響到房價，是你要負責還是管委會要負責?管委會為什麼要為這個風險承擔你做到了嗎?說大電流充電危險的人知道嗎?這些口中有可能火燒的危險，大概就等同於你家同時開兩台電磁爐煮火鍋一般的危險嗎?危險的不是安裝充電樁，而是在環境不允許的情況下，開啟過大的充電電流，例如老舊社區線路不安全的狀況下,卻硬要開啟到48A、72A充電電流。所以才會需要專業團隊來場勘評估，安裝地點能夠使用多大的充電電流或適不適合安裝。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownVerbLIST = articut.getVerbStemLIST(unknownResultDICT)
    print("charge5/complaint：")
    print(wordExtractor(unknownVerbLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個動詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballVerbLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballVerbLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownVerbLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge5/complaint] 的動詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge5/complaint] 的動詞餘弦相似度:{}".format(basketball2unknownSIM))


    # 取得「名詞」做為特徵列表
    baseballNounLIST = articut.getNounStemLIST(baseballResultDICT)
    print("battery：")
    print(wordExtractor(baseballNounLIST, unify=False))
    print("\n")
    print("Charge：")
    basketballNounLIST = articut.getNounStemLIST(basketballResultDICT)
    print(wordExtractor(basketballNounLIST, unify=False))
    print("\n")



    # 未知類別的文本 (charge5/complaint)

    unknownSTR01 = """一般對充電的疑慮是什麼?電氣走火、充電異常危險吧。歸根究柢就是電流異常或電路問題。但一般家庭中最不缺的就是電器，冰箱會電線走火嗎?手機會充電到一半爆炸嗎?除濕機會開到一半自燃嗎?電磁爐、微波爐會使用到一半爆炸嗎?以上都會，也都確確實實發生過，但特斯拉好像還沒有充電起火的案例吧。有發生起火的沒要求要保險，沒發生起火的反而要求要保險?
    有住戶會要求，大樓只要有一個人買了一個電磁爐、一個冰箱。這個人就需要替整棟大樓投保保險，不然不可以買嗎?不然如果燒起來的話，整棟大樓火燒怎麼辦?誰要負責?如果燒起來，附近住戶也跟著遭殃，更慘的如果影響到房價，是你要負責還是管委會要負責?管委會為什麼要為這個風險承擔你做到了嗎?說大電流充電危險的人知道嗎?這些口中有可能火燒的危險，大概就等同於你家同時開兩台電磁爐煮火鍋一般的危險嗎?危險的不是安裝充電樁，而是在環境不允許的情況下，開啟過大的充電電流，例如老舊社區線路不安全的狀況下,卻硬要開啟到48A、72A充電電流。所以才會需要專業團隊來場勘評估，安裝地點能夠使用多大的充電電流或適不適合安裝。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownNounLIST = articut.getNounStemLIST(unknownResultDICT)
    print("charge5/complaint：")
    print(wordExtractor(unknownNounLIST, unify=False))
    print("\n")


    # 利用 Counter() 模組計算每個名詞出現的次數
    baseballCOUNT = Counter(wordExtractor(baseballNounLIST, unify=False))
    basketballCOUNT = Counter(wordExtractor(basketballNounLIST, unify=False))
    unknownCOUNT = Counter(wordExtractor(unknownNounLIST, unify=False))

    # 計算 [棒球文本 vs. 未知文本] 的餘弦相似度；計算 [籃球文本 vs. 未知文本] 的餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge5/complaint] 的名詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge5/complaint] 的名詞餘弦相似度:{}".format(basketball2unknownSIM))



    # 取得「TF-IDF」做為特徵列表
    baseballTFIDFLIST = articut.analyse.extract_tags(baseballResultDICT)
    print("battery TF-IDF：")
    print(baseballTFIDFLIST)
    print("\n")
    print("charge TF-IDF：")
    basketballTFIDFLIST = articut.analyse.extract_tags(basketballResultDICT)
    print(basketballTFIDFLIST)
    print("\n")

    # 未知類別的文本 (charge5/complaint)
    unknownSTR01 = """一般對充電的疑慮是什麼?電氣走火、充電異常危險吧。歸根究柢就是電流異常或電路問題。但一般家庭中最不缺的就是電器，冰箱會電線走火嗎?手機會充電到一半爆炸嗎?除濕機會開到一半自燃嗎?電磁爐、微波爐會使用到一半爆炸嗎?以上都會，也都確確實實發生過，但特斯拉好像還沒有充電起火的案例吧。有發生起火的沒要求要保險，沒發生起火的反而要求要保險?
    有住戶會要求，大樓只要有一個人買了一個電磁爐、一個冰箱。這個人就需要替整棟大樓投保保險，不然不可以買嗎?不然如果燒起來的話，整棟大樓火燒怎麼辦?誰要負責?如果燒起來，附近住戶也跟著遭殃，更慘的如果影響到房價，是你要負責還是管委會要負責?管委會為什麼要為這個風險承擔你做到了嗎?說大電流充電危險的人知道嗎?這些口中有可能火燒的危險，大概就等同於你家同時開兩台電磁爐煮火鍋一般的危險嗎?危險的不是安裝充電樁，而是在環境不允許的情況下，開啟過大的充電電流，例如老舊社區線路不安全的狀況下,卻硬要開啟到48A、72A充電電流。所以才會需要專業團隊來場勘評估，安裝地點能夠使用多大的充電電流或適不適合安裝。
    """.replace(" ", "").replace("\n", "")

    unknownResultDICT = articut.parse(unknownSTR01, userDefinedDictFILE="./mixedDICT.json")
    unknownTFIDFLIST = articut.analyse.extract_tags(unknownResultDICT)
    print("charge5/complaint TF-IDF：")
    print(unknownTFIDFLIST)
    print("\n")


    # 利用 Counter() 模組計算每個 TF-IDF 特徵詞出現的次數
    baseballCOUNT = Counter(baseballTFIDFLIST)
    basketballCOUNT = Counter(basketballTFIDFLIST)
    unknownCOUNT = Counter(unknownTFIDFLIST)

    # 計算 [棒球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；計算 [籃球文本 vs. 未知文本] 的 TF-IDF 餘弦相似度；
    baseball2unknownSIM = counterCosineSimilarity(baseballCOUNT, unknownCOUNT)
    basketball2unknownSIM = counterCosineSimilarity(basketballCOUNT, unknownCOUNT)

    print("[battery vs. charge5/complaint] 的 TF-IDF 特徵詞餘弦相似度:{}".format(baseball2unknownSIM))
    print("[charge vs. charge5/complaint] 的 TF-IDF 特徵詞餘弦相似度:{}".format(basketball2unknownSIM))

   



    

  