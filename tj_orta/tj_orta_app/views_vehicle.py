from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.http import JsonResponse
from .models import User, Vehicle, SysStatus
from tj_orta.utils import MyPaginator
from tj_orta import settings
from .decorator import login_check
import time
import datetime
import os
import xlrd
import re


# 显示车辆管理页面
@login_check
def vehicle(request):
    # 获取session中的user_id, 根据user_id查询企业
    user_id = int(request.session.get('user_id', ''))

    # 查询已提交申请车辆数, 限制提交车辆数
    user = User.objects.get(id=user_id)
    limit_number = user.limit_number
    applied_number = Vehicle.objects.exclude(vehicle_type_id=15).filter(enterprise_id=user_id).\
        filter(status_id__in=[2, 3, 4]).count()

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

    # 保存页面状态到session
    request.session['number'] = number
    request.session['status'] = status
    request.session['page_num'] = page_num

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

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/vehicle?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)


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

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/vehicle?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)


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

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/vehicle?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)


# 提交车辆
def vehicle_submit(request):
    vehicle_id = request.GET.get('vehicle_id')  # id

    # 根据id查询车辆
    truck = Vehicle.objects.filter(id=vehicle_id)[0]

    # 审核状态根据车辆类型变化, 大型货车需要环保局审核, 其它直接到交管局审核
    if truck.vehicle_type_id == 1:
        truck.status_id = 3  # 暂时都提交到交管局,设置为3, 如果需要提交到环保局, 改为2
        truck.submit_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    else:
        truck.status_id = 3

    # 存入数据库
    try:
        truck.save()

        # 如果不是挂车, 该用户已提交车辆计数加1
        if truck.vehicle_type_id != 15:
            user_id = int(request.session.get('user_id', ''))

            # 查询已提交申请车辆数, 限制提交车辆数
            user = User.objects.get(id=user_id)
            user.applied_number += 1

            user.save()

    except Exception as e:
        print(e)

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/vehicle?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)


# 是否允许提交申请, 判断到大型车辆是否达到提交上限
def can_submit_vehicle(request):
    # 系统是否允许提交申请
    allow_submit = SysStatus.objects.get(id=1).allow_submit

    # 如果可以提交, 判断大型车辆是否达到提交上线
    if allow_submit:
        user_id = request.GET.get('user_id', 0)

        result = False
        if user_id != 0:
            try:
                applied_number = Vehicle.objects.exclude(vehicle_type_id=15).filter(enterprise_id=user_id). \
                    filter(status_id__in=[2, 3, 4]).count()
                user = User.objects.get(id=user_id)
                if applied_number < user.limit_number:
                    result = True
            except Exception as e:
                print(e)
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
            applied_number = Vehicle.objects.exclude(vehicle_type_id=15).filter(enterprise_id=user_id). \
                filter(status_id__in=[2, 3, 4]).count()
            # 计算允许提交的车辆总数
            allow_number = user.limit_number - applied_number
            if allow_number < 0:
                allow_number = 0

            # 查询本次需要提交的车辆
            vehicle_list = Vehicle.objects.filter(enterprise_id=user_id).filter(status_id=1)

            # 本次需要提交的非挂车辆总数
            vehicle_1_num = 0
            # 本次需要提交的挂车总数
            vehicle_other_num = 0
            # 信息不正确的车辆数量
            error_num = 0
            for truck in vehicle_list:
                vehicle_type = truck.vehicle_type_id
                number = str(truck.number).strip()
                engine = str(truck.engine).strip()
                vehicle_model = str(truck.vehicle_model).strip()
                register_date = str(truck.register_date).strip()
                route = str(truck.route).strip()

                could_submit = True
                if vehicle_type not in [1, 2, 15]:
                    could_submit = False
                elif len(number) == 0 or number == 'None':
                    could_submit = False
                elif vehicle_type == 15 and (re.match(r'^[\W][A-Z][A-Z0-9]{4}$', number, re.A) is None):
                    could_submit = False
                elif vehicle_type != 15 and (re.match(r'^[\W][A-Z][A-Z0-9]{5}$', number, re.A) is None):
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
                    if vehicle_type == 15:
                        vehicle_other_num += 1
                    else:
                        vehicle_1_num += 1
                else:
                    error_num += 1

            # 如果提交的非挂车辆的总数大于允许提交总数, 返回本次提交的数量和未提交的数量
            ignore_num = 0
            if vehicle_1_num > allow_number:
                result = False
                ignore_num = vehicle_1_num - allow_number
                vehicle_num = allow_number + vehicle_other_num      # 可以提交的车辆数量
            else:
                vehicle_num = vehicle_1_num + vehicle_other_num     # 可以提交的车辆数量
    else:
        vehicle_num = -1
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

        if number == '' or number is None:
            continue
        else:
            # 如果库中该企业已经存在该车牌, 则忽略该车辆, 否者创建新的车辆对象
            # 获取session中的user_id, 根据user_id查询企业
            user_id = int(request.session.get('user_id', ''))

        # 查询该企业的所有车辆数据
        if user_id == '' or user_id == 1:
            continue
        else:
            truck_list = Vehicle.objects.filter(enterprise_id=user_id).filter(number=number)

        if truck_list:
            truck = truck_list[0]
        else:
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

        truck.save()

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/vehicle?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)


