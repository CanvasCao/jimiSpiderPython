#!/usr/bin/env python
# coding:utf-8

import re
import json
from sqlHelper import SqlHelper  # sqlHelper
from clueHelper import ClueHelper

dmId = 1
dt = SqlHelper.ExecuteDataTable(
    "select scrab_json,dict from jimi_radar_dimension_mode where id=" + str(dmId))
dictJson = json.loads(dt[0][1])
dict = dictJson['data']

scrab_json = json.loads(dt[0][0])
scrabArray = scrab_json['data']

resultsAll = []
for i in range(len(scrabArray)):
    scrabObj = scrabArray[i]
    scrab_id = int(scrabObj['scrabId'])
    processed_clue = ClueHelper.getProcessedClue(scrab_id, scrabObj['clue'])
    results = SqlHelper.ExecuteDataTable(
        "select scrab_result from jimi_radar_result where scrab_id=%d and processed_clue=%d" % (
            scrab_id, int(processed_clue)))

    resultsAll.extend(list(results))

# 结果字典
resDictionary = {}
for row in resultsAll:
    for word in dict:
        wordEncode = word.encode('utf8')
        resultHTML = row[0].encode('utf8')  # 不知道为什么
        pattern1 = re.compile(wordEncode)
        res = re.findall(pattern1, resultHTML)
        matchLength = res.__len__()

        if matchLength != 0:
            print matchLength
            print wordEncode
            if resDictionary.get(wordEncode) == None:
                resDictionary[wordEncode] = matchLength
            else:
                resDictionary[wordEncode] += matchLength

print json.dumps(resDictionary, ensure_ascii=False, encoding='UTF-8')

insertNum = SqlHelper.ExecuteNonQuery("update jimi_radar_dimension_mode set dm_result='%s' where id=%d" % (
    json.dumps(resDictionary, ensure_ascii=False, encoding='UTF-8'), dmId))