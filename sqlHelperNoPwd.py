# coding:utf-8


import MySQLdb

conn = MySQLdb.connect()
# conn = MySQLdb.connect(host='', user='', passwd='', db='', port=, charset="")


class sqlHelper():
    # 静态方法
    @staticmethod
    # 执行增删改的返回 int
    def ExecuteNonQuery(sql):
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.rowcount
            conn.commit()
            return res
        except:
            conn.rollback()

    @staticmethod
    # 返回单个值的方法
    def ExecuteScalar(sql):
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchone()
            return res[0]
        except:
            conn.rollback()

    @staticmethod
    # 返回dataTable
    def ExecuteDataTable(sql):
        try:
            cursor = conn.cursor()
            cursor.execute(sql)
            res = cursor.fetchall()
            return res
        except:
            conn.rollback()

# sqlHelper.ExecuteNonQuery("insert into jimi_radar_user (pwd,mobile,mail) values('1','2','3'),('1','2','33')")
# res = sqlHelper.ExecuteDataTable("select * from jimi_radar_site")
# for row in res:
# print row[0]
# print row[1]
# print row[2]
#     print row[3]
