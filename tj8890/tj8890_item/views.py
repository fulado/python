from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from .models import Item, Cate, Dept
from tj8890.utils import MyPaginator
import random
import time
import xlrd
from tj8890.decorator import login_check

STATUS_LIST = ['全部', '未转办', '已转办', '办理中', '已反馈', '已超时', '退回重办', '申请延期', '催办', '退驳', '办结']

STATUS_DIC = {0: '全部',
              1: '未转办',
              2: '已转办',
              3: '办理中',
              4: '已反馈',
              5: '已超时',
              6: '退回重办',
              7: '申请延期',
              8: '催办',
              9: '退驳',
              66: '办结'
              }
EMERGENCY_LIST = ['全部', '普通(3天)', '加急(2天)', '紧急(当日回复)', '特急(两小时内回复)']


# 创建n条事件数据
def create_item(request):
    print(1)
    for i in range(1, 135):
        item = Item()
        # if i < 10:
        #     item.id = '20170411000' + str(i)
        # elif i < 100:
        #     item.id = '2017041100' + str(i)
        # else:
        #     item.id = '201704110' + str(i)
        item.summary = '''市民来电：2014年4月份违章，但是当时车辆和驾驶证被红桥支队扣下了，现在市民多个途径寻找驾驶证，但均未找到。
        处理当时的违法需要驾驶证，如果撤销不了违法信息接受处罚就不能换本或者是重新学驾驶证。张继德，120224198310131715，津GQ3901。
        现在市民咨询，这种情况该怎么办？'''
        item.order_id = 'GD2016122113557102'
        item.source = '电话语音'
        item.sh_phone = '18622940896'
        item.sh_person = '张先生'
        item.area = '和平区'
        item.recoder = '李申'
        item.emergency = random.randint(1, 4)
        item.status_id = random.randint(1, 7)
        item.category1_id = random.randint(1, 3)
        item.category2_id = random.randint(4, 12)

        if item.category2_id == 4:
            item.category3_id = random.randint(13, 18)
        elif item.category2_id == 5:
            item.category3_id = random.randint(19, 24)
        elif item.category2_id == 11:
            item.category3_id = random.randint(34, 38)
        elif item.category2_id == 12:
            item.category3_id = random.randint(39, 41)

        if item.category3_id == 19:
            item.category4_id = random.randint(42, 44)
        elif item.category3_id == 20:
            item.category4_id = random.randint(45, 47)
        elif item.category3_id == 23:
            item.category4_id = random.randint(52, 54)
        elif item.category3_id == 39:
            item.category4_id = random.randint(56, 68)
        elif item.category3_id == 40:
            item.category4_id = random.randint(60, 74)

        # if item.category4_id is not None:
        #     cate_name = Category.objects.get(id=item.category4_id).name
        # else:
        #     cate_name = '驾驶证丢失'
        # item.title = cate_name

        # 生成随机时间 '2016-12-21 15:49:20'
        str_time = '2018-%d-%d %d:%d:%d' % (random.randint(1, 12), random.randint(1, 28),
                                            random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        item.recd_time = str_time
        item.deliver_time = str_time
        item.save()

    return HttpResponse('创建成功')


# 显示main页面
@login_check
def main_show(request):
    # 查询各类事项数量
    count_0 = Item.objects.all().count()
    count_1 = Item.objects.filter(status=1).count()
    count_2 = Item.objects.filter(status=2).count()
    count_3 = Item.objects.filter(status=3).count()
    count_4 = Item.objects.filter(status=4).count()
    count_5 = Item.objects.filter(status=5).count()
    count_6 = Item.objects.filter(status=6).count()
    count_7 = Item.objects.filter(status=7).count()

    context = {'count_0': count_0,
               'count_1': count_1,
               'count_2': count_2,
               'count_3': count_3,
               'count_4': count_4,
               'count_5': count_5,
               'count_6': count_6,
               'count_7': count_7,
               }

    return render(request, 'main.html', context)


# 显示各类别事项页面
@login_check
def all_show(request):
    # 获得办单提交的信息
    cate = int(request.GET.get('cate', 0))
    status = int(request.GET.get('status', 0))
    emergency = int(request.GET.get('emergency', 0))
    accept_time_begin = request.GET.get('accept_time_begin', '0')
    accept_time_end = request.GET.get('accept_time_end', '0')
    keyword = request.GET.get('keyword', '')

    # 获取分项title
    second_title = STATUS_DIC[status]
    title = ['办理事项管理', second_title]

    # 将检索信息保存到session
    request.session['second_title'] = second_title
    request.session['cate'] = cate
    request.session['status'] = status
    request.session['emergency'] = emergency
    request.session['accept_time_begin'] = accept_time_begin
    request.session['accept_time_end'] = accept_time_end
    request.session['keyword'] = keyword

    # 查询事项全部事项
    item_list = Item.objects.all().order_by('-receive_time')

    # 根据用户所在部门过滤检索结果
    authority = request.session.get('authority', 2)

    if authority == 3:
        dept_id = request.session.get('dept_id', 0)

        if dept_id != 0:
            item_list = item_list.filter(assign_dept_id=dept_id)

    # 按照表单中的的信息进行过滤
    if accept_time_begin == '0':
        accept_time_begin = time.strftime('%Y-01-01', time.localtime())

    if accept_time_end == '0':
        accept_time_end = time.strftime('%Y-%m-%d', time.localtime())

    item_list = item_list.filter(accept_time__lte=accept_time_end)
    item_list = item_list.filter(accept_time__gte=accept_time_begin)

    if cate != 0:
        item_list = item_list.filter(cate_id=cate)

    if status != 0:
        item_list = item_list.filter(status=status)

    if emergency != 0:
        item_list = item_list.filter(emergency=emergency)

    # 关键字检索
    if keyword != '':
        item_list = item_list.filter(id__contains=keyword)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))
    # 分页
    mp = MyPaginator()
    mp.paginate(item_list, 10, page_num)

    context = {
               # 'title': title,
               # 'status': status,
               # 'emergency': emergency,
               # 'mp': mp,
               # 'cate_list': cate1_list,
               # 'status_list': STATUS_LIST,
               'emergency_list': EMERGENCY_LIST,
               # 'cate1': cate1,
               # 'cate2': cate2,
               # 'cate3': cate3,
               # 'cate4': cate4,
               # 'recd_time_begin': recd_time_begin,
               # 'recd_time_end': recd_time_end,
               # 'deliver_time_begin': deliver_time_begin,
               # 'deliver_time_end': deliver_time_end,
               # 'default_time_begin': default_time_begin,
               # 'default_time_end': default_time_end,
               }

    return render(request, 'item/all.html', context)


