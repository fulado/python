from django.shortcuts import render
from .models import User
import hashlib

# Create your views here.


# 显示登录页
def login(request):
    return render(request, 'user/login.html')


# 登录服务
def login_service(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    # 根据用户名查询用户
    user_list = User.objects.filter(username=username)
    # 如果用户不存在返回错误
    if len(user_list) > 0:
        # 如果用户存在, 对比密码
        # 对密码进行sha1加密
        password_encrypted = hashlib.sha1(password.encode('utf-8')).hexdigest()
        user = user_list[0]

        if password_encrypted == user.password:
            error = False
        else:
            # 密码不同返回错误
            error = True
    else:
        error = True
    print(error)
    if error:
        context = {'username': username, 'password': password, 'error': error}
        return render(request, 'user/login.html', context)
    else:
        return render(request, 'user/success.html')
