# coding:utf-8


import re
from sqlHelper import SqlHelper  # sqlHelper
from scrabHelper import ScrabHelper


dmId = 1

scrabJson = {"data": [{
                          "scrabId": 1,
                          "clue": 'http://cosme.pclady.com.cn/product/1682.html'
                      }, {
                          "scrabId": 2,
                          "clue": 'http://product.kimiss.com/product/14930/'
                      }]}
scrabArray = scrabJson['data']


def doScrab(scrabId, clue):
    defaultScrabPageNum = 10

    # 化妆品库的评论
    if scrabId == 1:
        # 匹配这个模型 找到 /1682.html 中的数字 就是id
        matches = re.findall(r"/(\d+)[.]{1}html", clue)
        proId = matches[0]

        startPageNum = 1  # 可能是0
        interfaceWithoutParas = 'http://cosme.pclady.com.cn/common/2013/solr_comment_list.jsp?&pageType=1&attitude=&status=&lvl=&ageBegin=&ageEnd=&skin=&stp=0&atp=0&type=0&pageNum=%d&id=' + str(
            proId)
        interface = interfaceWithoutParas % (startPageNum)

        soup = ScrabHelper.getSoupFromInterface(interface, 'gb2312')

        divs = soup.find_all('div', 'userCmtList')[0].find_all('ul')[0].find_all('div', 'userCmt')
        for div in divs:
            content = div.find_all('div', 'uCmt')[0].find_all('a')[0].string
            date = div.find_all('span', 'dateTime')[0].string
            print str(1) + '-------------' + content
            print str(1) + '-------------' + date



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


# 主程 开始遍历scrabID爬数据
'''
for i in range(len(scrabArray)):
    ele = scrabArray[i]
    scrabId = ele['scrabId']
    clue = ele['clue']
    # print scrabId,clue
    doScrab(scrabId, clue)
'''

ele = scrabArray[1]
scrabId = ele['scrabId']
clue = ele['clue']
doScrab(scrabId, clue)

