# coding:utf-8

import datetime
import time


class DateHelper():
    # 静态方法
    @staticmethod
    # 返回当前时间字符串
    def getDateNowStr():
        return (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))


    @staticmethod
    # 根据日期返回秒数
    def getDateInt(dateStr):
        return int(time.mktime(dateStr.timetuple()))

