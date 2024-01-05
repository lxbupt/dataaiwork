# _*_ coding : utf-8 _*_
# @Time : 2023/12/28 19:14
# @Author : 战斧牛排炖洋芋
# @File : SongDao
# @Project : dataaiwork
import pymysql

from dao.BaseDao import BaseDao


class SongDao(BaseDao):
    def __init__(self, config="mysql.json"):
        super().__init__(config)

    def insert_song(self, start, length, content):
        try:
            sql = "INSERT INTO t_songs (start, length, content) VALUES (%s, %s, %s)"
            params = (start, length, content)

            self.execute(sql, params)
            self.commit()
        except pymysql.DatabaseError as e:
            print(e)
            self.rollback()
        finally:
            self.close()

    def get_all_songs(self):
        try:
            sql = "SELECT * FROM t_songs"
            self.execute(sql)
            return self.fetchall()
        except pymysql.DatabaseError as e:
            print(e)
        finally:
            self.close()
