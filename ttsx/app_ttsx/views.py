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
    # 获取用户输入信息, 创建UserInfo对象
    user = UserInfo()
    user_info = request.POST
    user.username = user_info.get('user_name')
    user.password = user_info.get('pwd')
    user.email = user_info.get('email')

    # 调用dao，判断是否可以写入数据库
    if UserDao.is_user_exist(user.username):
        # 用户已存在注册失败
        result = '注册失败，用户已存在'
    else:
        # 添加用户信息到数据库，返回注册成功
        try:
            UserDao.insert(user)
        except Exception as e:
            print(e)
            result = '注册失败，请重试'
        else:
            result = '注册成功'

    # 跳转到注册结果页面
    context = {'result': result}
    # return render(request, 'app_ttsx/login.html')
    return render(request, 'app_ttsx/register_result.html', context)



