from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from .models import User, Location, Vehicle
from tj_orta.utils import MyPaginator
from .utils import generate_certification
import hashlib
import time
import random

# Create your views here.


# 显示主页面
def main(request):
    return render(request, 'main.html')


# 显示企业管理页面
def enterprise(request):
    # 查询企业信息
    enterprise_list = User.objects.filter(authority_id=1).filter(is_delete=False).order_by('-id')

    # 获取企业搜索信息
    search_name = request.GET.get('search_name', '')
    # 在结果集中搜索包含搜索信息的企业
    if search_name != '':
        enterprise_list = enterprise_list.filter(enterprise_name__contains=search_name)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 创建分页
    mp = MyPaginator()
    mp.paginate(enterprise_list, 10, page_num)

    context = {'mp': mp, 'search_name': search_name}
    
    return render(request, 'enterprise.html', context)


# 添加企业
def enterprise_add(request):
    # 获取企业信息
    username = request.POST.get('username')                 # 帐号
    password = request.POST.get('password')                 # 密码 不能使用'12345678'
    authority = int(request.POST.get('author'))             # 权限等级
    enterprise_name = request.POST.get('companyName', '')   # 企业名称
    enterprise_phone = request.POST.get('tel', '')          # 企业联系方式
    legal_person = request.POST.get('corName', '')          # 法人
    organization_code = request.POST.get('orgCode', '')     # 组织机构代码
    contact = request.POST.get('contect', '')               # 联系人
    contact_phone = request.POST.get('conMobile', '')       # 联系人电话

    # 创建user
    user = User()
    user.username = username
    user.password = hashlib.sha1(password.encode('utf8')).hexdigest()
    user.authority_id = authority
    user.enterprise_name = enterprise_name
    user.enterprise_phone = enterprise_phone
    user.legal_person = legal_person
    user.organization_code = organization_code
    user.contact = contact
    user.contact_phone = contact_phone

    # 存入数据库
    try:
        user.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/enterprise')


# 判断用户名是否已经存在
def is_user_exist(request):
    username = request.GET.get('username')
    user_id = request.GET.get('id', 0)

    if user_id == 0:
        is_exist = User.objects.filter(username=username).exists()
    else:
        is_exist = User.objects.filter(username=username).exclude(id=user_id).exists()

    return JsonResponse({'is_exist': is_exist})


# 编辑企业信息
def enterprise_modify(request):
    # 获取企业信息
    username = request.POST.get('username')                 # 帐号
    password = request.POST.get('password')                 # 密码
    authority = int(request.POST.get('author'))             # 权限等级
    enterprise_name = request.POST.get('companyName', '')   # 企业名称
    enterprise_phone = request.POST.get('tel', '')          # 企业联系方式
    legal_person = request.POST.get('corName', '')          # 法人
    organization_code = request.POST.get('orgCode', '')     # 组织机构代码
    contact = request.POST.get('contect', '')               # 联系人
    contact_phone = request.POST.get('conMobile', '')       # 联系人电话
    user_id = request.POST.get('id')                        # 用户id

    # 查询用户
    user = User.objects.filter(id=user_id).filter(is_delete=False)[0]

    # 保存user信息
    user.username = username
    user.authority_id = authority
    user.enterprise_name = enterprise_name
    user.enterprise_phone = enterprise_phone
    user.legal_person = legal_person
    user.organization_code = organization_code
    user.contact = contact
    user.contact_phone = contact_phone
    # 如果密码不能8个'#', 需要修改密码
    if password != r'########':
        user.password = hashlib.sha1(password.encode('utf8')).hexdigest()
        print('change password')

    # 存入数据库
    try:
        user.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/enterprise')


# 删除用户信息
def enterprise_delete(request):
    # 获取用户id
    user_id = request.POST.get('id')  # 用户id

    # 查询user
    user = User.objects.filter(id=user_id).filter(is_delete=False)[0]

    # 删除user
    try:
        user.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/enterprise')


