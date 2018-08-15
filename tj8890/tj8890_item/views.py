from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.http import JsonResponse
from .models import Item, Category, Dept
from tj8890.utils import MyPaginator
import random
import time

STATUS_LIST = ['全部', '未转办', '已转办', '办理中', '已反馈', '已超时', '退回重办', '申请延期']
EMERGENCY_LIST = ['全部', '普通(3天)', '加急(2天)', '紧急(当日回复)', '特急(两小时内回复)']


# 创建n条事件数据
def create_item(request):
    for i in range(1, 135):
        item = Item()
        if i < 10:
            item.id = '20170411000' + str(i)
        elif i < 100:
            item.id = '2017041100' + str(i)
        else:
            item.id = '201704110' + str(i)
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
        item.status = random.randint(1, 7)
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

        if item.category4_id is not None:
            cate_name = Category.objects.get(id=item.category4_id).name
        else:
            cate_name = '驾驶证丢失'
        item.title = cate_name

        # 生成随机时间 '2016-12-21 15:49:20'
        str_time = '20%d-%d-%d %d:%d:%d' % (random.randint(10, 18), random.randint(1, 12), random.randint(1, 28),
                                            random.randint(0, 23), random.randint(0, 59), random.randint(0, 59))
        item.recd_time = str_time
        item.deliver_time = str_time
        item.save()

    return HttpResponse('创建成功')


# 显示main页面
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
def all_show(request):
    # 获取分项title
    second_title = request.GET.get('title')
    title = ['办理事项管理', second_title]

    # 获得办单提交的信息
    cate1 = int(request.GET.get('cate1', 0))
    cate2 = int(request.GET.get('cate2', 0))
    cate3 = int(request.GET.get('cate3', 0))
    cate4 = int(request.GET.get('cate4', 0))
    status = int(request.GET.get('status', 0))
    emergency = int(request.GET.get('emergency', 0))
    recd_time_begin = request.GET.get('recd_time_begin', 0)
    recd_time_end = request.GET.get('recd_time_end', 0)
    deliver_time_begin = request.GET.get('deliver_time_begin', 0)
    deliver_time_end = request.GET.get('deliver_time_end', 0)

    # 查询事项全部事项
    item_list = Item.objects.all().order_by('-recd_time')

    # 按照表单中的的信息进行过滤
    if recd_time_begin == 0:
        recd_time_begin = time.strftime('%Y-1-1', time.localtime())
    else:
        item_list = item_list.filter(recd_time__gte=recd_time_begin)
    if recd_time_end == 0:
        recd_time_end = time.strftime('%Y-%m-%d', time.localtime())
    else:
        item_list = item_list.filter(recd_time__lte=recd_time_end)

    if deliver_time_begin == 0:
        deliver_time_begin = time.strftime('%Y-1-1', time.localtime())
    else:
        item_list = item_list.filter(deliver_time__gte=deliver_time_begin)
    if deliver_time_end == 0:
        deliver_time_end = time.strftime('%Y-%m-%d', time.localtime())
    else:
        item_list = item_list.filter(deliver_time__lte=deliver_time_end)

    # 按照服务器的时间, 把默认起止事件传给客户端
    default_time_begin = time.strftime('%Y-1-1', time.localtime())
    default_time_end = time.strftime('%Y-%m-%d', time.localtime())

    if cate1 != 0:
        item_list = item_list.filter(category1_id=cate1)
        print('cate1: %d' % (len(item_list)))
    if cate2 != 0:
        item_list = item_list.filter(category2_id=cate2)
        print('cate2: %d' % (len(item_list)))
    if cate3 != 0:
        item_list = item_list.filter(category3_id=cate3)
        print('cate3: %d' % (len(item_list)))
    if cate4 != 0:
        item_list = item_list.filter(category4_id=cate4)
        print('cate4: %d' % (len(item_list)))
    if status != 0:
        print('status: %d' % status)
        item_list = item_list.filter(status=status)
        print('status: %d' % (len(item_list)))
    if emergency != 0:
        print(emergency)
        item_list = item_list.filter(emergency=emergency)
        print('emergency: %d' % (len(item_list)))

    # 事项分类
    cate1_list = Category.objects.filter(level=1)
    cate2_list = Category.objects.filter(level=2)
    cate3_list = Category.objects.filter(cate_id=cate2)
    cate4_list = Category.objects.filter(cate_id=cate3)

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))
    # 分页
    mp = MyPaginator()
    mp.paginate(item_list, 10, page_num)

    context = {'title': title,
               'status': status,
               'emergency': emergency,
               'mp': mp,
               'cate1_list': cate1_list,
               'cate2_list': cate2_list,
               'cate3_list': cate3_list,
               'cate4_list': cate4_list,
               'status_list': STATUS_LIST,
               'emergency_list': EMERGENCY_LIST,
               'cate1': cate1,
               'cate2': cate2,
               'cate3': cate3,
               'cate4': cate4,
               'recd_time_begin': recd_time_begin,
               'recd_time_end': recd_time_end,
               'deliver_time_begin': deliver_time_begin,
               'deliver_time_end': deliver_time_end,
               'default_time_begin': default_time_begin,
               'default_time_end': default_time_end,
               }

    return render(request, 'item/all.html', context)


# 查询事项分类
def cate_search(request):
    parent_id = request.GET.get('parent_id')

    # 查询数据
    cate_list = Category.objects.filter(cate_id=parent_id)

    # 构建返回的Json数组格式数据
    data = []
    for cate in cate_list:
        cate_info = {'id': cate.id, 'name': cate.name}
        data.append(cate_info)

    return JsonResponse({'cate_list': data})


# 未转办事项详情
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

    item_info.save()

    return HttpResponseRedirect('/item/detail?id=%s' % item_info.id)