# 查询事项分类
# def cate_search(request):
#     parent_id = request.GET.get('parent_id')
#
#     # 查询数据
#     cate_list = Category.objects.filter(cate_id=parent_id)
#
#     # 构建返回的Json数组格式数据
#     data = []
#     for cate in cate_list:
#         cate_info = {'id': cate.id, 'name': cate.name}
#         data.append(cate_info)
#
#     return JsonResponse({'cate_list': data})


# 未转办事项详情
@login_check
def detail_show(request):
    title = ['办理事项管理', '事项详情']

    # 获取事项id
    item_id = request.GET.get('id', '0')

    # 根据id查询事项
    item_info = Item.objects.get(id=item_id)

    # 查询部门
    supervisor_list = Dept.objects.filter(supervisor__isnull=True).filter(is_delete=False)

    context = {'title': title,
               'item': item_info,
               'supervisor_list': supervisor_list,
               }

    return render(request, 'item/detail.html', context)


# 转办
def deliver_action(request):
    item_id = request.GET.get('item_id', '0')
    dept_id = request.GET.get('assign_dept_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 2
    item_info.assign_dept_id = dept_id
    item_info.deliver_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 撤销转办
def deliver_cancel(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 1
    item_info.assign_dept_id = None
    item_info.deliver_time = None

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 催办
def remind_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 8

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 退回重办
def return_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 6

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 办结保存
def save_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 66

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 同意延期
def delay_approve_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 3

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 驳回延期
def delay_reject_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 3

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 客户端接受转办事项
def accept_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 3

    # 保存办理部门
    dept_id = request.session.get('dept_id', 0)
    item_info.agency_dept_id = dept_id

    # 保存受理人&受理时间
    user = request.session.get('user')
    item_info.receiver = user
    item_info.receive_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 客户端拒收转办事项
def reject_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 1
    item_info.assign_dept_id = None

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 客户端提交办结
def complete_item(request):
    item_id = request.GET.get('item_id', '0')
    item_result = request.GET.get('item_result', '')
    # item_answer = request.GET.get('item_answer', '')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 66
    item_info.result = item_result
    # item_Info.answer = item_answer

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 客户端申请延期
def delay_item(request):
    item_id = request.GET.get('item_id', '0')
    delay_reason = request.GET.get('delay_reason', '')
    delay_to_time = request.GET.get('delay_to_time', '')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 7
    item_info.delay_reason = delay_reason
    item_info.delay_apply_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
    item_info.delay_to_time = delay_to_time

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    second_title = request.session.get('second_title', '全部事项')
    cate1 = request.session.get('cate1', 0)
    cate2 = request.session.get('cate2', 0)
    cate3 = request.session.get('cate3', 0)
    cate4 = request.session.get('cate4', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    recd_time_begin = request.session.get('recd_time_begin', 0)
    recd_time_end = request.session.get('recd_time_end', 0)
    deliver_time_begin = request.session.get('deliver_time_begin', 0)
    deliver_time_end = request.session.get('deliver_time_end', 0)
    keyword = request.session.get('keyword', '')

    url = '/item/all?title=%s&cate1=%s&cate2=%s&cate3=%s&cate4=%s&status=%s&emergency=%s&recd_time_begin=%s&' \
          'recd_time_end=%s&deliver_time_begin=%s&deliver_time_end=%s&keyword=%s' % \
          (second_title, cate1, cate2, cate3, cate4, status, emergency, recd_time_begin, recd_time_end,
           deliver_time_begin, deliver_time_end, keyword)

    return HttpResponseRedirect(url)


# 导入事项数据
def import_excel(request):
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

        try:
            # 创建一条事项数据
            item_info = Item()

            item_info.order_id = worksheet.cell_value(i, 0)  # 工单编号
            item_info.source = worksheet.cell_value(i, 1)  # 求助来源
            item_info.sh_phone = worksheet.cell_value(i, 3)  # 求助号码
            item_info.sh_person = worksheet.cell_value(i, 4)  # 求助人员
            item_info.c_phone = worksheet.cell_value(i, 5)  # 联系电话
            item_info.area = worksheet.cell_value(i, 8)  # 所在区域
            item_info.recorder = worksheet.cell_value(i, 12)  # 录入人员
            item_info.recd_time = worksheet.cell_value(i, 13)  # 录入时间
            item_info.title = worksheet.cell_value(i, 20)  # 标题
            item_info.summary = worksheet.cell_value(i, 21)  # 内容摘要

            item_info.save()
            # print(item_info.order_id)
            # print(item_info.source)
            # print(item_info.title)
            # print(item_info.summary)
            # print(i)
        except Exception as e:
            print(e)

    return HttpResponseRedirect('/item/all')
