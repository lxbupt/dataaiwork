from dao.BaseDao import BaseDao


class UserDao(BaseDao):

    def getAllUserList(self):
        sql = "select * from t_user "
        result = self.execute(sql)
        return self.fetchall()

        pass

    pass
