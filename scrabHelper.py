# coding:utf-8


import pycurl
from bs4 import BeautifulSoup
from StringIO import StringIO


class ScrabHelper():
    # 静态方法
    @staticmethod
    def getSoupFromHtml(html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    @staticmethod
    def getHtmlFromInterface(interfaceName,codeName):
        buffer = StringIO()
        c = pycurl.Curl()
        c.setopt(c.URL, interfaceName)
        c.setopt(c.WRITEDATA, buffer)
        c.perform()
        c.close()
        body = buffer.getvalue()

        # print body gb2312 utf-8
        return body.decode(codeName, 'ignore')

    # 类方法
    @classmethod
    def getSoupFromInterface(self, interfaceName,codeName):
        html = self.getHtmlFromInterface(interfaceName,codeName)
        return self.getSoupFromHtml(html)


