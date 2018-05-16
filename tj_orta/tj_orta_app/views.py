from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import HttpResponse
from .models import User, Vehicle, SysStatus, Backup1
from tj_orta.utils import MyPaginator
from .utils import generate_certification
from tj_orta import settings
from .decorator import login_check
import hashlib
import time
import datetime
import calendar
import random
import os
import xlrd
import xlwt
from PIL import Image, ImageDraw, ImageFont
import io
# Create your views here.


# 创建超级用户
def create_admin(request):
    user = User()
    user.username = 'admin'
    user.password = hashlib.sha1('yxtc_20921'.encode('utf8')).hexdigest()
    user.authority_id = 99
    try:
        user.save()
    except Exception as e:
        print(e)
        return HttpResponse('创建失败')
    else:
        return HttpResponse('创建成功')


# 验证码
def check_code(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 255, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD23EFGHJK456LMNPQRS789TUVWXYZ'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 设置字体
    font = ImageFont.truetype(r"%s/simsun.ttf" % settings.FONTS_DIR, 23)
    # 字体颜色
    fontcolor = (255, 243, 67)
    # 绘制4个字
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['check_code'] = rand_str
    request.session.set_expiry(0)  # 浏览器关闭后清除session
    # 内存文件操作
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# 显示登录页
def login(request):
    # session中的user_id不等于空直接跳转到主页
    user_id = request.session.get('user_id', '')
    if user_id != '':
        return HttpResponseRedirect('/main')

    msg = request.GET.get('msg', '')

    context = {'msg': msg}

    return render(request, 'login.html', context)


# 登陆服务
def login_handle(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    code = request.POST.get('check_code').upper()

    session_code = request.session.get('check_code')

    if code != session_code:
        msg = '验证码错误'
        return HttpResponseRedirect('/?msg=%s' % msg)

    user_list = User.objects.filter(username=username)
    if len(user_list) == 0:
        msg = '用户不存在'
        return HttpResponseRedirect('/?msg=%s' % msg)

    user = user_list[0]
    if hashlib.sha1(password.encode('utf8')).hexdigest() != user.password:
        msg = '用户名或密码错误'
        return HttpResponseRedirect('/?msg=%s' % msg)

    # 根据user.id获取用户权限, 2-环保局, 3-交管局
    if user.id != 0:
        authority = User.objects.get(id=user.id).authority.id
    else:
        authority = 0

    # 把user.id保存到session中
    request.session.set_expiry(0)  # 浏览器关闭后清除session
    request.session['user_id'] = user.id
    request.session['authority_id'] = authority

    return HttpResponseRedirect('/main')


# 退出登录
def logout(request):
    request.session.clear()
    request.session.flush()

    return HttpResponseRedirect('/')


# 显示主页面
@login_check
def main(request):
    user_id = request.session.get('user_id', '')

    if user_id != '':
        user = User.objects.filter(id=user_id)[0]
    # 这里有点问题, user不一定有值, 后面得修改
    context = {'user': user}

    return render(request, 'main.html', context)


# 显示企业管理页面
@login_check
def enterprise(request):
    # 查询企业信息
    enterprise_list = User.objects.filter(is_delete=False).exclude(id=1).order_by('id')

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
    password = request.POST.get('password')                 # 密码 不能使用'########'
    authority = int(request.POST.get('author'))             # 权限等级
    enterprise_name = request.POST.get('companyName', '')   # 企业名称
    enterprise_phone = request.POST.get('tel', '')          # 企业联系方式
    legal_person = request.POST.get('corName', '')          # 法人
    organization_code = request.POST.get('orgCode', '')     # 组织机构代码
    contact = request.POST.get('contect', '')               # 联系人
    contact_phone = request.POST.get('conMobile', '')       # 联系人电话
    limit_number = request.POST.get('limit_number', '1')    # 申请通行证上限
    if limit_number is not None:
        if limit_number.isdigit():
            limit_number = int(limit_number)
        else:
            limit_number = 1

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
    user.limit_number = limit_number

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
    limit_number = request.POST.get('limit_number', '1')  # 申请通行证上限
    if limit_number is not None:
        if limit_number.isdigit():
            limit_number = int(limit_number)
        else:
            limit_number = 1

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
    user.limit_number = limit_number
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
@login_check
def vehicle(request):
    # 获取session中的user_id, 根据user_id查询企业
    user_id = int(request.session.get('user_id', ''))

    # 查询已提交申请车辆数, 限制提交车辆数
    user = User.objects.get(id=user_id)
    limit_number = user.limit_number
    applied_number = user.applied_number

    # 查询该企业的所有车辆数据
    if user_id != '' and user_id != 1:
        vehicle_list = Vehicle.objects.filter(enterprise_id=user_id).order_by('id')
    else:
        vehicle_list = Vehicle.objects.all().order_by('id')

    # 获取用户选择的车辆查询状态
    status = int(request.GET.get('status', 0))

    # 根据不同状态过滤车辆
    if status == 2:
        vehicle_list = vehicle_list.filter(status_id__in=[2, 3]).order_by('id')
    elif status != 0:
        vehicle_list = vehicle_list.filter(status_id=status).order_by('id')

    # 获取车辆搜索信息
    number = request.GET.get('number', '')

    # 在结果集中搜索包含搜索信息的车辆, 车辆搜索功能不完善, 指数如车牌号,不要输入号牌所在地
    if number != '':
        vehicle_list = vehicle_list.filter(number__contains=number)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 创建分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, page_num)

    # 查询是否允许提交
    allow_submit = SysStatus.objects.get(id=1).allow_submit

    context = {'mp': mp, 'number': number, 'limit_number': limit_number, 'applied_number': applied_number,
               'user_id': user_id, 'status': status, 'allow_submit': allow_submit}

    return render(request, 'vehicle.html', context)


# 添加车辆
def vehicle_add(request):
    # 获取用户提交的车辆信息
    # location_id = int(request.GET.get('location'))          # 车牌所在地
    number = request.GET.get('number')                      # 号牌号码
    engine = request.GET.get('engine')                      # 发动机型号
    vehicle_type_id = int(request.GET.get('vehicle_type'))     # 车辆类型
    vehicle_model = request.GET.get('vehicle_model')        # 车辆型号
    register_date = request.GET.get('register_date')        # 车辆注册日期
    route = request.GET.get('route')                        # 路线

    # 创建车辆数据对象
    truck = Vehicle()
    truck.vehicle_type_id = vehicle_type_id
    # truck.location_id = location_id
    truck.number = number
    truck.engine = engine
    truck.vehicle_model = vehicle_model
    truck.register_date = register_date
    truck.route = route
    truck.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    # 获取session中的user_id, 根据user_id查询企业
    user_id = int(request.session.get('user_id', ''))

    # 查询该企业的所有车辆数据
    if user_id != '' and user_id != 1:
        truck.enterprise_id = user_id
    else:
        truck.enterprise_id = 1

    # 存入数据库
    try:
        truck.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/vehicle')


# 编辑车辆
def vehicle_modify(request):
    # 获取用户提交的车辆信息
    # location_id = int(request.GET.get('location'))          # 车牌所在地
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
    # truck.location_id = location_id
    truck.number = number
    truck.engine = engine
    truck.vehicle_model = vehicle_model
    truck.register_date = register_date
    truck.route = route
    truck.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    # 审核状态变为未提交
    truck.status_id = 1
    # 删除未通过原因
    truck.reason = ''

    # 删除原有的通行证图片文件
    file_name = truck.file_name

    if file_name is not None and file_name != '':
        file_name = r'%s/certification/%s' % (settings.FILE_DIR, file_name)
        truck.file_name = None
        truck.cert_id = None
        if os.path.exists(file_name):
            os.remove(file_name)

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

    # 审核状态根据车辆类型变化, 大型货车需要环保局审核, 其它直接到交管局审核
    if truck.vehicle_type_id == 1:
        truck.status_id = 2
    else:
        truck.status_id = 3

    # 存入数据库
    try:
        truck.save()

        # 该用户已提交车辆计数加1
        user_id = int(request.session.get('user_id', ''))

        # 查询已提交申请车辆数, 限制提交车辆数
        user = User.objects.get(id=user_id)
        user.applied_number += 1

        user.save()

    except Exception as e:
        print(e)

    # # 生成通行证图片
    # # 生成通行证id, 201805+车牌号+三位随机数
    # # certification_id = '%s%s%d%d%d' % (time.strftime('%Y%m', time.localtime()), truck.number[1:], random.randint(0, 9),
    # #                                    random.randint(0, 9), random.randint(0, 9))
    # # 临时设定, 记得改掉
    # certification_id = '%s%s%d%d%d' % ('201805', truck.number[1:], random.randint(0, 9), random.randint(0, 9),
    #                                    random.randint(0, 9))
    #
    # truck.cert_id = certification_id
    # limit_data = '2018年5月31日'  # 暂时写为5月底
    # number = '%s' % truck.number
    # enterprise_name = truck.enterprise.enterprise_name
    # route = truck.route
    # # 图片文件名
    # file_name = r'%s/certification/%s.jpg' % (settings.FILE_DIR, certification_id)
    # truck.file_name = '%s.jpg' % certification_id
    #
    # generate_certification(certification_id, limit_data, number, enterprise_name, route, file_name)
    #

    return HttpResponseRedirect('/vehicle')


# 是否到达车辆提交上限
def is_reach_limit(request):
    allow_submit = SysStatus.objects.get(id=1).allow_submit

    if allow_submit:
        user_id = request.GET.get('user_id', 0)

        result = False
        if user_id != 0:
            user = User.objects.get(id=user_id)
            if user.applied_number >= user.limit_number:
                result = True
    else:
        result = False

    return JsonResponse({'result': result, 'allow_submit': allow_submit})


# 是否可以提交全部车辆
def can_submit_all(request):
    result = SysStatus.objects.get(id=1).allow_submit

    if result:
        user_id = request.GET.get('user_id', 0)

        if user_id != 0:
            # 查询全已提交车辆和可提交车辆上限
            user = User.objects.get(id=user_id)
            # 计算允许提交的车辆总数
            allow_number = user.limit_number - user.applied_number
            if allow_number < 0:
                allow_number = 0

            # 查询本次提交需要提交的车辆总数
            vehicle_list = Vehicle.objects.filter(enterprise_id=user_id).filter(status_id=1)
            # 可以提交的车辆数量
            vehicle_num = 0
            # 信息不全的车辆数量
            error_num = 0
            for truck in vehicle_list:
                vehicle_type = str(truck.vehicle_type_id).strip()
                number = str(truck.number).strip()
                engine = str(truck.engine).strip()
                vehicle_model = str(truck.vehicle_model).strip()
                register_date = str(truck.register_date).strip()
                route = str(truck.route).strip()

                could_submit = True
                if len(number) == 0 or number == 'None':
                    could_submit = False
                elif len(vehicle_model) == 0 or vehicle_model == 'None':
                    could_submit = False
                elif len(register_date) == 0 or register_date == 'None':
                    could_submit = False
                elif len(route) == 0 or route == 'None':
                    could_submit = False
                elif vehicle_type != 15 and (len(engine) == 0 or engine == 'None'):
                    could_submit = False

                if could_submit:
                    vehicle_num += 1
                else:
                    error_num += 1

            # 如果提交车辆的总数大于允许提交总数, 返回本次提交的数量和未提交的数量
            ignore_num = 0
            if vehicle_num > allow_number:
                result = False
                ignore_num = vehicle_num - allow_number
                vehicle_num = allow_number
    else:
        vehicle_num = 0
        ignore_num = 0
        error_num = 0

    return JsonResponse({'result': result, 'vehicle_num': vehicle_num, 'ignore_num': ignore_num,
                         'error_num': error_num})


# 批量导入车辆信息
def excel_import(request):
    # 获取用户上传的excel文件, 文件不存储, 在内存中对文件进行操作
    excel_file = request.FILES.get('excel_file')

    # 打开excel文件, 直接从内存读取文件内容
    workbook = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
    # 获得sheets列表
    sheets = workbook.sheet_names()
    # 获得第一个sheet对象
    worksheet = workbook.sheet_by_name(sheets[0])
    # 遍历
    new_truck_list = []
    for i in range(1, worksheet.nrows):
        # row = worksheet.row(i)
        # 读取一条车辆信息
        # ctype： 0-empty, 1-string, 2-number, 3-date, 4-boolean, 5-error
        vehicle_type = worksheet.cell_value(i, 1)           # 车辆类型

        if worksheet.cell(i, 2).ctype == 2:
            number = str(int(worksheet.cell_value(i, 2))).strip()       # 车牌号
        else:
            number = str(worksheet.cell_value(i, 2)).strip()

        if worksheet.cell(i, 3).ctype == 2:
            engine = str(int(worksheet.cell_value(i, 3))).strip()       # 发动机型号
        else:
            engine = str(worksheet.cell_value(i, 3)).strip()

        vehicle_model = str(worksheet.cell_value(i, 4)).strip()         # 车辆型号

        if worksheet.cell(i, 5).ctype == 3:
            register_date = xlrd.xldate_as_datetime(worksheet.cell_value(i, 5), 0)
            register_date = datetime.datetime.strftime(register_date, r'%Y/%m/%d')
        else:
            register_date = str(worksheet.cell_value(i, 5))           # 注册日期

        route = str(worksheet.cell_value(i, 6)).strip()                   # 路线

        # print('%s %s %s %s %s %s' % (vehicle_type, number, engine, vehicle_model, register_date, route))
        # 如果车牌不为空, 创建车辆对象, 否则略过该条数据
        is_exist = False
        if number == '' or number is None:
            is_exist = True

        if not is_exist:
            # 如果库中该企业已经存在该车牌, 则忽略该车辆, 否者创建新的车辆对象
            # 获取session中的user_id, 根据user_id查询企业
            user_id = int(request.session.get('user_id', ''))

            # 查询该企业的所有车辆数据
            if user_id == '' or user_id == 1:
                is_exist = True
            else:
                is_exist = Vehicle.objects.filter(enterprise_id=user_id).filter(number=number).exists()

        if not is_exist:
            truck = Vehicle()
            truck.number = number

            # 添加车辆属性
            if vehicle_type != '' and vehicle_type is not None:
                if '大' in vehicle_type:
                    truck.vehicle_type_id = 1
                elif '小' in vehicle_type:
                    truck.vehicle_type_id = 2
                elif '挂' in vehicle_type:
                    truck.vehicle_type_id = 15

            if engine != '' and engine is not None:
                truck.engine = engine

            if vehicle_model != '' and vehicle_model is not None:
                truck.vehicle_model = vehicle_model

            # 车辆注册日期, 应该判断一下格式是否正确, 不正确添加默认值, 或设置为空, 现在没时间做了
            if register_date != '' and register_date is not None:
                register_date = time.strptime(register_date, r'%Y/%m/%d')
                truck.register_date = time.strftime(r'%Y-%m-%d', register_date)

            if route != '' and route is not None:
                truck.route = route

            truck.modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

            if user_id != '' and user_id != 1:
                truck.enterprise_id = user_id
            else:
                truck.enterprise_id = 1     # 多此一举

            new_truck_list.append(truck)

    Vehicle.objects.bulk_create(new_truck_list)

        # for j in range(1, worksheet.ncols):
            # ctype： 0-empty, 1-string, 2-number, 3-date, 4-boolean, 5-error
            # 判断数据的类型, 如果是数字, 默认显示为浮点数, 这里转成整数
            # if worksheet.cell(i, j).ctype == 2:
            #     print("%s\t" % int(worksheet.cell_value(i, j)), end="")
            # else:
            #     print("%s\t" % worksheet.cell_value(i, j), end="")

    return HttpResponseRedirect('/vehicle')


# 提交全部车辆(request):
def vehicle_submit_all(request):
    # 获取session中的user_id, 根据user_id查询企业
    user_id = int(request.session.get('user_id', ''))

    # 查询该企业的所有车辆数据
    if user_id != '' and user_id != 1:
        # 查询已提交申请车辆数, 限制提交车辆数
        user = User.objects.get(id=user_id)
        limit_number = user.limit_number
        applied_number = user.applied_number

        # 判断是否到达上限, 如果达到退出提交
        if applied_number >= limit_number:
            return HttpResponseRedirect('/vehicle')
        else:
            truck_list = Vehicle.objects.filter(enterprise_id=user_id).filter(status_id=1)
    # 判断查询结果集是否为空
    # [{'id': 9796, 'number': '津AQ5028', 'enterprise': 24, 'route': '津北线，复康路'},]
    if truck_list:
        for truck in truck_list:
            # 判断信息是否填写完整
            vehicle_type = str(truck.vehicle_type_id).strip()
            number = str(truck.number).strip()
            engine = str(truck.engine).strip()
            vehicle_model = str(truck.vehicle_model).strip()
            register_date = str(truck.register_date).strip()
            route = str(truck.route).strip()

            could_submit = True
            if len(number) == 0 or number == 'None':
                could_submit = False
            elif len(vehicle_model) == 0 or vehicle_model == 'None':
                could_submit = False
            elif len(register_date) == 0 or register_date == 'None':
                could_submit = False
            elif len(route) == 0 or route == 'None':
                could_submit = False
            elif vehicle_type != 15 and (len(engine) == 0 or engine == 'None'):
                could_submit = False

            # 提交车辆
            if could_submit:
                try:
                    # 审核状态根据车辆类型变化, 大型货车需要环保局审核, 其它直接到交管局审核
                    if truck.vehicle_type_id == 1:
                        Vehicle.objects.filter(id=truck.id).update(status_id=2)
                    else:
                        Vehicle.objects.filter(id=truck.id).update(status_id=3)

                    # 已提交车辆数+1
                    applied_number += 1

                    # 如果到达提交上限, 退出循环
                    if applied_number >= limit_number:
                        break
                except Exception as e:
                    print(e)

        user.applied_number = applied_number
        user.save()

    # # 查询该企业的所有车辆数据
    # if user_id != '' and user_id != 1:
    #     # 查询已提交申请车辆数, 限制提交车辆数
    #     user = User.objects.get(id=user_id)
    #     limit_number = user.limit_number
    #     applied_number = user.applied_number
    #
    #     # 判断是否到达上限, 如果达到退出循环
    #     if applied_number >= limit_number:
    #         return HttpResponseRedirect('/vehicle')
    #     else:
    #         truck_list = Vehicle.objects.filter(enterprise_id=user_id).filter(status_id=1).values_list('id', flat=True)
    #         print(truck_list)
    # # 判断查询结果集是否为空
    # if len(truck_list) > 0:
    #     for truck in truck_list:
    #         # 审核状态变为通过
    #         truck.status_id = 4
    #
    #         # 生成通行证图片
    #         # 生成通行证id, 201805+车牌号+三位随机数
    #         certification_id = '%s%s%d%d%d' % (time.strftime('%Y%m', time.localtime()), truck.number[1:],
    #                                            random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    #         truck.cert_id = certification_id
    #         limit_data = '2018年5月31日'  # 暂时写为5月底
    #         number = '%s' % truck.number
    #         enterprise_name = truck.enterprise.enterprise_name
    #         route = truck.route
    #         # 图片文件名
    #         file_name = r'%s/certification/%s.jpg' % (settings.FILE_DIR, certification_id)
    #         truck.file_name = '%s.jpg' % certification_id
    #
    #         generate_certification(certification_id, limit_data, number, enterprise_name, route, file_name)
    #
    #         # 存入数据库
    #         try:
    #             truck.save()
    #
    #             # 已提交车辆数+1
    #             applied_number += 1
    #
    #             if applied_number == limit_number:
    #                 break
    #         except Exception as e:
    #             print(e)
    #
    #     user.applied_number = applied_number
    #     user.save()

    # # 查询该企业的所有车辆数据
    # if user_id != '' and user_id != 1:
    #     # 查询已提交申请车辆数, 限制提交车辆数
    #     user = User.objects.get(id=user_id)
    #     limit_number = user.limit_number
    #     applied_number = user.applied_number
    #
    #     # 判断是否到达上限, 如果达到退出循环
    #     if applied_number >= limit_number:
    #         return HttpResponseRedirect('/vehicle')
    #     else:
    #         vehicle_info_list = Vehicle.objects.filter(enterprise_id=user_id).filter(status_id=1).\
    #             values('id', 'number', 'enterprise', 'route')
    # # 判断查询结果集是否为空
    # # [{'id': 9796, 'number': '津AQ5028', 'enterprise': 24, 'route': '津北线，复康路'},]
    # if len(vehicle_info_list) > 0:
    #     for vehicle_info in vehicle_info_list:
    #         # 生成通行证图片
    #         # 生成通行证id, 201805+车牌号+三位随机数
    #         certification_id = '%s%s%d%d%d' % (time.strftime('%Y%m', time.localtime()), vehicle_info['number'][1:],
    #                                            random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
    #         limit_data = '2018年5月31日'  # 暂时写为5月底
    #         number = '%s' % vehicle_info['number']
    #         enterprise_name = User.objects.get(id=vehicle_info['enterprise']).enterprise_name
    #         route = vehicle_info['route']
    #         # 图片文件名
    #         file_name = r'%s/certification/%s.jpg' % (settings.FILE_DIR, certification_id)
    #
    #         generate_certification(certification_id, limit_data, number, enterprise_name, route, file_name)
    #
    #         # 存入数据库
    #         try:
    #             # 审核状态变为通过
    #             # truck.status_id = 4
    #             # truck.cert_id = certification_id
    #             Vehicle.objects.filter(id=vehicle_info['id']).update(status_id=4, cert_id=certification_id,
    #                                                                  file_name=os.path.basename(file_name))
    #             # 已提交车辆数+1
    #             applied_number += 1
    #
    #             if applied_number == limit_number:
    #                 break
    #         except Exception as e:
    #             print(e)
    #
    #     user.applied_number = applied_number
    #     user.save()

    return HttpResponseRedirect('/vehicle')


# 显示通行证查询下载页面
def download(request):
    # 获取车牌号
    number = request.GET.get('number', '')

    status = 99
    truck = None
    # 如果number为空, 当前是未查询状态
    if number != '':
        # 通过车牌查询车辆
        truck_list = Vehicle.objects.filter(number=number)

        if len(truck_list) > 0:
            truck = truck_list[0]
            status = truck.status_id
        else:
            status = 0   # 车辆不存在

    context = {'status': status, 'truck': truck, 'number': number}

    return render(request, 'download.html', context)


# 通行证查询
def download_search(request):
    # 获取车牌号
    number = request.GET.get('number', '')

    return HttpResponseRedirect('/download?number=%s' % number)


# 生成密码
# def generate_pwd(reqeust):
#     user_list = User.objects.all()
#
#     for user in user_list:
#         password = hashlib.sha1(user.password.encode('utf8')).hexdigest()
#         user.password = password
#
#         user.save()
#
#     return HttpResponse('创建成功')


# 显示审核页面
@login_check
def verify(request):

    # 获取查询信息
    number = request.GET.get('number', '')

    # 根据用户提交的查询信息, 查询车辆数据
    if number == '':
        # 如果未输入车牌号, 默认查询全部车辆, 未提交申请车辆除外
        vehicle_list = Vehicle.objects.all().exclude(status_id=1)
    else:
        vehicle_list = Vehicle.objects.filter(number__contains=number).exclude(status_id=1)

    # 从session中获取authority_id
    # user_id = int(request.session.get('user_id', 0))
    authority = int(request.session.get('authority_id', 0))

    # 根据用户权限查询需要该用户审核的车辆
    if authority == 2:
        # 环保局
        # 获取查询车辆的审核状态
        status = int(request.GET.get('status', 2))
        vehicle_list = vehicle_list.filter(vehicle_type_id=1)
    else:
        # 交管局
        status = int(request.GET.get('status', 3))

    if status != 0:
        vehicle_list = vehicle_list.filter(status_id=status)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 创建分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, page_num)

    context = {'mp': mp, 'number': number, 'status': status, 'authority': authority}

    return render(request, 'verify.html', context)


