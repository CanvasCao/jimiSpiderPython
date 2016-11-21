# coding:utf-8

import sqlHelper

dmId = 1

scrabJson = {"data": [{
                          "scrabId": 1,
                          "clue": '135143'
                      }, {
                          "scrabId": 2,
                          "clue": '135111'
                      }]}

scrabArray = scrabJson['data']
for ele in scrabArray:
    scrabId = str(ele['scrabId'])
    clue = ele['clue']
    row=sqlHelper.sqlHelper.ExecuteDataTable('select * from jimi_radar_scrab where id='+scrabId)[0]
    print row[0]
    print row[1]
