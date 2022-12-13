import pymysql
import pymysql.cursors

from ..config import HOST, USER, PASSWD, DB

class DataBase():

    def __init__ (self):

        self.HOST = HOST
        self.USER = USER
        self.PASSWD = PASSWD
        self.DB = DB 

    def SQL (self, sql):
        db = pymysql.connect(host = self.HOST,
                             user = self.USER,
                             passwd = self.PASSWD,
                             db = self.DB,
                             charset = 'utf8')

        cursor = db.cursor()
        cursor.execute(sql)


        if (sql.find("SELECT") != -1): return cursor.fetchall()

        else: db.commit()

        db.close()