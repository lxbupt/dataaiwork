from dao.UserDao import UserDao


class UserService():

    def getAllUserList(self):
        userDao = UserDao()
        try:
            rset = userDao.getAllUserList()
        finally:
            userDao.close()
        return rset
        pass

    pass
