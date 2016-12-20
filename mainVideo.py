# coding:utf-8

import requests
from sqlHelper import SqlHelper
from scrabHelper import ScrabHelper
from dateHelper import DateHelper
from selenium import webdriver
import time


dmId = 1
searchStr = '兰蔻 小黑瓶'


def numMinusComma(num):
    return ''.join(num.split(','))


# 不存在根据 type 判断视频网站的情况


# 优酷 原站的写法
def youkuSearch():
    searchArr = searchStr.split(' ')
    youkuSearchStr = '+'.join(searchArr)

    url = 'http://www.soku.com/search_video/q_' + youkuSearchStr
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')

    # 相关视频数
    num = soup.find_all('div', 'vnum')[0].find_all('span')[0].string
    num = numMinusComma(num)

    print str(num) + '个视频'

    # 最大播放量
    # orderby=3 说明按播放数 我需要取播放数第一的播放量
    url = 'http://www.soku.com/search_video/q_' + youkuSearchStr
    soup = ScrabHelper.getSoupFromURL(url, {'orderby': 3}, 'utf8')

    maxPlayed = soup.find_all('div', 'sk-vlist')[0].find('div', {'data-type': "tipHandle"}).find_all('span', 'pub')[
        0].string
    maxPlayed = numMinusComma(maxPlayed)

    print str(maxPlayed) + '次播放'
    print '优酷=================='
    print '======================'


# youkuSearch()


def aiqiyiSearch():
    searchArr = searchStr.split(' ')
    aiqiyiSearchStr = '+'.join(searchArr)

    url = 'http://so.iqiyi.com/so/q_' + aiqiyiSearchStr + '_ctg__t_0_page_1_p_1_qc_0_rd__site_iqiyi_m_1_bitrate_'
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')
    num = soup.find_all('div', 'search_content')[0].find_all('em', 'keyword')[1].string
    if u'万' in num:
        num = num.replace(u'万', '')
    num = float(num) * 10000

    print str(num) + '个视频'

    url = 'http://so.iqiyi.com/so/q_' + aiqiyiSearchStr + '_ctg__t_0_page_1_p_1_qc_0_rd__site_iqiyi_m_11_bitrate_'
    soup = ScrabHelper.getSoupFromURL(url, {}, 'utf8')
    mostPlayUrl = soup.find_all('ul', 'mod_result_list')[0].find_all('a')[0].attrs['href']

    dr = webdriver.PhantomJS(executable_path='C:\\Python27\\Scripts\\phantomjs.exe')
    dr.get(mostPlayUrl)
    time.sleep(8)
    maxPlayed = dr.find_element_by_id("widget-playcount").text
    maxPlayed = numMinusComma(maxPlayed)
    print str(maxPlayed) + '次播放'

    # print soup2.find_all('span',{'id':'widget-playcount'})[0].string


# aiqiyiSearch()

def souhuSearch():
    pass