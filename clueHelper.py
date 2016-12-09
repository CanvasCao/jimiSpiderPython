# coding:utf-8



import re

class ClueHelper():
    # 静态方法
    @staticmethod
    # 根据JMS输入的clue找到对应的产品ID的方法
    def getProcessedClue(scrabId, clue):
        if scrabId == 1:
            # 匹配这个模型 找到 /1682.html 中的数字 就是id
            matches=re.findall(r"/(\d+)[.]{1}html", clue)
            return matches[0]
        elif scrabId==2:
            matches = re.findall(r"product/(\d+)/", clue)
            return matches[0]
        else:
            return None

