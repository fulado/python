"""
大队功能
"""
from django.shortcuts import render, HttpResponseRedirect

from .models import Vehicle, Mark, User
from .decorator import login_check
from .utils import MyPaginator


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

    # 保存页码和搜索信息
    request.session['page_num'] = page_num
    request.session['number'] = number

    return render(request, 'dadui/vehicle_mark.html', context)


# 车辆标记
def vehicle_mark(request):
    user_id = request.session.get('user_id', '')
    dept_id = (User.objects.get(id=user_id)).dept_id

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
    mark_info.user_id = user_id

    if mark_reason == 61:
        mark_info.mark_time = mark_time
        mark_info.mark_position = mark_position
    else:
        pass

    mark_info.save()

    vehicle_info = Vehicle.objects.get(id=vehicle_id)
    vehicle_info.mark_cnt += 1
    vehicle_info.vehicle_status_id = 6 if vehicle_info.mark_cnt < 3 else 5

    # 如果是新被标记的测量，车辆所属用户累计标记车辆
    if vehicle_info.mark_cnt == 1:
        user_info = vehicle_info.vehicle_user
        user_info.marked_vehicle_cnt += 1

        # 如果被标记车辆大于等于10辆，冻结该用户
        if user_info.marked_vehicle_cnt >= 10:
            user_info.status_id = 72

        user_info.save()

    vehicle_info.save()

    # 获取页码和搜索信息
    page_num = int(request.session.get('page_num', 1))
    number = request.session.get('number', '')

    url = '/dadui/vehicle_mark_show/?page_num=%d&number=%s' % (page_num, number)

    return HttpResponseRedirect(url)


# 显示解除标记
@login_check
def mark(request):
    page_num = request.GET.get('page_num', 1)
    number = request.GET.get('number', '')

    user_id = request.session.get('user_id', '')
    user_info = User.objects.get(id=user_id)

    if number == '' or number is None:
        mark_list = Mark.objects.filter(dept_id=user_info.dept_id)
    else:
        mark_list = Mark.objects.filter(dept_id=user_info.dept_id).filter(vehicle__vehicle_number__contains=number)

    # 分页
    mp = MyPaginator()
    mp.paginate(mark_list, 10, page_num)

    context = {'mp': mp,
               'number': number
               }

    # 保存页码和搜索信息
    request.session['page_num'] = page_num
    request.session['number'] = number

    return render(request, 'dadui/mark.html', context)


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

    # 如果是新被标记的数量为0，车辆所属用户累计标记车辆-1
    if vehicle_info.mark_cnt <= 0:
        user_info = vehicle_info.vehicle_user
        user_info.marked_vehicle_cnt -= 1 if user_info.marked_vehicle_cnt > 0 else 0

    user_info.save()

    # 获取页码和搜索信息
    page_num = int(request.session.get('page_num', 1))
    number = request.session.get('number', '')

    url = '/dadui/mark/?page_num=%d&number=%s' % (page_num, number)

    return HttpResponseRedirect(url)












