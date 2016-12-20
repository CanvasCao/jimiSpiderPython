# coding:utf-8

import datetime
import time


class DateHelper():
    # 静态方法
    @staticmethod
    # 返回当前时间字符串
    def getDateNowStr():
        return (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))


