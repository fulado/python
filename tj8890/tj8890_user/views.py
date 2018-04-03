from django.shortcuts import render
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from .models import User, Dept
import hashlib
from tj8890.utils import MyPaginator
from django.http import HttpResponseRedirect


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
def user_show(request):
    # 获取所有的一级部门
    supervisor_list = Dept.objects.filter(supervisor__isnull=True).filter(is_delete=False)

    # 页面标题
    title = ['用户管理', '人员管理']

    # 获取用户选择的部门id, 默认是0
    supervisor_id = int(request.GET.get('supervisor_id', 0))
    dept_id = int(request.GET.get('dept_id', 0))

    # 查询二级部门
    # 如果一级部门id等于0, 取一级部门列表中的一个作为上级部门
    if supervisor_id == 0:
        dept_list = Dept.objects.filter(supervisor=supervisor_list[0].id)
        # 查询全部人员
        user_list = User.objects.all()
    else:
        dept_list = Dept.objects.filter(supervisor=supervisor_id)
        # 查询用户指定
        # 如果二级部门id等于0, 查询全部的属于该二级部门上级部门的用户
        if dept_id == 0:
            user_list = User.objects.filter(dept=supervisor_id)
        else:
            # 如果二级部门id不等于0, 查询该二级部门下的全部人员
            user_list = User.objects.filter(dept=dept_id)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))
    # 分页
    mp = MyPaginator()
    mp.paginate(user_list, 10, page_num)

    context = {'title': title, 'supervisor_list': supervisor_list, 'dept_list': dept_list,
               'supervisor_id': supervisor_id, 'dept_id': dept_id, 'mp': mp}
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

    return HttpResponseRedirect('/user/user')
