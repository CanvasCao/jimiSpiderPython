# coding:utf-8
import json

from sqlHelper import SqlHelper
from scrabHelper import ScrabHelper
from dateHelper import DateHelper


dmId = 1
searchArr = ['小黑瓶', '兰蔻小黑瓶', '兰蔻 小黑瓶']
searchStr = searchArr[0]

count = SqlHelper.ExecuteScalar(
    "select count(*) from jimi_radar_evaluate where dm_id=%d and keyword='%s'" % (dmId, searchStr))

if count == 0:
    SqlHelper.ExecuteScalar("insert into jimi_radar_evaluate (dm_id,keyword,ctime) values (%d,'%s','%s')" % (
        dmId, searchStr, DateHelper.getDateNowStr()))

id = SqlHelper.ExecuteScalar("select id from jimi_radar_evaluate where dm_id=%d and keyword='%s'" % (dmId, searchStr))

print id

# 微博印象
def weiboYinXiang():
    resArr = {}
    url = 'http://s.weibo.com/impress?key=' + searchStr + '&cate=whole&isswitch=1&refer=tag&cuid=3235723984'
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')
    secs = soup.find_all('div', 'impress_label')[0].find_all('section')
    for sec in secs:
        aas = sec.find_all('a')
        length = len(aas)

        for a in aas:
            text = a.get_text()
            resArr[text] = (5 - length)

    resJson = {
        'data': resArr
    }

    sql = "update jimi_radar_evaluate set weiboyinxiang = '%s' where id=%d" % (
        json.dumps(resJson, ensure_ascii=False, encoding='UTF-8'), id)
    print sql
    SqlHelper.ExecuteNonQuery(sql)


# weiboYinXiang()


# 天猫评价
def tiaomao():
    url = 'https://rate.tmall.com/listTagClouds.htm?itemId=43165859354&isAll=true&isInner=true&t=1482481000827&callback=jsonp1575'
    jsonp = ScrabHelper.getHTMLFromURL(url, {}, 'gbk')


    # json = {
    # "tags": {
    # "dimenSum": 9,
    # "innerTagCloudList": "",
    # "rateSum": 177,
    # "structuredRateStatisticList": [],
    #     "tagClouds": [{"count": 39, "id": "10120", "posi": true, "tag": "服务好", "weight": 0}, {
    #         "count": 35,
    #         "id": "620",
    #         "posi": true,
    #         "tag": "质量好",
    #         "weight": 0
    #     }, {"count": 33, "id": "420", "posi": true, "tag": "物流快", "weight": 0}, {
    #         "count": 33,
    #         "id": "1020",
    #         "posi": true,
    #         "tag": "正品",
    #         "weight": 0
    #     }, {"count": 13, "id": "824", "posi": true, "tag": "保湿滋润", "weight": 0}, {
    #         "count": 9,
    #         "id": "4624",
    #         "posi": true,
    #         "tag": "吸收效果不错",
    #         "weight": 0
    #     }, {"count": 8, "id": "2524", "posi": true, "tag": "清洁度强", "weight": 0}, {
    #         "count": 4,
    #         "id": "124",
    #         "posi": true,
    #         "tag": "味道好闻",
    #         "weight": 0
    #     }, {"count": 3, "id": "1224", "posi": true, "tag": "控油", "weight": 0}],
    #     "userTagCloudList": [{
    #         "dimenName": "年龄",
    #         "id": 26,
    #         "tagScaleList": [{"count": 2, "index": 0, "proportion": 0.0, "scale": "18岁以下"}, {
    #             "count": 491,
    #             "index": 1,
    #             "proportion": 16.0,
    #             "scale": "18-24"
    #         }, {"count": 1011, "index": 2, "proportion": 33.0, "scale": "25-29"}, {
    #             "count": 1080,
    #             "index": 3,
    #             "proportion": 35.0,
    #             "scale": "30-40"
    #         }, {"count": 484, "index": 4, "proportion": 16.0, "scale": "40岁以上"}],
    #         "total": 3068
    #     }]
    # }
    # }
    loadjson = ScrabHelper.loads_jsonp(jsonp)

    # ******************************************************
    tagClouds = loadjson['tags']['tagClouds']
    resArr = {}
    for tagCloud in tagClouds:
        resArr[tagCloud['tag']] = tagCloud['count']

    resJson = {
        'data': resArr
    }

    sql = "update jimi_radar_evaluate set tianmaoyinxiang = '%s' where id=%d" % (
        json.dumps(resJson, ensure_ascii=False, encoding='UTF-8'), id)
    print sql
    SqlHelper.ExecuteNonQuery(sql)

    # ******************************************************
    tagScaleList = loadjson['tags']['userTagCloudList'][0]['tagScaleList']
    resArr = {}
    for tagScale in tagScaleList:
        resArr[tagScale['scale']] = tagScale['count']

    resJson = {
        'data': resArr
    }

    sql = "update jimi_radar_evaluate set tianmaoAge = '%s' where id=%d" % (
        json.dumps(resJson, ensure_ascii=False, encoding='UTF-8'), id)
    print sql
    SqlHelper.ExecuteNonQuery(sql)


# tiaomao()


def jd():
    url = 'https://sclub.jd.com/comment/productPageComments.action?productId=256035&score=0&sortType=3&page=0&pageSize=10&isShadowSku=0&callback=fetchJSON_comment98vv3934'
    jsonp = ScrabHelper.getHTMLFromURL(url, {}, 'gbk')
    loadJson = ScrabHelper.loads_jsonp(jsonp)
    hotCommentTagStatistics = loadJson['hotCommentTagStatistics']
    resArr = {}
    for stat in hotCommentTagStatistics:
        resArr[stat['name']] = stat['count']

    resJson = {
        'data': resArr
    }

    sql = "update jimi_radar_evaluate set jdyinxiang = '%s' where id=%d" % (
        json.dumps(resJson, ensure_ascii=False, encoding='UTF-8'), id)
    print sql
    SqlHelper.ExecuteNonQuery(sql)


jd()