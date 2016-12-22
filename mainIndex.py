# coding:utf-8

import urllib
import requests
from sqlHelper import SqlHelper
from scrabHelper import ScrabHelper
from dateHelper import DateHelper


dmId = 1
searchArr = ['小黑瓶', '兰蔻小黑瓶', '兰蔻 小黑瓶']
searchStr = searchArr[0]


# quit()

# 百度指数
def baiduIndex():
    searchQuote = urllib.quote(searchStr.decode('utf8').encode('gbk'))
    url = 'https://index.baidu.com/?tpl=trend&word=' + searchQuote
    print url
    soup = ScrabHelper.getSoupFromURL(url, {}, 'gbk')
    print soup


# baiduIndex()


def baiduYear1():
    stf = 'stf=1450775975,1482398375|stftype=1'
    stf = urllib.quote(stf)
    url = "http://www.baidu.com/s?wd=小黑瓶&gpc=" + stf
    data = requests.get(url).text
    soup = ScrabHelper.getSoupFromHtml(data)
    print soup.find_all('div', 'nums')[0].get_text()


# baiduYear1()