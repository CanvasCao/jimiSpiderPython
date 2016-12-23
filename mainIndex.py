# coding:utf-8

import urllib
import datetime
import re
import requests
from sqlHelper import SqlHelper
from scrabHelper import ScrabHelper
from dateHelper import DateHelper
from selenium import webdriver
import time


dmId = 1
searchArr = ['小黑瓶', '兰蔻小黑瓶', '兰蔻 小黑瓶']
searchStr = searchArr[0]

count = SqlHelper.ExecuteScalar(
    "select count(*) from jimi_radar_index where dm_id=%d and keyword='%s'" % (dmId, searchStr))

if count == 0:
    SqlHelper.ExecuteScalar("insert into jimi_radar_index (dm_id,keyword,ctime) values (%d,'%s','%s')" % (
        dmId, searchStr, DateHelper.getDateNowStr()))

id = SqlHelper.ExecuteScalar("select id from jimi_radar_index where dm_id=%d and keyword='%s'" % (dmId, searchStr))


def numMinusComma(num):
    return ''.join(num.split(','))


# 百度指数
def baiduIndex():
    searchQuote = urllib.quote(searchStr.decode('utf8').encode('gbk'))
    url = 'https://index.baidu.com/?tpl=trend&word=' + searchQuote
    print url
    soup = ScrabHelper.getSoupFromURL(url, {}, 'gbk')
    print soup


# 百度今年的搜索结果
def baiduYear1():
    dateNow = datetime.datetime.now()
    dateYearAgo = dateNow + datetime.timedelta(days=-365)
    intNow = str(DateHelper.getDateInt(dateNow))
    yearAgoNow = str(DateHelper.getDateInt(dateYearAgo))

    print intNow
    print yearAgoNow

    stf = 'stf=' + yearAgoNow + ',' + intNow + '|stftype=1'
    stf = urllib.quote(stf)
    url = "http://www.baidu.com/s?wd=" + searchStr + "&gpc=" + stf
    data = requests.get(url).text
    soup = ScrabHelper.getSoupFromHtml(data)
    text = soup.find_all('div', 'nums')[0].get_text()  # 搜索工具百度为您找到相关结果约403,000个

    pat = re.compile(r'[\d,]+')
    num = pat.findall(text)[0]
    num = numMinusComma(num)

    sql = "update jimi_radar_index set %s = '%s' where id=%d" % ('baidu_year1', num, id)
    SqlHelper.ExecuteNonQuery(sql)


# baiduYear1()


# 需要登录 暂时写不出
def weiboYear1():
    # http://s.weibo.com/weibo/%25E5%258D%25A7%25E6%25A7%25BDa1&typeall=1&suball=1&timescope=custom:2015-12-01:2016-12-01&Refer=g
    url = 'http://s.weibo.com/weibo/%25E5%25B0%258F%25E9%25BB%2591%25E7%2593%25B6&Refer=STopic_box'

    dr = webdriver.PhantomJS(executable_path='C:\\Python27\\Scripts\\phantomjs.exe')
    dr.get(url)
    time.sleep(5)
    js = "document.body.scrollTop=10000"
    dr.execute_script(js)
    time.sleep(5)
    data = dr.page_source
    print data
    # soup=ScrabHelper.getSoupFromHtml(data)
    # print soup.find_all('div','search_rese')


# weiboYear1()

def weixinYear1():
    dateNow = datetime.datetime.now()
    dateYearAgo = dateNow + datetime.timedelta(days=-365)
    dateNow = str(dateNow).split(' ')[0]
    dateYearAgo = str(dateYearAgo).split(' ')[0]

    url = 'http://weixin.sogou.com/weixin?type=2&ie=utf8&query=' + searchStr + '&tsn=5&ft=' + dateYearAgo + '&et=' + dateNow + '&interation=null&wxid=&usip=null&from=tool'
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')

    text = soup.find_all('div', 'mun')[0].get_text()  # 搜索工具百度为您找到相关结果约403,000个

    pat = re.compile(r'[\d,]+')
    num = pat.findall(text)[0]
    num = numMinusComma(num)

    sql = "update jimi_radar_index set %s = '%s' where id=%d" % ('weixin_year1', num, id)
    SqlHelper.ExecuteNonQuery(sql)

# weixinYear1()