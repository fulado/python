"""
交管局功能
"""
from django.shortcuts import render, HttpResponseRedirect


from .models import Enterprise, Vehicle, User, Station
from .decorator import login_check
from .utils import MyPaginator


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

    # 分页
    mp = MyPaginator()
    mp.paginate(user_list, 10, page_num)

    context = {'mp': mp,
               'page_num': page_num,
               'search_name': search_name,
               }

    return render(request, 'zongdui/account.html', context)































