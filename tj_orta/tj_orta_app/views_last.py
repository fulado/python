from django.shortcuts import render
from .models import Backup1
from tj_orta.utils import MyPaginator


# 显示本月车辆下载页面
def show_page(request):
    # 获取session中的user_id, 根据user_id查询企业
    user_id = int(request.session.get('user_id', ''))

    # 查询该企业的所有车辆数据
    if user_id != '' and user_id != 1:
        vehicle_list = Backup1.objects.filter(enterprise_id=user_id).order_by('id')
    else:
        vehicle_list = Backup1.objects.all().order_by('id')

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

    context = {'mp': mp, 'number': number, 'status': status}

    # 保存页面状态到session
    request.session['number'] = number
    request.session['status'] = status
    request.session['page_num'] = page_num

    return render(request, 'last.html', context)
