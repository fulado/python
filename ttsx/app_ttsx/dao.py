from .models import *


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

    # def get_user_by_name(self, username):
    #     user_info = UserInfo.objects.filter(username=username)
    #     return user_info

    def is_user_exist(self):
        return UserInfo.objects.filter(username=self.user.username).exists()