# 车辆审核通过
def verify_pass(request):
    vehicle_id = int(request.GET.get('vehicle_id', 0))

    number = request.GET.get('number', 0)
    page_num = request.GET.get('page_num', 0)
    status = request.GET.get('status', 0)

    url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    if vehicle_id != 0:
        truck = Vehicle.objects.get(id=vehicle_id)
        truck.status_id += 1

        if truck.status_id == 4:
            # 生成通行证图片
            # 生成通行证id, 201805+车牌号+三位随机数
            # 获取当前年, 月
            year = time.localtime().tm_year
            month = time.localtime().tm_mon
            # 如果是12月, 则年+1, 月变为1; 否则, 月+1
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1

            if month < 10:
                id_start = '%d0%d' % (year, month)
            else:
                id_start = '%d%d' % (year, month)

            certification_id = '%s%s%d%d%d' % (id_start, truck.number[1:], random.randint(0, 9), random.randint(0, 9),
                                               random.randint(0, 9))
            truck.cert_id = certification_id
            # 计算通行证截至日期
            end_day = calendar.monthrange(year, month)[1]
            limit_data = '%d年%d月%d日' % (year, month, end_day)
            number = '%s' % truck.number
            enterprise_name = truck.enterprise.enterprise_name
            route = truck.route
            # 图片文件名
            file_name = r'%s/certification/%s.jpg' % (settings.FILE_DIR, certification_id)
            truck.file_name = '%s.jpg' % certification_id

            generate_certification(certification_id, limit_data, number, enterprise_name, route, file_name)

        # 存入数据库
        try:
            truck.save()
        except Exception as e:
            print(e)

    return HttpResponseRedirect(url)


