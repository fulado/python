import random
import hashlib
import io
import time
import calendar

from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.db.models import Count
from PIL import Image, ImageDraw, ImageFont

from .models import User, Enterprise, Station, Department, Route, Vehicle, Permission, Mark
from .decorator import login_check
from tj_scheduled_bus import settings
from .utils import save_file, MyPaginator, statistic_update, send_sms, check_vehicle


# Create your views here.


# 验证码
def check_code(request):
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (255, 255, 255)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 0, random.randrange(0, 255))
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
    fontcolor = (0, 0, 0)
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


# 短信验证码
def sms_check_code(request):
    phone_number = request.POST.get('phone', '')

    if not phone_number:
        data = {'result': False}
    else:
        sms_code = '%d%d%d%d' % (random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), random.randint(0, 9))
        if send_sms(sms_code):
        # if True:
            print(sms_code)
            request.session['sms_code'] = sms_code
            data = {'result': True}
        else:
            data = {'result': False}

    return JsonResponse(data)


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

    # 把user.id保存到session中
    request.session.set_expiry(0)  # 浏览器关闭后清除session
    request.session['user_id'] = user.id
    request.session['authority'] = user.authority

    return HttpResponseRedirect('/main')


# 退出登录
def logout(request):
    request.session.clear()
    request.session.flush()

    return HttpResponseRedirect('/')


# 显示注册页面
def register(request):
    # user_id = request.session.get('user_id', '')
    # if user_id != '':
    #     return HttpResponseRedirect('/login')

    msg = request.GET.get('msg', '')
    cp = request.GET.get('cp', '')

    context = {'msg': msg,
               'cp': cp,
               }

    return render(request, 'register.html', context)


