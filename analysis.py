#!/usr/bin/env python
# coding:utf-8

import re
import json
from sqlHelper import SqlHelper  # sqlHelper
from clueHelper import ClueHelper


dmId = 1


def analysisAndSaveOnce(resultsAll, dict, fieldName):
    # 结果字典
    resultDictionary = {}
    for row in resultsAll:
        for word in dict:
            wordEncode = word.encode('utf8')
            resultHTML = row[0].encode('utf8')  # 不知道为什么
            pattern1 = re.compile(wordEncode)
            res = re.findall(pattern1, resultHTML)
            matchLength = res.__len__()

            if matchLength != 0:
                # print matchLength
                # print wordEncode
                if resultDictionary.get(wordEncode) == None:
                    resultDictionary[wordEncode] = matchLength
                else:
                    resultDictionary[wordEncode] += matchLength

    jsonStr = json.dumps(resultDictionary, ensure_ascii=False, encoding='UTF-8')


    sql= "update jimi_radar_dimension_mode set %s ='%s' where id=%d" % (fieldName, jsonStr, dmId)
    insertNum = SqlHelper.ExecuteNonQuery(sql)
    print jsonStr
    print sql
    print insertNum


# 得到当前dm爬取了哪些网站
scrab_json = SqlHelper.ExecuteScalar("select scrab_json from jimi_radar_dimension_mode where id=" + str(dmId))
# {"data": [{"scrabId": 1,
# "clue": 'http://cosme.pclady.com.cn/product/29669.html'
# }, {
# "scrabId": 2,
# "clue": 'http://product.kimiss.com/product/80696/'
# }]}
scrab_json = json.loads(scrab_json)
scrabArray = scrab_json['data']

# 得到字典对象数组
dtDict = SqlHelper.ExecuteDataTable(
    "select cate_json from jimi_radar_dict_cate where id<10 order by id")

# 字典关键字数组 {"data":["浓稠", "粘稠", "有点稠", "稠稠", "粘粘", "黏腻", "黏黏", "厚实", "厚重", "比较厚", "丰盈"]}
dictKeyWordArray = []
for i in range(9):
    jsonStr = dtDict[i][0]
    dictKeyWordArray.append(json.loads(jsonStr)['data'])


# 保存回数据库的字段名 数组
dictFieldArray = ['dm_result_outlook',
                  'dm_result_smell',
                  'dm_result_texture',
                  'dm_result_useFeeling',
                  'dm_result_effect', 'dm_result_effectSatisfaction',
                  'dm_result_makeup',
                  'dm_result_color',
                  'dm_result_priceSatisfaction',
                  'dm_result_other']

# print dictKeyWordArray[2]
# quit()



# 爬取多个网站的结果数据 进行汇总 resultsAll.extend到一个数组中
resultsAll = []
for i in range(len(scrabArray)):
    scrabObj = scrabArray[i]
    scrab_id = int(scrabObj['scrabId'])
    processed_clue = ClueHelper.getProcessedClue(scrab_id, scrabObj['clue'])
    results = SqlHelper.ExecuteDataTable(
        "select scrab_result from jimi_radar_result where scrab_id=%d and processed_clue=%d" % (
            scrab_id, int(processed_clue)))

    resultsAll.extend(list(results))


analysisAndSaveOnce(resultsAll, dictKeyWordArray[3], dictFieldArray[3])
quit()

# 根据多个字典分析多个结果
for i in range(len(dictKeyWordArray)):
    print dictKeyWordArray[i]
    print dictFieldArray[i]
    print i
    analysisAndSaveOnce(resultsAll, dictKeyWordArray[i], dictFieldArray[i])