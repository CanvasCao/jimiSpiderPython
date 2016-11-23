# coding:utf-8


import re
from sqlHelper import SqlHelper  # sqlHelper
from scrabHelper import ScrabHelper
from dateHelper import DateHelper


dmId = 1

scrabJson = {"data": [{
                          "scrabId": 1,
                          "clue": 'http://cosme.pclady.com.cn/product/1682.html'
                      }, {
                          "scrabId": 2,
                          "clue": 'http://product.kimiss.com/product/14930/'
                      }]}
scrabArray = scrabJson['data']


def doSave(json):
    # print json
    scrabId = json.get('scrabId')  # int
    processed_clue = json.get('processed_clue')  # str
    scrab_result = json.get('scrab_result')
    data_time = json.get('data_time')

    '''
    rowCount = SqlHelper.ExecuteNonQuery(
        "insert into jimi_radar_result (scrab_id,processed_clue,scrab_result,data_time,insert_time) values('%d','%s','%s','%s','%s')" % (
            scrabId, processed_clue, scrab_result, data_time, DateHelper.getDateNowStr())
    )
    print rowCount
    '''


def doScrab(json):
    # print json
    defaultScrabPageNum = json.get('defaultScrabPageNum') or 10
    scrabId = json['scrabId']
    clue = json['clue']


    # 化妆品库的评论
    if scrabId == 1:
        # 匹配这个模型 找到 /1682.html 中的数字 就是id
        matches = re.findall(r"/(\d+)[.]{1}html", clue)
        proId = matches[0]

        startPageNum = 1  # 可能是0

        interfaceWithoutParas = 'http://cosme.pclady.com.cn/common/2013/solr_comment_list.jsp?&pageType=1&attitude=&status=&lvl=&ageBegin=&ageEnd=&skin=&stp=0&atp=0&type=0&pageNum=%d&id=' + str(
            proId)

        # 第一层for循环 循环接口
        while (True):
            interface = interfaceWithoutParas % (startPageNum)

            soup = ScrabHelper.getSoupFromInterface(interface, 'gb2312')

            divs = soup.find_all('div', 'userCmtList')[0].find_all('ul')[0].find_all('div', 'userCmt')
            if len(divs) == 0:
                return
            else:
                for div in divs:
                    content = div.find_all('div', 'uCmt')[0].find_all('a')[0].string
                    date = div.find_all('span', 'dateTime')[0].string

                    doSave(
                        {'scrabId': scrabId,
                         'processed_clue': proId,
                         'scrab_result': content,
                         'data_time': date.strip(),
                        })

            startPageNum += 1


    # 闺蜜网的评论
    elif scrabId == 2:
        # 匹配这个模型
        matches = re.findall(r"product/(\d+)/", clue)
        proId = matches[0]

        startPageNum = 1  # 可能是0
        interfaceWithoutParas = 'http://product.kimiss.com/product/%s/%d/'
        interface = interfaceWithoutParas % (proId, startPageNum)
        print interface
        soup = ScrabHelper.getSoupFromInterface(interface, 'utf-8')
        divs = soup.find_all('ul', 'f_remark_list')[0].find_all('div', 'f_re_rig')
        for div in divs:
            content = div.find_all('p', 'com_p')[0].string
            date = div.find_all('div', 'f_re_time')[0].find_all('cite')[0].string
            print str(1) + '-------------' + content
            print str(1) + '-------------' + date
            doSave(
                {'scrabId': scrabId,
                 'processed_clue': proId,
                 'scrab_result': content,
                 'data_time': date.strip(),
                })

# 主程 开始遍历scrabID爬数据
'''
for i in range(len(scrabArray)):
    ele = scrabArray[i]
    scrabId = ele['scrabId']
    clue = ele['clue']
    # print scrabId,clue
    doScrab(scrabId, clue)
'''

ele = scrabArray[0]
scrabId = ele['scrabId']
clue = ele['clue']
doScrab({'scrabId': scrabId,
         'clue': clue})

