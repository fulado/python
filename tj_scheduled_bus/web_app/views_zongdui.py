"""
交管局功能
"""
from django.shortcuts import render, HttpResponseRedirect
from django.http import JsonResponse


from .models import Enterprise, Vehicle, User, Station, Department
from .decorator import login_check
from .utils import MyPaginator


import hashlib


# 显示企业审核页面
@login_check
def enterprise(request):
    enterprise_list = Enterprise.objects.all()

    # 分页
    mp = MyPaginator()
    mp.paginate(enterprise_list, 10, 1)

    context = {'mp': mp}

    return render(request, 'zongdui/enterprise.html', context)


# 显示车辆审核页面
@login_check
def vehicle(request):
    vehicle_list = Vehicle.objects.all()

    # 分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, 1)

    context = {'mp': mp}

    return render(request, 'zongdui/vehicle.html', context)


# 显示站点信息页面
@login_check
def station(request):
    page_num = request.GET.get('page_num', 1)
    search_name = request.POST.get('search_name', '')

    station_list = Station.objects.filter(station_name__contains=search_name)

    # 分页
    mp = MyPaginator()
    mp.paginate(station_list, 10, page_num)

    context = {'mp': mp,
               'page_num': page_num
               }

    return render(request, 'zongdui/station.html', context)


# 添加站点
def station_add(request):
    station_area = request.POST.get('station_area', '')
    station_road = request.POST.get('station_road', '')
    station_direction = request.POST.get('station_direction', '')
    station_name = request.POST.get('station_name', '')
    station_position = request.POST.get('station_position', '')

    station_status = int(request.POST.get('station_status', 31))

    station_info = Station()
    station_info.station_area = station_area
    station_info.station_road = station_road
    station_info.station_direction = station_direction
    station_info.station_name = station_name
    station_info.station_position = station_position
    station_info.station_status_id = station_status

    station_info.save()

    return HttpResponseRedirect('/zongdui/station')


# 编辑站点
def station_modify(request):
    station_id = request.POST.get('station_id', None)

    if station_id:
        station_area = request.POST.get('station_area', '')
        station_road = request.POST.get('station_road', '')
        station_direction = request.POST.get('station_direction', '')
        station_name = request.POST.get('station_name', '')
        station_position = request.POST.get('station_position', '')
        station_status = int(request.POST.get('station_status', 31))

        station_info = Station.objects.get(id=station_id)

        station_info.station_area = station_area
        station_info.station_road = station_road
        station_info.station_direction = station_direction
        station_info.station_name = station_name
        station_info.station_position = station_position
        station_info.station_status_id = station_status

        station_info.save()
    else:
        pass

    return HttpResponseRedirect('/zongdui/station')


# 删除站点
def station_delete(request):
    station_id = request.POST.get('station_id', None)

    if station_id:
        Station.objects.filter(id=station_id).delete()
    else:
        pass

    return HttpResponseRedirect('/zongdui/station')


# 显示支队行号管理
@login_check
def account(request):
    page_num = request.GET.get('page_num', 1)
    search_name = request.POST.get('search_name', '')

    user_list = User.objects.filter(username__contains=search_name)
    dept_list = Department.objects.all()

    # 分页
    mp = MyPaginator()
    mp.paginate(user_list, 10, page_num)

    context = {'mp': mp,
               'page_num': page_num,
               'search_name': search_name,
               'dept_list': dept_list
               }

    return render(request, 'zongdui/account.html', context)


# 是否可以添加账号
def can_add_account(request):
    username = request.GET.get('username', '')

    if User.objects.filter(username=username).exists():
        result = False
    else:
        result = True

    return JsonResponse({'result': result})


# 添加账号
def account_add(request):
    username = request.POST.get('username', '')
    password = request.POST.get('password', '')
    dept_id = request.POST.get('dept_id', '')
    person_name = request.POST.get('person_name', '')
    person_id = request.POST.get('person_id', '')
    phone = request.POST.get('phone', '')

    user_info = User()

    user_info.username = username
    user_info.password = hashlib.sha1(password.encode('utf8')).hexdigest()
    user_info.dept_id = dept_id
    user_info.person_name = person_name
    user_info.person_id = person_id
    user_info.phone = phone

    if dept_id == 1:
        user_info.authority = 3
    else:
        user_info.authority = 2

    user_info.save()

    return HttpResponseRedirect('/zongdui/account')


# 修改账号
def account_modify(request):
    password = request.POST.get('password', '')
    dept_id = request.POST.get('dept_id', '')
    person_name = request.POST.get('person_name', '')
    person_id = request.POST.get('person_id', '')
    phone = request.POST.get('phone', '')
    user_id = request.POST.get('user_id', '')

    user_info = User.objects.get(id=user_id)

    if password != '!!!!!!!!!!':
        user_info.password = password
    else:
        pass

    user_info.dept_id = dept_id
    user_info.person_name = person_name
    user_info.person_id = person_id
    user_info.phone = phone

    user_info.save()

    return HttpResponseRedirect('/zongdui/account')


# 删除账号
def account_delete(request):
    user_id = request.POST.get('user_id', None)

    if user_id:
        User.objects.filter(id=user_id).delete()
    else:
        pass

    return HttpResponseRedirect('/zongdui/account')


# 冻结账号
def account_lock(request):
    user_id = request.POST.get('user_id', None)
    reason = request.POST.get('reason', '')

    if user_id:
        User.objects.filter(id=user_id).update(reason=reason, status=72)
    else:
        pass

    return HttpResponseRedirect('/zongdui/account')


# 解冻账号
def account_unlock(request):
    user_id = request.GET.get('user_id', None)

    if user_id:
        User.objects.filter(id=user_id).update(reason='', status=71)
    else:
        pass

    return HttpResponseRedirect('/zongdui/account')























