import pymysql
import json
import os


class BaseDao:
    """
    数据库访问基类
    """

    def __init__(self, config="mysql.json"):
        self.__config = json.load(open(os.path.dirname(__file__) + os.sep + config, mode="r",
                                       encoding="utf-8"))  # 读取mysql.json配置文件，转为python对象
        self.__conn = None
        self.__cursor = None

        pass

    def getConnection(self):
        if self.__conn != None:
            return self.__conn
            pass
        self.__conn = pymysql.connect(
            **self.__config)  # **{"host":"127.0.0.1", "user":"root", "password":"root", "database":"db_jobsdata", "port":3306, "charset":"utf8"}
        return self.__conn
        pass

    def execute(self, sql, params=[], ret="dict"):
        result = 0
        try:
            self.__conn = self.getConnection()
            if ret == "dict":
                self.__cursor = self.__conn.cursor(pymysql.cursors.DictCursor)  # 返回字典数据
            else:
                self.__cursor = self.__conn.cursor()  # 返回元组数据
            result = self.__cursor.execute(sql, params)
        except pymysql.DatabaseError as e:
            print(e)
            pass

        return result
        pass

    def fetchone(self):
        if self.__cursor:
            return self.__cursor.fetchone()
        pass

    def fetchall(self):
        if self.__cursor:
            return self.__cursor.fetchall()
            pass

    def close(self):
        if self.__cursor:
            self.__cursor.close()
            pass

        if self.__conn:
            self.__conn.close()
        pass

    def commit(self):
        if self.__conn:
            self.__conn.commit()
        pass

    def rollback(self):
        if self.__conn:
            self.__conn.rollback()
            pass
        pass

    pass
