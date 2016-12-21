# coding:utf-8

import urllib
import re
import requests
from sqlHelper import SqlHelper
from scrabHelper import ScrabHelper
from dateHelper import DateHelper

from selenium import webdriver
import time


dmId = 1
searchStr = '兰蔻 小黑瓶'
searchArr = searchStr.split(' ')

searchStrAdd = '+'.join(searchArr)
searchStr20 = '%20'.join(searchArr)

count = SqlHelper.ExecuteNonQuery(
    "select count(*) from jimi_radar_video where dm_id=%d and keyword='%s'" % (dmId, searchStr))
if count == 0:
    SqlHelper.ExecuteScalar("insert into jimi_radar_video (dm_id,keyword,ctime) values (%d,'%s','%s')" % (
        dmId, searchStr, DateHelper.getDateNowStr()))

id = SqlHelper.ExecuteScalar("select id from jimi_radar_video where dm_id=%d and keyword='%s'" % (dmId, searchStr))


def doSave(numName, num, playName, play):
    sql = "update jimi_radar_video set %s = '%s' , %s = '%s' where id=%d" % (numName, num, playName, play, id)
    print sql
    SqlHelper.ExecuteNonQuery(sql)


def numMinusComma(num):
    return ''.join(num.split(','))


def playNumFix(num):
    strr = str(num)
    if u'万' in strr:
        res = strr.replace(u'万', '')
        return float(res) * 10000
    else:
        return strr


# 优酷 原站的写法
def youkuSearch():
    url = 'http://www.soku.com/search_video/q_' + searchStrAdd
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')

    # 相关视频数
    num = soup.find_all('div', 'vnum')[0].find_all('span')[0].string
    num = numMinusComma(num)

    print str(num) + '个视频'

    # 最大播放量
    # orderby=3 说明按播放数 我需要取播放数第一的播放量
    url = 'http://www.soku.com/search_video/q_' + searchStrAdd
    soup = ScrabHelper.getSoupFromURL(url, {'orderby': 3}, 'utf8')

    maxPlayed = soup.find_all('div', 'sk-vlist')[0].find('div', {'data-type': "tipHandle"}).find_all('span', 'pub')[
        0].string
    maxPlayed = numMinusComma(maxPlayed)

    print str(maxPlayed) + '次播放'
    print '优酷=================='
    print '======================'
    doSave('youku_num', num, 'youku_max_play', maxPlayed)


def aiqiyiSearch():
    # m_1_bitrate 1代表按默认相关度排序
    url = 'http://so.iqiyi.com/so/q_' + searchStrAdd + '_ctg__t_0_page_1_p_1_qc_0_rd__site_iqiyi_m_1_bitrate_'
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')
    num = soup.find_all('div', 'search_content')[0].find_all('em', 'keyword')[1].string
    if u'万' in num:
        num = num.replace(u'万', '')
        num = float(num) * 10000

    print str(num) + '个视频'

    # m_11_bitrate 11代表按播放量倒序
    url = 'http://so.iqiyi.com/so/q_' + searchStrAdd + '_ctg__t_0_page_1_p_1_qc_0_rd__site_iqiyi_m_11_bitrate_'
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')
    mostPlayUrl = soup.find_all('ul', 'mod_result_list')[0].find_all('a')[0].attrs['href']

    # print mostPlayUrl
    dr = webdriver.PhantomJS(executable_path='C:\\Python27\\Scripts\\phantomjs.exe')
    dr.get(mostPlayUrl)
    time.sleep(9)
    maxPlayed = dr.find_element_by_id("widget-playcount").text
    maxPlayed = numMinusComma(maxPlayed) or 0
    print str(maxPlayed) + '次播放'
    doSave('aiqiyi_num', num, 'aiqiyi_max_play', maxPlayed)


def souhuSearch():
    # 搜狐无法出现视频数量 借用爱奇艺的接口
    url = 'http://so.iqiyi.com/so/q_' + searchStrAdd + '_ctg__t_0_page_1_p_1_qc_0_rd__site_sohu_m_1_bitrate_'
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')
    num = soup.find_all('div', 'search_content')[0].find_all('em', 'keyword')[1].string
    num = playNumFix(num)

    print str(num) + '个视频'

    url = 'http://so.tv.sohu.com/mts?wd=' + searchStrAdd + '&o=1'
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')
    maxPlayed = soup.find_all('div', 'ssList')[0].find_all('li')[0].find_all('span', 'acount')[0].string
    maxPlayed = numMinusComma(maxPlayed)
    print maxPlayed

    doSave('souhu_num', num, 'souhu_max_play', maxPlayed)


def qqSearch():
    # m_1_bitrate 1代表按默认相关度排序
    url = 'http://so.iqiyi.com/so/q_' + searchStrAdd + '_ctg__t_0_page_1_p_1_qc_0_rd__site_qq_m_1_bitrate_'
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')
    num = soup.find_all('div', 'search_content')[0].find_all('em', 'keyword')[1].string
    num = playNumFix(num)

    print str(num) + '个视频'



    # sort%3D2 sort=2代表 排序等于2 就是最热排序
    url = 'https://v.qq.com/x/search/?ses=qid%3Dvc2GJPA2uIeNUvRfCybccR-9S_iE2kH1cfVRuMSzaZZf6FVAuGJfrg%26tabid_list%3D0%7C2%7C1%7C3%7C6%7C21%7C7%26tabname_list%3D全部%7C电视剧%7C电影%7C综艺%7C纪录片%7C汽车%7C其他' + \
          '&q=' + searchStr20 + \
          '&stag=4' + \
          '&filter=sort%3D2%26pubfilter%3D0%26duration%3D0%26tabid%3D0'
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')
    mostPlayUrl = soup.find_all('div', 'result_item')[0].find_all('a')[0].attrs['href']

    soup = ScrabHelper.getSoupFromURL(mostPlayUrl, {}, 'utf8')
    maxPlayed = soup.find_all('em', {'id': 'mod_cover_playnum'})[0].string
    maxPlayed = playNumFix(maxPlayed)
    print maxPlayed

    doSave('qq_num', num, 'qq_max_play', maxPlayed)


def bilibiliSearch():
    # b站需要把中文转成%的形式
    urlEncode = urllib.quote(searchStr)
    url = 'http://search.bilibili.com/video?keyword=' + urlEncode + '&order=click'

    soup = ScrabHelper.getSoupFromInterface(url, 'utf8')

    innerHTML = soup.find('p', 'so-info-total').string

    pat = re.compile(r'\d+')
    num = pat.findall(innerHTML)[0]

    print num

    maxPlayed = soup.find_all('span', 'watch-num')[0].get_text().strip()
    maxPlayed = playNumFix(maxPlayed)
    print maxPlayed

    doSave('bilibili_num', num, 'bilibili_max_play', maxPlayed)


# youkuSearch()
aiqiyiSearch()
# souhuSearch()
# qqSearch()
# bilibiliSearch()