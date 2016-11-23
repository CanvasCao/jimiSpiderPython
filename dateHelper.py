# coding:utf-8

import datetime
import time


class DateHelper():
    # 静态方法
    @staticmethod
    def getDateNowStr():
        return (datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S'))


