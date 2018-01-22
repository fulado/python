from .models import *
from .exceptions import *


class UserDao(object):
    # 插入一条UserInfo数据
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

    # 通过用户名判断数据是否存在
    @staticmethod
    def is_user_exist(username):
        return UserInfo.objects.filter(username=username).exists()

    # 通过用户名查询数据，返回结果列表，如果用户不存在返回空列表
    @staticmethod
    def get_user_by_name(username):
        return UserInfo.objects.filter(username=username)

    @staticmethod
    def get_user_sites_by_user_id(user_id):
        """
        通过用户的id查询用户的收获地址信息
        :param user_id:
        :return: 用户首地址对象列表
        """
        return UserSite.objects.filter(user_id=user_id)

    @staticmethod
    def insert_user_site(user_site):
        """
        插入一条数据到user_site表
        :param user_site:
        :return:
        """
        # 如果对象是UserSite类型，则存入数据库
        if isinstance(user_site, UserSite):
            try:
                user_site.save()
            except Exception as e:
                print(e)
                # 自定义异常，并将异常抛出
                raise DatabaseInsertException('数据库插入异常')
            else:
                return True
        else:
            raise DatabaseInsertException('对象不是UserSite类型')