from .models import *
from .exceptions import *


class UserDao(object):
    def __init__(self, username, password, email):
        self.user = UserInfo()
        self.user.username = username
        self.user.password = password
        self.user.email = email

    def register(self):
        """
        用户注册
        :return: 成功返回True， 失败返回False
        """
        if self.is_user_exist(self.user.username):
            # 用户已存在注册失败
            return False
        else:
            # 添加用户信息到数据库，返回注册成功
            self.user.save()
            return True

    @staticmethod
    def insert(user):
        # 如果对象是UserInfo类型，则存入数据库
        if isinstance(user, UserInfo):
            try:
                user.save()
            except Exception:
                # 自定义异常，并将异常抛出
                raise DatabaseInsertException('数据库插入异常')
        else:
            raise DatabaseInsertException('对象不是UserInfo类型')

    # def get_user_by_name(self, username):
    #     user_info = UserInfo.objects.filter(username=username)
    #     return user_info

    @staticmethod
    def is_user_exist(username):
        return UserInfo.objects.filter(username=username).exists()


