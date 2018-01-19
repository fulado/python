from django.shortcuts import render, redirect
from .models import UserInfo, UserSite
from .dao import UserDao
import hashlib

# Create your views here.


def test(request):
    dao = UserDao(username='abcdef', password='123', email='')
    print(dao.is_user_exist())


def show_index(request):
    """
    显示系统首页
    :param request:
    :return:
    """
    return render(request, 'app_ttsx/index.html')


def show_login(request):
    """
    显示用户登录界面
    :param request:
    :return:
    """
    # 获取Cookie中保存的用户名
    if 'username' in request.COOKIES.keys():
        username = request.COOKIES.get('username')
    else:
        username = ''
    context = {'username': username}

    return render(request, 'app_ttsx/login.html', context)


def show_reg(request):
    """
    跳转到用户注册页面
    :param request:
    :return:
    """
    return render(request, 'app_ttsx/register.html')


def show_user_site(request):
    """
    显示用户地址页面
    :param request:
    :return:
    """

    user_id = request.session.get('user_id')

    # 修改收获地址
    site_info = request.POST
    print(user_id)
    print(site_info.get('site'))

    user_site = UserSite()
    user_site.receiver = site_info.get('receiver')
    user_site.site = site_info.get('site')
    user_site.zip = site_info.get('zip')
    user_site.phone = site_info.get('phone')
    user_site.user



    return render(request, 'app_ttsx/user_center_site.html')


def show_user_info(request):
    """
    显示用户个人信息页面
    :param request:
    :return:
    """
    # 取出session中存储的个人信息
    user_id = request.session.get('user_id')
    # user_sites =

    if user_id is not None:
        context = {'user_id': user_id}
    else:
        context = {}

    return render(request, 'app_ttsx/user_center_info.html', context)


# 用户注册服务
def register_service(request):
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
        # 对用户密码进行加密
        user.password = hashlib.sha1(user.password.encode('utf-8')).hexdigest()

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


# 用户登录服务
def login_server(request):
    """
    验证用户登录信息
    :param request:
    :return:
    """
    # 获取用户输入信息
    username = request.POST.get('username')
    password = request.POST.get('pwd')
    remember = request.POST.get('remember')  # 勾选后返回一个str对象，值是'on'；不勾选返回None

    # 通过用户名在数据库中查询用户
    users = UserDao.get_user_by_name(username)

    # 查询结果为空列表，返回用户不存在
    if len(users) == 0:
        result = '用户不存在'
    # 查询结果不为空，验证密码
    else:
        user = users[0]
        password = hashlib.sha1(password.encode('utf-8')).hexdigest()

        # 密码不一致，返回用户名密码不匹配
        if password != user.password:
            result = '用户名密码不匹配'
        else:
            # 密码一致，登录成功
            result = '登录成功'

            # 登录成功后将用户信息保存在session中(存不了自定义类的实例？？？)
            request.session['user_id'] = user.id
            request.session.set_expiry(0)

    context = {'result': result}
    response = render(request, 'app_ttsx/login_result.html', context)

    # 使用Cookie保存用户名
    # 如果用户勾选，保存到Cookie，否则清除Cookie
    if remember is not None:
        response.set_cookie('username', username)
    else:
        response.delete_cookie('username')

    return response