# 提交全部车辆(request):
def vehicle_submit_all(request):
    # 获取session中的user_id, 根据user_id查询企业
    user_id = int(request.session.get('user_id', ''))
    print(user_id)
    # 查询该企业的所有车辆数据
    if user_id == 1:
        user = User.objects.get(id=user_id)
        limit_number = user.limit_number
        applied_number = Vehicle.objects.exclude(vehicle_type_id=15).filter(status_id__in=[2, 3, 4]).count()
        truck_list = Vehicle.objects.filter(status_id=1)
    elif user_id != '':
        # 查询已提交申请车辆数, 限制提交车辆数
        user = User.objects.get(id=user_id)
        limit_number = user.limit_number

        applied_number = Vehicle.objects.exclude(vehicle_type_id=15).filter(enterprise_id=user_id).\
            filter(status_id__in=[2, 3, 4]).count()

        # 判断是否到达上限, 如果达到, 则只能提交挂车
        if applied_number >= limit_number:
            truck_list = Vehicle.objects.filter(enterprise_id=user_id).filter(status_id=1).\
                filter(vehicle_type_id__in=15)
        else:
            truck_list = Vehicle.objects.filter(enterprise_id=user_id).filter(status_id=1)
    # 判断查询结果集是否为空
    # [{'id': 9796, 'number': '津AQ5028', 'enterprise': 24, 'route': '津北线，复康路'},]
    if truck_list:
        for truck in truck_list:
            # 如果到达提交上限, 并且车辆类型不是挂车, 退出本次循环
            if (applied_number >= limit_number) and (truck.vehicle_type_id != 15):
                continue
            # 判断信息是否填写完整
            vehicle_type = truck.vehicle_type_id
            number = str(truck.number).strip()
            engine = str(truck.engine).strip()
            vehicle_model = str(truck.vehicle_model).strip()
            register_date = str(truck.register_date).strip()
            route = str(truck.route).strip()

            could_submit = True
            if vehicle_type not in [1, 2, 15]:
                could_submit = False
            elif len(number) == 0 or number == 'None':
                could_submit = False
            # 正则匹配车牌号码, 不正确不能提交
            elif vehicle_type == 15 and (re.match(r'^[\W][A-Z][A-Z0-9]{4}$', number, re.A) is None):
                could_submit = False
            elif vehicle_type != 15 and (re.match(r'^[\W][A-Z][A-Z0-9]{5}$', number, re.A) is None):
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
                        Vehicle.objects.filter(id=truck.id).update(status_id=3)   # 暂时都提交到交管局,设置为3, 如果需要提交到环保局, 改为2
                    else:
                        Vehicle.objects.filter(id=truck.id).update(status_id=3)

                    Vehicle.objects.filter(id=truck.id).update(submit_time=time.strftime('%Y-%m-%d %H:%M:%S',
                                                                                         time.localtime()))

                    # 已提交车辆数+1
                    if truck.vehicle_type_id != 15:
                        applied_number += 1
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

    # 构建返回url
    number = request.session.get('number', '')
    status = request.session.get('status', '')
    page_num = request.session.get('page_num', '')
    url = '/vehicle?number=%s&page_num=%s&status=%s' % (number, page_num, status)

    return HttpResponseRedirect(url)