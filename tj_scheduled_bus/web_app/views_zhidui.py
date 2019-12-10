"""
支队功能
"""
from django.shortcuts import render, HttpResponseRedirect


from .models import Enterprise, Vehicle, Statistic
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

    return render(request, 'zhidui/enterprise.html', context)


# 企业审核通过
def enterprise_pass(request):
    enterprise_id = request.POST.get('enterprise_id', '')

    Enterprise.objects.filter(id=enterprise_id).update(enterprise_status=3, enterprise_reason='')

    return HttpResponseRedirect('/zhidui/enterprise/')


# 企业审核不通过
def enterprise_refuse(request):
    enterprise_id = request.POST.get('enterprise_id', '')
    enterprise_reason = request.POST.get('refuse_reason', '')

    enterprise_info = Enterprise.objects.get(id=enterprise_id)

    if enterprise_info.enterprise_status_id == 2:
        enterprise_info.enterprise_status_id = 4
    else:
        enterprise_info.enterprise_status_id = 5

    enterprise_info.enterprise_reason = enterprise_reason

    enterprise_info.save()

    return HttpResponseRedirect('/zhidui/enterprise/')


# 显示车辆审核页面
@login_check
def vehicle(request):
    vehicle_list = Vehicle.objects.all()

    # 分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, 1)

    context = {'mp': mp}

    return render(request, 'zhidui/vehicle.html', context)


# 车辆审核通过
def vehicle_pass(request):
    vehicle_id = request.POST.get('vehicle_id', '')

    Vehicle.objects.filter(id=vehicle_id).update(vehicle_status=3)
    Vehicle.objects.filter(id=vehicle_id).update(vehicle_reason='')

    return HttpResponseRedirect('/zhidui/vehicle/')


# 车辆审核不通过
def vehicle_refuse(request):
    vehicle_id = request.POST.get('vehicle_id', '')
    vehicle_reason = request.POST.get('refuse_reason', '')

    vehicle_info = Vehicle.objects.get(id=vehicle_id)

    if vehicle_info.vehicle_status_id == 2:
        vehicle_info.vehicle_status_id = 4
    else:
        vehicle_info.vehicle_status_id = 5

    vehicle_info.vehicle_reason = vehicle_reason

    vehicle_info.save()

    return HttpResponseRedirect('/zhidui/vehicle/')


# 显示通行证信息
@login_check
def permission(request):
    enterprise_name = request.POST.get('enterprise_name', '')

    statistic_list = Statistic.objects.filter(sta_enterprise__enterprise_name__contains=enterprise_name)

    # 分页
    mp = MyPaginator()
    mp.paginate(statistic_list, 10, 1)

    context = {'enterprise_name': enterprise_name,
               'mp': mp
               }

    return render(request, 'zhidui/permit.html', context)






























