"""
支队功能
"""
from django.shortcuts import render, HttpResponseRedirect


from .models import Enterprise, Vehicle, Statistic, Department, Mark, User
from .decorator import login_check
from .utils import MyPaginator


# 显示企业审核页面
@login_check
def enterprise(request):
    user_id = request.session.get('user_id', '')
    user_info = User.objects.get(id=user_id)
    search_name = request.GET.get('search_name', '')
    page_num = request.GET.get('page_num', 1)

    enterprise_list = Enterprise.objects.filter(dept_id=user_info.dept_id, enterprise_name__contains=search_name)

    # 分页
    mp = MyPaginator()
    mp.paginate(enterprise_list, 10, page_num)

    context = {'mp': mp,
               'search_name': search_name,
               }

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
    user_id = request.session.get('user_id', '')
    user_info = User.objects.get(id=user_id)
    user_list = User.objects.filter(dept_id=user_info.dept_id)
    page_num = request.GET.get('page_num', 1)
    number = request.GET.get('number', '')

    user_id_list = []
    for user_info in user_list:
        user_id_list.append(user_info.id)

    vehicle_list = Vehicle.objects.filter(vehicle_user_id__in=user_id_list)

    # 分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, page_num)

    context = {'mp': mp,
               'number': number,
               }

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


# 车辆标记
def vehicle_mark(request):
    user_id = request.session.get('user_id', '')
    dept_id = Department.objects.get(user_id=user_id).id

    vehicle_id = request.POST.get('vehicle_id', '')
    mark_time = request.POST.get('mark_time', '')
    mark_position = request.POST.get('mark_position', '')
    mark_reason = int(request.POST.get('mark_reason', 61))
    mark_content = request.POST.get('mark_content', '')

    mark_info = Mark()

    mark_info.mark_reason_id = mark_reason
    mark_info.mark_content = mark_content
    mark_info.vehicle_id = vehicle_id
    mark_info.dept_id = dept_id

    if mark_reason == 61:
        mark_info.mark_time = mark_time
        mark_info.mark_position = mark_position
    else:
        pass

    mark_info.save()

    vehicle_info = Vehicle.objects.get(id=vehicle_id)
    vehicle_info.mark_cnt += 1
    vehicle_info.vehicle_status_id = 6 if vehicle_info.mark_cnt < 3 else 5

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


# 显示支队信息
@login_check
def department(request):
    user_id = request.session.get('user_id', '')
    user_info = User.objects.get(id=user_id)

    dept_list = Department.objects.filter(id=user_info.dept_id)

    # 分页
    mp = MyPaginator()
    mp.paginate(dept_list, 10, 1)

    context = {'mp': mp,
               }

    return render(request, 'zhidui/department.html', context)


# 保存支队信息
def department_modify(request):
    dept_name = request.POST.get('dept_name', '')
    dept_address = request.POST.get('dept_address', '')
    dept_phone = request.POST.get('dept_phone', '')
    dept_id = request.POST.get('dept_id', '')

    print(dept_name, dept_address, dept_phone, dept_id)

    Department.objects.filter(id=dept_id).update(dept_name=dept_name, dept_address=dept_address, dept_phone=dept_phone)

    return HttpResponseRedirect('/zhidui/department')


# 显示标记车辆页面
@login_check
def vehicle_mark_show(request):
    page_num = request.GET.get('page_num', 1)
    number = request.GET.get('number', '')

    vehicle_list = Vehicle.objects.filter(vehicle_number__contains=number).exclude(vehicle_status_id__in=(1, 2, 4))

    # 分页
    mp = MyPaginator()
    mp.paginate(vehicle_list, 10, page_num)

    context = {'mp': mp,
               'number': number,
               }

    return render(request, 'zhidui/vehicle_mark.html', context)


# 显示车辆标记信息
@login_check
def mark(request):
    user_id = request.session.get('user_id', '')
    user_info = User.objects.get(id=user_id)

    mark_list = Mark.objects.filter(dept_id=user_info.dept_id)

    # 分页
    mp = MyPaginator()
    mp.paginate(mark_list, 10, 1)

    context = {'mp': mp,
               }

    return render(request, 'zhidui/mark.html', context)


# 解除标记
def mark_delete(request):
    mark_id = request.POST.get('mark_id', '')

    mark_info = Mark.objects.get(id=mark_id)

    vehicle_info = Vehicle.objects.get(id=mark_info.vehicle_id)
    vehicle_info.mark_cnt -= 1

    if vehicle_info.mark_cnt <= 0:
        vehicle_info.vehicle_status_id = 3
    elif vehicle_info.mark_cnt < 3:
        vehicle_info.vehicle_status_id = 6
    else:
        vehicle_info.vehicle_status_id = 5

    vehicle_info.save()
    mark_info.delete()

    return HttpResponseRedirect('/zhidui/mark')


# 解冻车辆
def vehicle_unlock(request):
    vehicle_id = request.POST.get('vehicle_id', '')

    vehicle_info = Vehicle.objects.get(id=vehicle_id)

    if vehicle_info.mark_cnt > 0:
        vehicle_info.vehicle_status_id = 6
    else:
        vehicle_info.vehicle_status_id = 3

    vehicle_info.vehicle_reason = ''

    vehicle_info.save()

    return HttpResponseRedirect('/zhidui/vehicle')
