# 车辆审核不通过
def verify_refuse(request):
    vehicle_id = int(request.GET.get('vehicle_id', 0))

    number = request.GET.get('number', 0)
    page_num = request.GET.get('page_num', 0)
    status = request.GET.get('status', 0)

    url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    if vehicle_id != 0:
        truck = Vehicle.objects.get(id=vehicle_id)
        truck.status_id = 5
        refuse_reason = request.GET.get('refuse_reason', '')
        truck.reason = refuse_reason

        truck.save()

    return HttpResponseRedirect(url)


# 定时任务, 每月26日0点, 修改系统状态为不能提交车辆审核
def forbid_submit():
    sys_status = SysStatus.objects.get(id=1)
    sys_status.allow_submit = False
    sys_status.save()
    print('submit forbidden!')


# 定时任务, 每月1日0点, 初始化系统:
# 保存上月车辆申请状态(id, 号牌, 审核状态, 未通过原因, 通行证id, 车辆提交审核时间, 环保局审核时间, 交管局审核时间)
# 修改系统状态为可以提交车辆审核
# 删除通行证图片文件
# 全部车辆状态修改为1-未提交, 清空数据库中如下列的内容: 未通过原因(reason), 通行证保存路径(file_name), 通行证id(cert_id)
# 所有用户的已提交车辆数量归零
def init_sys():
    # 清空备份数据库
    Backup1.objects.all().delete()

    # 备份上月车辆审核状态
    truck_list = Vehicle.objects.all()
    backup_list = []
    for truck in truck_list:
        backup = Backup1()
        backup.number = truck.number
        backup.status_id = truck.status_id
        backup.reason = truck.reason
        backup.cert_id = truck.cert_id
        backup.submit_time = truck.submit_time
        backup.hbj_time = truck.hbj_time
        backup.jgj_time = truck.jgj_time

        backup_list.append(backup)
        # 删除通行证图片文件
        file_name = truck.file_name

        if file_name is not None and file_name != '':
            file_name = r'%s/certification/%s' % (settings.FILE_DIR, file_name)
            if os.path.exists(file_name):
                os.remove(file_name)

    Backup1.objects.bulk_create(backup_list)

    # 修改系统状态为可以提交车辆审核
    sys_status = SysStatus.objects.get(id=1)
    sys_status.allow_submit = True
    sys_status.save()

    # 初始化全部车辆状态为未提交
    Vehicle.objects.all().update(status_id=1)

    # 清除数据库中如下列的内容: 未通过原因(reason), 通行证保存路径(file_name), 通行证id(cert_id)
    Vehicle.objects.all().update(reason=None)
    Vehicle.objects.all().update(file_name=None)
    Vehicle.objects.all().update(cert_id=None)

    # 所有用户的已提交车辆数量归零
    User.objects.all().update(applied_number=0)

    print('System initial complete.')


