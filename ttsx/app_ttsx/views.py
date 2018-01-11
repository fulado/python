from django.shortcuts import render, redirect
from .models import UserInfo
from .dao import UserDao

# Create your views here.


def test(request):
    dao = UserDao(username='abcdef', password='123', email='')
    print(dao.is_user_exist())


def show_login(request):
    """
    显示用户登录界面
    :param request:
    :return:
    """
    return render(request, 'app_ttsx/login.html')


def show_reg(request):
    """
    跳转到用户注册页面
    :param request:
    :return:
    """
    return render(request, 'app_ttsx/register.html')


def user_register(request):
    """
    用户注册
    :param request:
    :return:
    """
    # 获取用户输入信息
    user_info = request.POST
    username = user_info.get('user_name')
    password = user_info.get('pwd')
    email = user_info.get('email')
    # allow = user_info.get('allow')

    # 创建UserInfo对象
    # user = UserInfo()
    # user.username = username
    # user.password = password
    # user.email = email
    # 创建dao对象


    # 写入数据库
    user.save()

    # 返回登录界面
    # return render(request, 'app_ttsx/login.html')
    return redirect('/login/')



