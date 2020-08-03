from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from .models import User, Dept
import hashlib
import time
from tj8890.utils import MyPaginator
from django.http import HttpResponseRedirect
from tj8890.decorator import login_check


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
    login_error = False
    context = {'login_error': login_error}
    return render(request, 'user/login.html', context)


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
            login_error = False
        else:
            # 密码不同返回错误
            login_error = True
    else:
        login_error = True

    if login_error:
        # 登录失败
        context = {'username': username, 'password': password, 'login_error': login_error}
        return render(request, 'user/login.html', context)
    else:
        # 登录成功

        # 保存用户信息到session
        request.session['user_id'] = user.id

        if user.dept is not None:
            request.session['dept_id'] = user.dept.id
        else:
            request.session['dept_id'] = 1

        request.session['authority'] = user.authority
        request.session['real_name'] = user.real_name
        request.session['dept_name'] = user.dept.name

        default_time_begin = time.strftime('%Y-01-01', time.localtime())
        default_time_end = time.strftime('%Y-%m-%d', time.localtime())

        request.session['default_time_begin'] = default_time_begin
        request.session['default_time_end'] = default_time_end

        return HttpResponseRedirect('/item/main')


# 显示部门管理页
@login_check
def dept_show(request):
    # 获取所有的一级部门
    supervisor_list = Dept.objects.filter(supervisor__isnull=True).filter(is_delete=False)

    # 页面标题
    title = ['用户管理', '部门管理']

    # 获取用户选择的一级部门
    supervisor_id = int(request.GET.get('supervisor_id', 1))
    supervisor = Dept.objects.filter(id=supervisor_id)[0]
    # 查询二级部门
    dept_list = Dept.objects.filter(supervisor=supervisor_id)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))
    # 分页
    mp = MyPaginator()
    mp.paginate(dept_list, 10, page_num)

    context = {'title': title, 'supervisor_list': supervisor_list, 'supervisor': supervisor,
               'mp': mp}
    return render(request, 'user/dept.html', context)


# 添加部门
def dept_add(request):
    # 获取用户提交的信息
    grade = int(request.GET.get('grade', '1'))
    supervisor_id = int(request.GET.get('supervisor_id', '1'))
    dept_name = request.GET.get('dept_name')

    # 创建部门对象并对属性赋值
    dept = Dept()
    dept.name = dept_name
    if grade != 1:  # 不等与1, 添加的部门为下属科室
        dept.supervisor_id = supervisor_id

    # 存入数据库
    dept.save()

    # 设置url, 用户添加后可以直接看到添加的部门
    if grade != 1:  # 不等与1, 添加的部门为下属科室
        url = '/user/dept?supervisor_id=' + str(supervisor_id)
    else:
        url = '/user/dept?supervisor_id=' + str(dept.id)

    return HttpResponseRedirect(url)


# 编辑部门
def dept_modify(request):
    # 获取用户提交的编辑信息
    dept_id = int(request.GET.get('dept_id'))
    dept_name = request.GET.get('dept_name')
    supervisor_id = int(request.GET.get('supervisor_id', '0'))

    dept_list = Dept.objects.filter(id=dept_id)
    if len(dept_list) > 0:
        dept = dept_list[0]
    dept.name = dept_name

    # 如果supervisor_id不等于0, 修改该属性; 等于0说明是一级单位, 此字段为空
    if supervisor_id != 0:
        dept.supervisor_id = supervisor_id
        url = '/user/dept?supervisor_id=' + str(supervisor_id)
    else:
        url = '/user/dept?supervisor_id=' + str(dept.id)

    dept.save()

    return HttpResponseRedirect(url)


# 删除部门
def dept_del(request):
    # 获取用户提交的编辑信息
    dept_id = int(request.GET.get('dept_id'))
    supervisor_id = int(request.GET.get('supervisor_id', '0'))

    # 如果supervisor_id==0, 说明是一级部门, 需要先删除所有部门下属科室
    if supervisor_id == 0:
        dept_list = Dept.objects.filter(supervisor=dept_id)
        for dept in dept_list:
            dept.delete()
        url = '/user/dept'
    else:
        url = '/user/dept?supervisor_id=' + str(supervisor_id)

    supervisor_list = Dept.objects.filter(id=dept_id)
    if len(supervisor_list) > 0:
        dept = supervisor_list[0]
        dept.delete()

    return HttpResponseRedirect(url)


