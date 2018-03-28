from django.shortcuts import render
from django.shortcuts import HttpResponse
from .models import User, Dept
import hashlib
from tj8890.utils import MyPaginator

# Create your views here.


# 创建超级用户
def create_admin(request):
    user = User()
    user.username = 'admin'
    user.password = hashlib.sha1('123456'.encode('utf8')).hexdigest()
    user.real_name = '管理员'
    try:
        user.save()
    except Exception as e:
        print(e)
        return HttpResponse('创建失败')
    else:
        return HttpResponse('创建成功')


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
        return HttpResponse('登陆成功')


# 显示部门管理页
def dept(request):
    # 获取所有的一级部门
    supervisor_list = Dept.objects.filter(supervisor__isnull=True).filter(is_delete=False)

    # 页面标题
    title = ['用户管理', '部门管理']

    # 获取用户选择的一级部门id
    supervisor_id = int(request.GET.get('supervisor_id', 1))
    # 查询二级部门
    dept_list = Dept.objects.filter(supervisor=supervisor_id)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))
    # 分页
    mp = MyPaginator()
    mp.paginate(dept_list, 10, page_num)

    context = {'title': title, 'supervisor_list': supervisor_list, 'supervisor_id': supervisor_id,
               'mp': mp}
    return render(request, 'user/dept.html', context)