# 显示车辆管理页面
def vehicle(request):
    # 查询车辆所在地数据
    location_list = Location.objects.all()

    # 查询该企业的所有车辆数据
    vehicle_list = Vehicle.objects.filter(enterprise_id=4).order_by('-modify_time')

    # 获取车辆搜索信息
    search_name = request.GET.get('search_name', '')

    # 在结果集中搜索包含搜索信息的车辆, 车辆搜索功能不完善, 指数如车牌号,不要输入号牌所在地
    if search_name != '':
        vehicle_list = vehicle_list.filter(number__contains=search_name)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 创建分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, page_num)

    context = {'location_list': location_list, 'mp': mp, 'search_name': search_name}

    return render(request, 'vehicle.html', context)


# 显示审核页面
def verify(request):
    return render(request, 'verify.html')


# 添加车辆
def vehicle_add(request):
    # 获取用户提交的车辆信息
    location_id = int(request.GET.get('location'))          # 车牌所在地
    number = request.GET.get('number')                      # 号牌号码
    engine = request.GET.get('engine')                      # 发动机型号
    vehicle_type_id = int(request.GET.get('vehicle_type'))     # 车辆类型
    vehicle_model = request.GET.get('vehicle_model')        # 车辆型号
    register_date = request.GET.get('register_date')        # 车辆注册日期
    route = request.GET.get('route')                        # 路线

    # 创建车辆数据对象
    truck = Vehicle()
    truck.vehicle_type_id = vehicle_type_id
    truck.location_id = location_id
    truck.number = number
    truck.engine = engine
    truck.vehicle_model = vehicle_model
    truck.register_date = register_date
    truck.route = route
    truck.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    truck.enterprise_id = 4             # 测试, 先设置为4

    # 存入数据库
    try:
        truck.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/vehicle')


# 编辑车辆
def vehicle_modify(request):
    # 获取用户提交的车辆信息
    location_id = int(request.GET.get('location'))          # 车牌所在地
    number = request.GET.get('number')                      # 号牌号码
    engine = request.GET.get('engine')                      # 发动机型号
    vehicle_type_id = int(request.GET.get('vehicle_type'))  # 车辆类型
    vehicle_model = request.GET.get('vehicle_model')        # 车辆型号
    register_date = request.GET.get('register_date')        # 车辆注册日期
    route = request.GET.get('route')                        # 路线
    vehicle_id = request.GET.get('vehicle_id')              # id

    # 根据id查询车辆
    truck = Vehicle.objects.filter(id=vehicle_id)[0]
    truck.vehicle_type_id = vehicle_type_id
    truck.location_id = location_id
    truck.number = number
    truck.engine = engine
    truck.vehicle_model = vehicle_model
    truck.register_date = register_date
    truck.route = route
    truck.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # 审核状态变为未提交
    truck.status_id = 1

    # 存入数据库
    try:
        truck.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/vehicle')


# 删除车辆
def vehicle_delete(request):
    # 获取车辆id
    vehicle_id = request.GET.get('vehicle_id')  # 车辆i

    # 根据id查询车辆
    truck = Vehicle.objects.filter(id=vehicle_id)[0]

    # 删除车辆
    try:
        truck.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/vehicle')


# 提交车辆
def vehicle_submit(request):
    vehicle_id = request.GET.get('vehicle_id')  # id

    # 根据id查询车辆
    truck = Vehicle.objects.filter(id=vehicle_id)[0]

    # 审核状态变为通过
    truck.status_id = 4

    # 生成通行证图片
    # 生成通行证id, 201805+车牌号+三位随机数
    certification_id = '%s%s%d%d%d' % (time.strftime('%Y%m', time.localtime()), truck.number, random.randint(0, 9),
                                       random.randint(0, 9), random.randint(0, 9))
    truck.cert_id = certification_id
    limit_data = '2018年5月31日'  # 暂时写为5月底
    number = '%s%s' % (truck.location.name, truck.number)
    enterprise_name = truck.enterprise.enterprise_name
    route = truck.route
    # 图片文件名
    file_name = '%s.jpg' % certification_id
    truck.file_name = file_name

    generate_certification(certification_id, limit_data, number, enterprise_name, route, file_name)

    # 存入数据库
    try:
        truck.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/vehicle')