# 显示用户管理页
@login_check
def user_show(request):
    # 获取所有的一级部门
    dept_list = Dept.objects.filter(supervisor__isnull=True).filter(is_delete=False)

    # 页面标题
    title = ['用户管理', '人员管理']

    # 获取用户选择的部门id, 默认是0
    # supervisor_id = int(request.GET.get('supervisor_id', 0))
    dept_id = int(request.GET.get('dept_id', 0))

    request.session['dept_id'] = dept_id

    # 查询二级部门
    # 如果一级部门id等于0, 取一级部门列表中的一个作为上级部门
    # if supervisor_id == 0:
    #     dept_list = Dept.objects.filter(supervisor=supervisor_list[0].id)
    #     # 查询全部人员
    #     user_list = User.objects.all()
    # else:
    #     dept_list = Dept.objects.filter(supervisor=supervisor_id)
    #     # 查询用户指定
    #     # 如果二级部门id等于0, 查询全部的属于该二级部门上级部门的用户
    #     if dept_id == 0:
    #         user_list = User.objects.filter(dept=supervisor_id)
    #     else:
    #         # 如果二级部门id不等于0, 查询该二级部门下的全部人员
    #         user_list = User.objects.filter(dept=dept_id)

    # 如果部门id等于0, 查询全部的属id为1的部门的用户
    if dept_id == 0:
        user_list = User.objects.all()
    else:
        # 如果二级部门id不等于0, 查询该二级部门下的全部人员
        user_list = User.objects.filter(dept=dept_id)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))
    # 分页
    mp = MyPaginator()
    mp.paginate(user_list, 10, page_num)

    context = {'title': title, 'dept_list': dept_list, 'dept_id': dept_id, 'mp': mp}
    return render(request, 'user/user.html', context)


# 二级部门查询
def dept_search(request):
    supervisor_id = request.GET.get('supervisor_id', 0)
    dept_list = Dept.objects.filter(supervisor=supervisor_id)

    # 构建返回的Json格式数据
    data = []
    for dept in dept_list:
        dept_info = {'id': dept.id, 'name': dept.name}
        data.append(dept_info)

    return JsonResponse({'dept_list': data})


# 添加人员
def user_add(request):
    # 获取用户信息
    # supervisor_id = int(request.GET.get('supervisor_id'))
    username = request.GET.get('username')
    password = request.GET.get('password')
    real_name = request.GET.get('real_name', None)
    dept_id = int(request.GET.get('dept_id', None))
    duty = request.GET.get('duty', None)
    number = request.GET.get('number', None)
    phone = request.GET.get('phone', None)
    authority = int(request.GET.get('authority', None))

    user = User()
    user.username = username
    user.password = hashlib.sha1(password.encode('utf8')).hexdigest()  # 密码需要加密
    if real_name is not None:
        user.real_name = real_name
    if dept_id is not None:
        user.dept_id = dept_id
    if duty is not None:
        user.duty = duty
    if number is not None:
        user.number = number
    if phone is not None:
        user.phone = phone
    if authority is not None:
        user.authority = authority

    user.save()
    url = '/user/user?dept_id=%d' % request.session.get('dept_id', 0)

    return HttpResponseRedirect(url)


# 编辑人员
def user_modify(request):
    # supervisor_id = int(request.GET.get('supervisor_id'))
    dept_id = int(request.GET.get('dept_id'))
    real_name = request.GET.get('real_name')
    username = request.GET.get('username')
    duty = request.GET.get('duty')
    number = request.GET.get('number')
    authority = request.GET.get('authority')
    phone = request.GET.get('phone')
    user_id = int(request.GET.get('user_id'))

    user = User.objects.filter(id=user_id)[0]

    user.dept_id = dept_id
    user.real_name = real_name
    user.username = username
    user.duty = duty
    user.number = number
    user.authority = authority
    user.phone = phone

    user.save()
    url = '/user/user?dept_id=%d' % request.session.get('dept_id', 0)

    return HttpResponseRedirect(url)


# 删除人员
def user_del(request):
    # supervisor_id = int(request.GET.get('supervisor_id'))
    # dept_id = int(request.GET.get('dept_id'))
    user_id = int(request.GET.get('user_id'))

    user = User.objects.filter(id=user_id)[0]

    user.delete()
    url = '/user/user?dept_id=%d' % request.session.get('dept_id', 0)

    return HttpResponseRedirect(url)


# 重置密码
def reset_password(request):
    user_id = int(request.POST.get('user_id'))
    password = request.POST.get('password')

    user = User.objects.filter(id=user_id)[0]
    user.password = hashlib.sha1(password.encode('utf8')).hexdigest()  # 密码需要加密

    user.save()
    return HttpResponseRedirect('/user/user')


# 退出登录
def logout(request):
    request.session.clear()
    request.session.flush()

    return HttpResponseRedirect('/')