# 注册
def register_handle(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    re_password = request.POST.get('re_password')
    phone_number = request.POST.get('phone')

    if User.objects.filter(phone=phone_number).exists():
        msg = '手机号已经被注册'
        return HttpResponseRedirect('/register?msg=%s' % msg)

    sms_code = request.POST.get('sms_code')
    session_code = request.session.get('sms_code')

    if sms_code != session_code:
        msg = '验证码错误'
        return HttpResponseRedirect('/register?msg=%s' % msg)

    if password != re_password:
        msg = '两次输入密码不一致'
        return HttpResponseRedirect('/register?msg=%s' % msg)

    is_user_exist = User.objects.filter(username=username).exists()
    if is_user_exist:
        msg = '账号已存在'
        return HttpResponseRedirect('/register?msg=%s' % msg)

    user_info = User()
    user_info.username = username
    user_info.password = hashlib.sha1(password.encode('utf8')).hexdigest()
    user_info.authority = 1
    user_info.phone = phone_number

    user_info.save()

    msg = '注册成功，请登录'
    return HttpResponseRedirect('/login?msg=%s' % msg)


def change_password(request):
    username = request.POST.get('username')
    password = request.POST.get('password')
    re_password = request.POST.get('re_password')
    phone_number = request.POST.get('phone')

    if not User.objects.filter(phone=phone_number).exists():
        msg = '手机号不存在'
        return HttpResponseRedirect('/register?msg=%s' % msg)

    sms_code = request.POST.get('sms_code')
    session_code = request.session.get('sms_code')

    if sms_code != session_code:
        msg = '验证码错误'
        return HttpResponseRedirect('/register?msg=%s' % msg)

    if password != re_password:
        msg = '两次输入密码不一致'
        return HttpResponseRedirect('/register?msg=%s' % msg)

    user_list = User.objects.filter(username=username)

    if not user_list:
        msg = '账号不存在'
        return HttpResponseRedirect('/register?msg=%s' % msg)

    user_info = user_list[0]
    user_info.password = hashlib.sha1(password.encode('utf8')).hexdigest()

    user_info.save()

    msg = '密码修改成功，请登录'
    return HttpResponseRedirect('/login?msg=%s' % msg)


# 显示主页面
@login_check
def main(request):
    user_id = request.session.get('user_id', '')
    authority = int(request.session.get('authority', 1))

    user = User.objects.filter(id=user_id)[0] if user_id else None

    context = {'user': user}

    if authority == 2:
        return render(request, 'zhidui/main.html', context)
    elif authority == 3:
        return render(request, 'zongdui/main.html', context)
    else:
        return render(request, 'main.html', context)


# 显示企业管理页面
@login_check
def enterprise(request):
    user_id = request.session.get('user_id', '')
    search_name = request.POST.get('search_name', '')
    page_num = request.GET.get('page_num', 1)

    enterprise_list = Enterprise.objects.filter(user_id=user_id).filter(enterprise_name__contains=search_name)
    dept_list = Department.objects.all()

    # 分页
    mp = MyPaginator()
    mp.paginate(enterprise_list, 10, page_num)

    context = {'mp': mp,
               'search_name': search_name,
               'dept_list': dept_list
               }

    return render(request, 'enterprise.html', context)


# 新增企业
def enterprise_add(request):
    user_id = request.session.get('user_id', '')

    enterprise_type = request.POST.get('enterprise_type', 0)
    enterprise_name = request.POST.get('enterprise_name', '')
    enterprise_owner = request.POST.get('enterprise_owner', '')
    enterprise_code = request.POST.get('enterprise_code', '')
    contact_person = request.POST.get('contact_person', '')
    phone = request.POST.get('phone', '')
    dept_id = request.POST.get('dept_id', 0)

    enterprise_info = Enterprise()
    enterprise_info.enterprise_type_id = enterprise_type
    enterprise_info.enterprise_name = enterprise_name
    enterprise_info.enterprise_owner = enterprise_owner
    enterprise_info.enterprise_code = enterprise_code
    enterprise_info.contact_person = contact_person
    enterprise_info.phone = phone
    enterprise_info.user_id = user_id
    enterprise_info.enterprise_status_id = 1
    enterprise_info.dept_id = dept_id

    # 营业执照照片
    business_license = request.FILES.get('business_license', '')
    if business_license:
        file_name = '营业执照_' + enterprise_name
        save_file(business_license, file_name)
        enterprise_info.business_license = file_name

    # 法人身份证正面
    id_card_front = request.FILES.get('id_card_front', '')
    if id_card_front:
        file_name = '身份证正面_' + enterprise_name
        save_file(id_card_front, file_name)
        enterprise_info.id_card_front = file_name

    # 法人身份证反面
    id_card_back = request.FILES.get('id_card_back', '')
    if id_card_back:
        file_name = '身份证反面_' + enterprise_name
        save_file(id_card_back, file_name)
        enterprise_info.id_card_back = file_name

    # 法人身份证反面
    rent_contract = request.FILES.get('rent_contract', '')
    if rent_contract:
        file_name = '租赁合同_' + enterprise_name
        save_file(rent_contract, file_name)
        enterprise_info.rent_contract = file_name

    try:
        enterprise_info.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/enterprise')


# 编辑企业
def enterprise_modify(request):
    enterprise_id = request.POST.get('enterprise_id', '')

    enterprise_type = request.POST.get('enterprise_type', 0)
    enterprise_name = request.POST.get('enterprise_name', '')
    enterprise_owner = request.POST.get('enterprise_owner', '')
    enterprise_code = request.POST.get('enterprise_code', '')
    contact_person = request.POST.get('contact_person', '')
    phone = request.POST.get('phone', '')

    enterprise_info = Enterprise.objects.get(id=enterprise_id)
    enterprise_info.enterprise_type_id = enterprise_type
    enterprise_info.enterprise_name = enterprise_name
    enterprise_info.enterprise_owner = enterprise_owner
    enterprise_info.enterprise_code = enterprise_code
    enterprise_info.contact_person = contact_person
    enterprise_info.phone = phone

    # 营业执照照片
    business_license = request.FILES.get('business_license', '')
    if business_license:
        file_name = '营业执照_' + enterprise_name
        save_file(business_license, file_name)
        enterprise_info.business_license = file_name

    # 法人身份证正面
    id_card_front = request.FILES.get('id_card_front', '')
    if id_card_front:
        file_name = '身份证正面_' + enterprise_name
        save_file(id_card_front, file_name)
        enterprise_info.id_card_front = file_name

    # 法人身份证反面
    id_card_back = request.FILES.get('id_card_back', '')
    if id_card_back:
        file_name = '身份证反面_' + enterprise_name
        save_file(id_card_back, file_name)
        enterprise_info.id_card_back = file_name

    # 法人身份证反面
    rent_contract = request.FILES.get('rent_contract', '')
    if rent_contract:
        file_name = '租赁合同_' + enterprise_name
        save_file(rent_contract, file_name)
        enterprise_info.rent_contract = file_name

    try:
        enterprise_info.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/enterprise')


# 删除企业
def enterprise_delete(request):
    enterprise_id = request.POST.get('enterprise_id', '')

    enterprise_info = Enterprise.objects.get(id=enterprise_id)

    enterprise_info.delete()

    return HttpResponseRedirect('/enterprise')


# 提交企业
def enterprise_submit(request):
    enterprise_id = request.GET.get('enterprise_id', '')

    Enterprise.objects.filter(id=enterprise_id).update(enterprise_status_id=2)

    return HttpResponseRedirect('/enterprise')


# 判断企业是否存在
def is_enterprise_exist(request):
    user_id = request.session.get('user_id', '')
    enterprise_name = request.GET.get('enterprise_name')
    enterprise_code = request.GET.get('enterprise_code')

    is_exist = Enterprise.objects.filter(enterprise_name=enterprise_name, user_id=user_id).exists() or \
               Enterprise.objects.filter(enterprise_code=enterprise_code, user_id=user_id).exists()

    return JsonResponse({'is_exist': is_exist})


# 显示车辆信息
@login_check
def vehicle(request):
    user_id = request.session.get('user_id', '')
    number = request.POST.get('vehicle_number', '')
    vehicle_status = int(request.POST.get('vehicle_status', 0))
    page_num = request.GET.get('page_num', 1)

    vehicle_list = Vehicle.objects.filter(vehicle_user_id=user_id).filter(vehicle_number__contains=number)
    if vehicle_status != 0:
        vehicle_list = vehicle_list.filter(vehicle_status_id=vehicle_status)
    else:
        pass

    # 分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, page_num)

    context = {'mp': mp,
               'number': number,
               'vehicle_status': vehicle_status,
               }

    return render(request, 'vehicle.html', context)


# 添加车辆
def vehicle_add(request):
    user_id = request.session.get('user_id', '')

    vehicle_number = request.POST.get('vehicle_number', '')
    vehicle_type = request.POST.get('vehicle_type', '1')
    engine_code = request.POST.get('engine_code', '')
    vehicle_owner = request.POST.get('vehicle_owner', '')
    register_date = request.POST.get('register_date', '')
    vehicle_belong = request.POST.get('vehicle_belong', '1')

    vehicle_info = Vehicle()
    vehicle_info.vehicle_number = vehicle_number
    vehicle_info.vehicle_type_id = int(vehicle_type)
    vehicle_info.engine_code = engine_code
    vehicle_info.vehicle_owner = vehicle_owner
    vehicle_info.register_date = register_date
    vehicle_info.vehicle_belong_id = int(vehicle_belong)
    vehicle_info.vehicle_user_id = user_id
    vehicle_info.vehicle_status_id = 1

    vehicle_info.save()

    return HttpResponseRedirect('/vehicle')


# 编辑车辆
def vehicle_modify(request):
    vehicle_id = request.POST.get('vehicle_id', '')
    vehicle_type = request.POST.get('vehicle_type', '1')
    engine_code = request.POST.get('engine_code', '')
    vehicle_owner = request.POST.get('vehicle_owner', '')
    register_date = request.POST.get('register_date', '')
    vehicle_belong = request.POST.get('vehicle_belong', '1')

    vehicle_info = Vehicle.objects.get(id=vehicle_id)

    vehicle_info.vehicle_type_id = int(vehicle_type)
    vehicle_info.engine_code = engine_code
    vehicle_info.vehicle_owner = vehicle_owner
    vehicle_info.register_date = register_date
    vehicle_info.vehicle_belong_id = int(vehicle_belong)

    vehicle_info.save()

    return HttpResponseRedirect('/vehicle')


# 提交车辆审核
def vehicle_submit(request):
    vehicle_id = request.GET.get('vehicle_id', '')

    Vehicle.objects.filter(id=vehicle_id).update(vehicle_status_id=2)

    return HttpResponseRedirect('/vehicle_id')


# 删除车辆
def vehicle_delete(request):
    vehicle_id = request.POST.get('vehicle_id', '')

    vehicle_info = Vehicle.objects.get(id=vehicle_id)
    vehicle_info.delete()

    return HttpResponseRedirect('/vehicle')


# 车辆是否可以添加
def can_add_vehicle(request):
    vehicle_number = request.GET.get('number', '')
    engine_code = request.GET.get('engine', '')
    vehicle_owner = request.GET.get('owner', '')
    user_id = request.session.get('user_id', '')

    if Vehicle.objects.filter(vehicle_number=vehicle_number,vehicle_user_id=user_id).exists():
        result = '1'    # 车辆已经存在
    elif not check_vehicle(vehicle_number, engine_code, vehicle_owner):
        result = '2'
    else:
        result = '0'

    return JsonResponse({'result': result})


# 显示站点信息
@login_check
def station(request):
    user_id = request.session.get('user_id', '')
    search_name = request.POST.get('search_name', '')
    page_num = request.GET.get('page_num', 1)

    route_list = Route.objects.filter(route_user_id=user_id).filter(route_status=3).\
        filter(route_name__contains=search_name).values('route_name').annotate(num_station=Count('route_station'))

    area_list = Station.objects.filter(station_status=31).values('station_area').distinct()

    # 模态框显示控制
    display_add_route = request.GET.get('display_add_route', 'none')
    display_mask = request.GET.get('display_mask', 'none')
    route_name = request.GET.get('route_name', '')

    station_list = Route.objects.filter(route_name=route_name).filter(route_status=3).filter(route_user_id=user_id)

    # 分页
    mp = MyPaginator()
    mp.paginate(route_list, 10, page_num)

    context = {'area_list': area_list,
               'display_add_route': display_add_route,
               'display_mask': display_mask,
               'route_name': route_name,
               'station_list': station_list,
               'mp': mp,
               'search_name': search_name
               }

    # for station in station_list:
    #     print(station.route_station.station_name)
    return render(request, 'station.html', context)


# 查询站点信息
def station_search(request):
    obj_1_val = request.GET.get('obj_1_val', '')
    obj_2_val = request.GET.get('obj_2_val', '')
    parent_id = request.GET.get('parent_id', '')
    item = request.GET.get('item')

    # 查询数据
    if item == 'road' and parent_id != '':
        # cate_list = Road.objects.filter(road_area_id=parent_id)
        cate_list = Station.objects.filter(station_status=31).filter(station_area=parent_id).\
            values('station_road').distinct()
    elif item == 'direction' and parent_id != '':
        # cate_list = Direction.objects.filter(direction_road_id=parent_id)
        cate_list = Station.objects.filter(station_status=31).filter(station_area=obj_1_val).\
            filter(station_road=parent_id).values('station_direction').distinct()
    elif item == 'station' and parent_id != '':
        # cate_list = Station.objects.filter(station_direction_id=parent_id)
        cate_list = Station.objects.filter(station_status=31).filter(station_area=obj_1_val).\
            filter(station_road=obj_2_val).filter(station_direction=parent_id)
    else:
        cate_list = []

    # 构建返回的Json数组格式数据
    data = []
    for cate in cate_list:

        if item == 'road':
            cate_info = {'id': cate.get('station_road', ''), 'name': cate.get('station_road', '')}
        elif item == 'direction':
            cate_info = {'id': cate.get('station_direction', ''), 'name': cate.get('station_direction', '')}
        elif item == 'station':
            cate_info = {'id': cate.id, 'name': cate.station_name}
        else:
            cate_info = {}
        data.append(cate_info)
    # print(data)
    return JsonResponse({'cate_list': data})


# 是否可以添加站点
def can_add_station(request):
    user_id = request.session.get('user_id', '')
    route_name = request.GET.get('route_name', '')

    station_count = Route.objects.filter(route_user_id=user_id).filter(route_name=route_name).\
        filter(route_status__in=(1, 3)).count()

    if station_count >= 5:
        result = False
    else:
        result = True

    return JsonResponse({'result': result})


# 添加站点
# def station_add(request):
#     user_id = request.session.get('user_id', '')
#     route_name = request.POST.get('route_name', '')
#     station_id = request.POST.get('station', '')
#
#     route_info = Route()
#     route_info.route_name = route_name
#     route_info.route_station_id = station_id
#     route_info.route_user_id = user_id
#
#     route_info.save()
#
#     display_add_route = 'block'
#     display_mask = 'block'
#
#     url = '/station?display_add_route=%s&display_mask=%s&route_name=%s' % (display_add_route, display_mask, route_name)
#
#     return HttpResponseRedirect(url)


# 添加站点
def station_add(request):
    user_id = request.session.get('user_id', '')
    route_name = request.GET.get('route_name', '')
    station_id = int(request.GET.get('station_id', ''))

    is_station_exists = Route.objects.filter(route_name=route_name, route_user_id=user_id, route_station_id=station_id)\
        .filter(route_status__in=(1, 3)).exists()

    station_count = Route.objects.filter(route_name=route_name, route_user_id=user_id).count()

    if not is_station_exists:
        route_info = Route()
        route_info.route_name = route_name
        route_info.route_station_id = station_id
        route_info.route_user_id = user_id

        route_info.save()

        station_info = Station.objects.get(id=station_id)

        result = {'result': True,
                  'station_area': station_info.station_area,
                  'station_road': station_info.station_road,
                  'station_direction': station_info.station_direction,
                  'station_name': station_info.station_name,
                  'route_id': route_info.id,
                  }
    else:
        result = {'result': False}

    return JsonResponse(result)


# 删除站点
def station_delete(request):
    route_id = request.GET.get('route_id', '')

    try:
        route_info = Route.objects.get(id=route_id)

        if route_info.route_status == 1:
            route_info.delete()
        elif route_info.route_status == 3:
            route_info.route_status = 2
            route_info.save()
        else:
            pass

        result = True
    except Exception as e:
        print(e)
        result = False
    finally:
        return JsonResponse({'result': result})


# 取消添加路线
def station_cancel(request):
    user_id = request.session.get('user_id', '')

    try:
        # status是2的更新为3
        Route.objects.filter(route_status=2).filter(route_user_id=user_id).update(route_status=3)

        # 删除status是1的
        Route.objects.filter(route_status=1).filter(route_user_id=user_id).delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect('/station')


# 保存添加路线
def station_save(request):
    Route.objects.filter(route_status=1).update(route_status=3)
    Route.objects.filter(route_status=2).delete()

    return HttpResponseRedirect('/station')


# 显示通行证信息
@login_check
def permission(request):
    user_id = request.session.get('user_id', '')

    vehicle_list = Vehicle.objects.filter(vehicle_user_id=user_id).filter(vehicle_status_id=3)
    route_list = Route.objects.filter(route_user_id=user_id).values('route_name').distinct()

    permission_list = Permission.objects.filter(permission_user_id=user_id)

    # 分页
    mp = MyPaginator()
    mp.paginate(permission_list, 10, 1)

    context = {'vehicle_list': vehicle_list,
               'route_list': route_list,
               'mp': mp
               }

    return render(request, 'permit.html', context)


# 申请通行证
def permission_add(request):
    user_id = request.session.get('user_id', '')
    vehicle_id = request.POST.get('vehicle_id', '')
    route_name = request.POST.get('route_name', '')

    permission_info = Permission()
    permission_info.permission_vehicle_id = vehicle_id
    permission_info.permission_route = route_name
    permission_info.permission_user_id = user_id
    permission_info.permission_status_id = 51

    # 有效日期
    current_time = time.localtime()
    year = current_time.tm_year
    month = current_time.tm_mon
    start_day = current_time.tm_mday
    end_day = calendar.monthrange(year, month)[1]

    # permission_info.start_date = time.strptime('%s-%s-%s' % (year, month, start_day), '%Y-%m-%d')
    # permission_info.end_date = time.strptime('%s-%s-%s' % (year, month, end_day), '%Y-%m-%d')

    permission_info.start_date = '%s-%s-%s' % (year, month, start_day)
    permission_info.end_date = '%s-%s-%s' % (year, month, end_day)

    permission_info.save()

    # 统计企业通行证数量
    enterprise_list = Enterprise.objects.filter(user_id=user_id).filter(enterprise_type_id=41)
    if enterprise_list:
        enterprise_info = enterprise_list[0]
        statistic_update(enterprise_info.id, '%s-%s-%s' % (year, month, end_day))
    else:
        pass

    return HttpResponseRedirect('/permission')


# 显示车辆标记信息
@login_check
def mark(request):
    user_id = request.session.get('user_id', '')
    vehicle_list = Vehicle.objects.filter(vehicle_user_id=user_id)

    vehicle_id_list = []
    for vehicle_info in vehicle_list:
        vehicle_id_list.append(vehicle_info.id)

    mark_list = Mark.objects.filter(vehicle_id__in=vehicle_id_list)

    # 分页
    mp = MyPaginator()
    mp.paginate(mark_list, 10, 1)

    # 所属支队
    dept_info = Department.objects.get(user_id=user_id)
    # print(dept_info.dept_name)
    context = {'mp': mp,
               'dept_info': dept_info,
               }

    return render(request, 'mark.html', context)





