# 导出全部待审核车辆
def export_xls(request):
    authority_id = request.session.get('authority_id', 0)
    if authority_id == 2:
        truck_list = Vehicle.objects.filter(status_id=2)
    elif authority_id == 3:
        truck_list = Vehicle.objects.filter(status_id=3)
    elif authority_id == 99:
        truck_list = Vehicle.objects.filter(status_id__in=[2, 3])
    else:
        truck_list = None

    if truck_list:
        # 创建工作簿
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('sheet1', cell_overwrite_ok=True)
        # 设置表头
        title = ['id', '企业名称', '车牌号', '车辆类型', '发动机号', '车辆型号', '注册日期', '运输路线', '审核结果(p-通过, f-不通过)',
                 '未通过原因']
        # 生成表头
        len_title = len(title)
        for i in range(0, len_title):
            if i == 7:
                ws.col(i).width = 256 * 50
            elif i == 8:
                ws.col(i).width = 256 * 30
            else:
                ws.col(i).width = 256 * 20
            ws.write(0, i, title[i])
        # 写入车辆数据
        i = 1
        len_content = len_title - 2
        for truck in truck_list:
            content = [truck.id, truck.enterprise.enterprise_name, truck.number, truck.vehicle_type.name, truck.engine,
                       truck.vehicle_model, str(truck.register_date), truck.route]

            for j in range(0, len_content):
                ws.write(i, j, content[j])
            i += 1

        # 内存文件操作
        buf = io.BytesIO()
        # 将文件保存在内存中
        wb.save(buf)
        response = HttpResponse(buf.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=vehicle_check.xls'
        response.write(buf.getvalue())
        return response
    else:
        number = request.GET.get('number', 0)
        page_num = request.GET.get('page_num', 0)
        status = request.GET.get('status', 0)
        url = '/verify?number=%s&page_num=%s&status=%s' % (number, page_num, status)
        return HttpResponseRedirect(url)


# 导入审核后的车辆数据
def import_xls(request):
    # 获取用户的权限等级
    authority_id = request.session.get('authority_id', 0)
    # 获取用户上传的excel文件, 文件不存储, 在内存中对文件进行操作
    excel_file = request.FILES.get('excel_file')

    # 打开excel文件, 直接从内存读取文件内容
    workbook = xlrd.open_workbook(filename=None, file_contents=excel_file.read())
    # 获得sheets列表
    sheets = workbook.sheet_names()
    # 获得第一个sheet对象
    worksheet = workbook.sheet_by_name(sheets[0])
    # 遍历
    for i in range(1, worksheet.nrows):
        # 读取一条车辆信息
        # ctype： 0-empty, 1-string, 2-number, 3-date, 4-boolean, 5-error

        # 读取车辆id
        if worksheet.cell(i, 0).ctype != 5 and worksheet.cell_value(i, 0) != '':
            vehicle_id = int(worksheet.cell_value(i, 0))  # 车辆id
        else:
            continue

        # 根据车辆id从数据库查询该车辆
        try:
            truck = Vehicle.objects.get(id=vehicle_id)
        except Exception as e:
            print(e)
            continue

        if truck.status_id != 2 and truck.status_id != 3:
            continue
        elif authority_id == 2 and truck.status_id != 2:
            continue
        elif authority_id == 3 and truck.status_id != 3:
            continue

        # 读取审核状态
        if worksheet.cell(i, 8).ctype != 5 and worksheet.cell_value(i, 8) != '':
            vehicle_status = str(worksheet.cell_value(i, 8))  # 审核状态
        else:
            continue

        # 审核通过
        if 'p' in vehicle_status.lower():
            truck.status_id += 1
        # 审核不通过
        elif 'f' in vehicle_status.lower():
            truck.status_id = 5
            # 读取未通过原因
            if worksheet.cell(i, 9).ctype != 5 and worksheet.cell_value(i, 9) != '':
                truck.reason = worksheet.cell_value(i, 9)  # 未通过原因
        else:
            continue

        # 完全通过审核, 生成通行证图片
        if truck.status_id == 4:
            # 生成通行证图片
            # 生成通行证id, 201805+车牌号+三位随机数
            # 获取当前年, 月
            year = time.localtime().tm_year
            month = time.localtime().tm_mon
            # 如果是12月, 则年+1, 月变为1; 否则, 月+1
            if month == 12:
                year += 1
                month = 1
            else:
                month += 1

            if month < 10:
                id_start = '%d0%d' % (year, month)
            else:
                id_start = '%d%d' % (year, month)

            certification_id = '%s%s%d%d%d' % (id_start, truck.number[1:], random.randint(0, 9), random.randint(0, 9),
                                               random.randint(0, 9))
            truck.cert_id = certification_id
            # 计算通行证截至日期
            end_day = calendar.monthrange(year, month)[1]
            limit_data = '%d年%d月%d日' % (year, month, end_day)
            number = '%s' % truck.number
            enterprise_name = truck.enterprise.enterprise_name
            route = truck.route
            # 图片文件名
            file_name = r'%s/certification/%s.jpg' % (settings.FILE_DIR, certification_id)
            truck.file_name = '%s.jpg' % certification_id

            generate_certification(certification_id, limit_data, number, enterprise_name, route, file_name)

        truck.save()

    return HttpResponseRedirect('/verify')


# 测试
def my_test(request):
    if 'post' in request.method.lower():
        content = request.POST.get('param')
    else:
        content = request.GET.get('param')
    print(content)

    return HttpResponse('ok')
