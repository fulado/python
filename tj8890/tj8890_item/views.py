from django.shortcuts import HttpResponse, HttpResponseRedirect, render
from django.http import JsonResponse
from django.db.models import Q
from .models import Item, Cate, Dept, Category
from tj8890.utils import MyPaginator
import random
import time
import xlrd
import xlwt
import io
from tj8890.decorator import login_check

STATUS_LIST = ['全部', '未转办', '已转办', '办理中', '已反馈', '已超时', '退回重办', '申请延期', '催办', '退驳', '办结']

STATUS_DIC = {0: '全部',
              1: '未转办',
              2: '已转办',
              3: '办理中',
              4: '已反馈',
              5: '超时',
              6: '重办',
              7: '申请延期',
              8: '催办',
              9: '退单',
              10: '超时',
              11: '驳回延期',
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
    authority = request.session.get('authority', 2)

    if authority == 2:
        # 查询各类事项数量
        init = Item.objects.filter(status=1).count()
        delivered = Item.objects.filter(status=2).count()
        reject = Item.objects.filter(status=9).count()
        handling = Item.objects.filter(status=3).count()
        urge = Item.objects.filter(status=8).count()
        overtime = Item.objects.filter(status=10).count()
        complete = Item.objects.filter(status=4).count()
        retreat = Item.objects.filter(status=6).count()
        delay = Item.objects.filter(status=7).count()
        refuse = Item.objects.filter(status=11).count()
    else:
        dept_id = request.session.get('dept_id', 0)

        init = 0
        delivered = Item.objects.filter(status=2).filter(assign_dept_id=dept_id).count()
        reject = 0
        handling = Item.objects.filter(status=3).filter(assign_dept_id=dept_id).count()
        urge = Item.objects.filter(status=8).filter(assign_dept_id=dept_id).count()
        overtime = Item.objects.filter(status=10).filter(assign_dept_id=dept_id).count()
        complete = Item.objects.filter(status=4).filter(assign_dept_id=dept_id).count()
        retreat = Item.objects.filter(status=6).filter(assign_dept_id=dept_id).count()
        delay = Item.objects.filter(status=7).filter(assign_dept_id=dept_id).count()
        refuse = Item.objects.filter(status=11).filter(assign_dept_id=dept_id).count()

    context = {'count_init': init,
               'count_delivered': delivered,
               'count_reject': reject,
               'count_handling': handling,
               'count_urge': urge,
               'count_overtime': overtime,
               'count_complete': complete,
               'count_retreat': retreat,
               'count_delay': delay,
               'count_refuse': refuse,
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
    title = ['办理事项管理', second_title + '事项']

    # 查询事项全部事项
    item_list = Item.objects.all().order_by('-accept_time')

    # 根据用户所在部门过滤检索结果
    authority = request.session.get('authority', 2)

    if authority == 3:
        dept_id = request.session.get('dept_id', 0)
        print(dept_id)
        if dept_id != 0:
            item_list = item_list.filter(assign_dept_id=dept_id)

    # 按照表单中的的信息进行过滤
    if accept_time_begin == '0':
        accept_time_begin = time.strftime('%Y-01-01', time.localtime())

    if accept_time_end == '0':
        accept_time_end = time.strftime('%Y-%m-%d', time.localtime())

    accept_time_end_for_query = '%s 23:59:59' % accept_time_end

    item_list = item_list.filter(accept_time__lte=accept_time_end_for_query)
    item_list = item_list.filter(accept_time__gte=accept_time_begin)

    if cate != 0:
        item_list = item_list.filter(cate_id=cate)

    if status != 0:
        item_list = item_list.filter(status=status)

    if emergency != 0:
        item_list = item_list.filter(emergency=emergency)

    # 关键字检索
    if keyword != '':
        item_list = item_list.filter(Q(content__contains=keyword) | Q(id__contains=keyword))

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))
    # 分页
    mp = MyPaginator()
    mp.paginate(item_list, 10, page_num)

    # 将检索信息保存到session
    request.session['title'] = title
    request.session['cate'] = cate
    request.session['status'] = status
    request.session['emergency'] = emergency
    request.session['accept_time_begin'] = accept_time_begin
    request.session['accept_time_end'] = accept_time_end
    request.session['keyword'] = keyword

    # 事项分类
    cate_list = Cate.objects.all()

    context = {
        # 'title': title,
        # 'status': status,
        # 'emergency': emergency,
        'mp': mp,
        # 'cate_list': cate1_list,
        # 'status_list': STATUS_LIST,
        'emergency_list': EMERGENCY_LIST,
        'cate_list': cate_list,
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
def cate_search(request):
    parent_id = int(request.GET.get('parent_id'))

    # 查询数据
    cate_list = Category.objects.filter(cate_id=parent_id)

    # 构建返回的Json数组格式数据
    data = []
    for cate in cate_list:
        cate_info = {'id': cate.id, 'name': cate.name}
        data.append(cate_info)

    return JsonResponse({'cate_list': data})


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

    # 查询事项大类
    cate1_list = Category.objects.filter(level=2)
    # 查询事项二类
    cate1_id = item_info.cate1_id if item_info.cate1_id else cate1_list[0].id
    cate2_list = Category.objects.filter(level=3).filter(cate_id=cate1_id)
    # 查询事项三类
    cate2_id = item_info.cate2_id if item_info.cate2_id else cate2_list[0].id
    cate3_list = Category.objects.filter(level=4).filter(cate_id=cate2_id)

    context = {'title': title,
               'item': item_info,
               'supervisor_list': supervisor_list,
               'cate1_list': cate1_list,
               'cate2_list': cate2_list,
               'cate3_list': cate3_list,
               }

    return render(request, 'item/detail.html', context)


# 删除事项
def delete_item(request):
    try:
        item_id = request.GET.get('item_id')
        Item.objects.get(id=item_id).delete()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 转办
def deliver_action(request):
    item_id = request.GET.get('item_id', '0')
    dept_id = request.GET.get('assign_dept_id', '0')
    dead_time = request.GET.get('dead_time', '')
    cate1_id = int(request.GET.get('cate1', 0))
    cate2_id = int(request.GET.get('cate2', 0))
    cate3_id = int(request.GET.get('cate3', 0))

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 2
    item_info.assign_dept_id = dept_id
    item_info.dead_time = dead_time
    item_info.approval_content = None
    item_info.approval_person = None
    item_info.cate1_id = cate1_id if cate1_id else None
    item_info.cate2_id = cate2_id if cate2_id else None
    item_info.cate3_id = cate3_id if cate3_id else None

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 撤销转办
def deliver_cancel(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 1
    item_info.assign_dept_id = None
    item_info.dead_time = None

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

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
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 退回重办
def return_item(request):
    item_id = request.GET.get('item_id', '0')
    return_reason = request.GET.get('return_reason', '')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 6
    item_info.return_reason = return_reason
    item_info.approval_content = None
    item_info.approval_person = None

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 办结保存
def save_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 66
    item_info.save_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 同意延期
def delay_approve_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 3
    item_info.dead_time = item_info.delay_time
    item_info.approval_content = None
    item_info.approval_person = None
    item_info.delay_time = None
    item_info.delay_reason = None

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 驳回延期
def delay_reject_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 11
    item_info.approval_content = None
    item_info.approval_person = None

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 客户端接受转办事项
def accept_item(request):
    item_id = request.GET.get('item_id', '0')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 3

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 客户端退单
def reject_item(request):
    item_id = request.GET.get('item_id', '0')
    reject_reason = request.GET.get('reject_reason', '')
    approval_content = request.GET.get('approval_content', '')
    approval_person = request.GET.get('approval_person', '')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 9  # 回驳事项
    # item_info.assign_dept_id = None
    item_info.reject_user_id = request.session.get('user_id')
    item_info.reject_reason = reject_reason
    item_info.approval_content = approval_content
    item_info.approval_person = approval_person
    item_info.delay_reason = None
    item_info.delay_time = None

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 客户端提交办结
def complete_item(request):
    item_id = request.GET.get('item_id', '0')
    item_result = request.GET.get('item_result', '')
    approval_content = request.GET.get('approval_content', '')
    approval_person = request.GET.get('approval_person', '')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 4
    item_info.result = item_result
    item_info.approval_content = approval_content
    item_info.approval_person = approval_person
    item_info.return_reason = None

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 客户端申请延期
def delay_item(request):
    item_id = request.GET.get('item_id', '0')
    delay_reason = request.GET.get('delay_reason', '')
    delay_time = request.GET.get('delay_time', '')
    approval_content = request.GET.get('approval_content', '')
    approval_person = request.GET.get('approval_person', '')

    item_info = Item.objects.get(id=item_id)

    item_info.status_id = 7
    item_info.delay_reason = delay_reason
    item_info.delay_time = delay_time
    item_info.approval_content = approval_content
    item_info.approval_person = approval_person

    try:
        item_info.save()
    except Exception as e:
        print(e)

    # 从session中获取检索信息
    cate = request.session.get('cate', 0)
    status = request.session.get('status', 0)
    emergency = request.session.get('emergency', 0)
    accept_time_begin = request.session.get('accept_time_begin', '0')
    accept_time_end = request.session.get('accept_time_end', '0')
    keyword = request.session.get('keyword', '')

    url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
          (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

    return HttpResponseRedirect(url)


# 导入事项数据
def import_excel(request):
    # 获取用户上传的excel文件, 文件不存储, 在内存中对文件进行操作
    excel_file = request.FILES.get('excel_file')

    # 打开excel文件, 直接从内存读取文件内容
    workbook = xlrd.open_workbook(filename=None, file_contents=excel_file.read())

    # 获得sheets列表
    sheets = workbook.sheet_names()

    # 获得第一个sheet对象, 导入办理类数据
    worksheet = workbook.sheet_by_name(sheets[0])

    for i in range(1, worksheet.nrows):
        # ctype： 0-empty, 1-string, 2-number, 3-date, 4-boolean, 5-error
        item_id = worksheet.cell_value(i, 0)

        item_list = Item.objects.filter(id=item_id)

        if item_list:
            item_info = item_list[0]
        else:
            # 创建一条事项数据
            item_info = Item()

            item_info.id = worksheet.cell_value(i, 0)               # 工单编号
            item_info.cate_id = 1                                   # 事项类别
            item_info.person = worksheet.cell_value(i, 4)           # 求助人员
            item_info.area = worksheet.cell_value(i, 8)             # 所在区域
            item_info.title = worksheet.cell_value(i, 20)           # 标题
            item_info.content = worksheet.cell_value(i, 21)         # 内容
            item_info.accept_time = worksheet.cell_value(i, 27)     # 接件时间
            item_info.limit_time = worksheet.cell_value(i, 29)      # 承办时限

            if worksheet.cell_value(i, 5) == '' or worksheet.cell(i, 5).ctype == 0:
                item_info.phone = worksheet.cell_value(i, 3)        # 联系电话
            else:
                item_info.phone = worksheet.cell_value(i, 5)        # 联系电话

            if worksheet.cell_value(i, 14)[0: 2] == '普通':
                item_info.emergency = 1                             # 紧急程度

        try:
            item_info.save()
        except Exception as e:
            print(e)

    # 获取后面4个sheet对象, 导入举报类、投诉类、建议类、表扬类数据
    for j in range(1, 4):
        worksheet = workbook.sheet_by_name(sheets[j])

        for i in range(1, worksheet.nrows):
            item_id = worksheet.cell_value(i, 0)

            item_list = Item.objects.filter(id=item_id)

            if item_list:
                item_info = item_list[0]
            else:
                # 创建一条事项数据
                item_info = Item()

                item_info.id = worksheet.cell_value(i, 0)  # 工单编号
                item_info.cate_id = j + 1  # 事项类别
                item_info.person = worksheet.cell_value(i, 4)  # 求助人员
                item_info.area = worksheet.cell_value(i, 8)  # 所在区域
                item_info.title = worksheet.cell_value(i, 10)  # 标题
                item_info.content = worksheet.cell_value(i, 14)  # 内容

                if worksheet.cell_value(i, 23) != '' and worksheet.cell(i, 23).ctype != 0:
                    item_info.accept_time = worksheet.cell_value(i, 23)  # 接件时间
                if worksheet.cell_value(i, 25) != '' and worksheet.cell(i, 25).ctype != 0:
                    item_info.limit_time = worksheet.cell_value(i, 25)  # 承办时限

                if worksheet.cell_value(i, 7) == '' or worksheet.cell(i, 7).ctype == 0:
                    item_info.phone = worksheet.cell_value(i, 5)  # 联系电话
                else:
                    item_info.phone = worksheet.cell_value(i, 7)  # 联系电话

                if worksheet.cell_value(i, 16)[0: 2] == '普通':
                    item_info.emergency = 1  # 紧急程度

            try:
                item_info.save()
            except Exception as e:
                print(item_info.id, item_info.cate_id, item_info.person, item_info.title)
                print(e)

    return HttpResponseRedirect('/item/all')


# 导出办结事项
def export_excel(request):
    save_time = request.GET.get('save_time', time.strftime('%Y-%m-%d', time.localtime()))
    save_time_begin = '%s 00:00:00' % save_time
    save_time_end = '%s 23:59:59' % save_time

    item_list = Item.objects.filter(status_id=66).filter(save_time__gte=save_time_begin).filter(save_time__lte=
                                                                                                save_time_end)

    if item_list:

        # 创建工作簿
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('sheet1', cell_overwrite_ok=True)

        # 设置表头
        title = ['工单编号', '办理情况', '办理单位']

        # 生成表头
        len_col = len(title)
        for i in range(0, len_col):
            ws.write(0, i, title[i])

        # 写入办结事项数据
        i = 1
        for item_info in item_list:

            # 生成excel内容: ['工单编号', '办理情况', '办理单位']
            content = [item_info.id, item_info.result, item_info.assign_dept.name]

            for j in range(0, len_col):
                ws.write(i, j, content[j])
            i += 1

            # # 修改是否已导出状态
            # item_info.is_exported = True
            # item_info.save()

        # 内存文件操作
        buf = io.BytesIO()

        # 将文件保存在内存中
        wb.save(buf)
        response = HttpResponse(buf.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename=item_completed.xls'
        response.write(buf.getvalue())
        return response
    else:
        # 从session中获取检索信息
        cate = request.session.get('cate', 0)
        status = request.session.get('status', 0)
        emergency = request.session.get('emergency', 0)
        accept_time_begin = request.session.get('accept_time_begin', '0')
        accept_time_end = request.session.get('accept_time_end', '0')
        keyword = request.session.get('keyword', '')

        url = '/item/all?cate=%s&status=%s&emergency=%s&accept_time_begin=%s&accept_time_end=%s&keyword=%s' % \
              (cate, status, emergency, accept_time_begin, accept_time_end, keyword)

        return HttpResponseRedirect(url)


# 判断是否超时
def check_dead_time():
    item_list = Item.objects.filter(status_id__in=[3, 6, 8, 11])

    current_time = time.time()

    for item_info in item_list:

        dead_time = time.mktime(item_info.dead_time.timetuple())
        # print(current_time, dead_time)
        if current_time > dead_time:
            item_info.status_id = 10
            item_info.save()


# 显示各类事项总数
def item_count(request):
    authority = request.session.get('authority', 2)

    if authority == 2:
        # 查询各类事项数量
        init = Item.objects.filter(status=1).count()
        delivered = Item.objects.filter(status=2).count()
        reject = Item.objects.filter(status=9).count()
        handling = Item.objects.filter(status=3).count()
        urge = Item.objects.filter(status=8).count()
        overtime = Item.objects.filter(status=10).count()
        complete = Item.objects.filter(status=4).count()
        retreat = Item.objects.filter(status=6).count()
        delay = Item.objects.filter(status=7).count()
        refuse = Item.objects.filter(status=11).count()
    else:
        dept_id = request.session.get('dept_id', 0)

        init = 0
        delivered = Item.objects.filter(status=2).filter(assign_dept_id=dept_id).count()
        reject = 0
        handling = Item.objects.filter(status=3).filter(assign_dept_id=dept_id).count()
        urge = Item.objects.filter(status=8).filter(assign_dept_id=dept_id).count()
        overtime = Item.objects.filter(status=10).filter(assign_dept_id=dept_id).count()
        complete = Item.objects.filter(status=4).filter(assign_dept_id=dept_id).count()
        retreat = Item.objects.filter(status=6).filter(assign_dept_id=dept_id).count()
        delay = Item.objects.filter(status=7).filter(assign_dept_id=dept_id).count()
        refuse = Item.objects.filter(status=11).filter(assign_dept_id=dept_id).count()

    data = {'init': init,
            'delivered': delivered,
            'reject': reject,
            'handling': handling,
            'urge': urge,
            'overtime': overtime,
            'complete': complete,
            'retreat': retreat,
            'delay': delay,
            'refuse': refuse,
            }

    return JsonResponse(data)


# 显示事项登录页面
def cate_show(request):

    level = int(request.GET.get('level', 1))

    cate1_id = int(request.GET.get('cate1', 0))
    cate2_id = int(request.GET.get('cate2', 0))

    # 获得用户指定的页面
    page_num = int(request.GET.get('page_num', 1))

    # 查询事项大类
    cate1_list = Category.objects.filter(level=2)

    # 查询事项二类
    cate1_id = cate1_id if cate1_id else cate1_list[0].id
    cate1 = Category.objects.get(id=cate1_id)
    cate2_list = Category.objects.filter(level=3).filter(cate_id=cate1_id)

    # 查询事项三类
    cate2 = Category.objects.get(id=cate2_id) if cate2_id else None
    cate3_list = Category.objects.filter(level=4).filter(cate_id=cate2_id)

    if level == 1:
        cate_list = cate1_list
    elif level == 2:
        cate_list = cate2_list
    elif level == 3:
        cate_list = cate3_list
    else:
        cate_list = []

    # 分页
    mp = MyPaginator()
    mp.paginate(cate_list, 10, page_num)

    request.session['level'] = level
    request.session['cate1_id'] = cate1_id
    request.session['cate2_id'] = cate2_id

    context = {
        'level': level,
        'cate1': cate1,
        'cate2': cate2,
        'cate1_id': cate1_id,
        'cate2_id': cate2_id,
        'cate1_list': cate1_list,
        'cate2_list': cate2_list,
        'cate3_list': cate3_list,
        'mp': mp,
    }

    return render(request, 'item/cate.html', context)


# 编辑分类
def cate_modify(request):
    cate_id = int(request.GET.get('cate_id', 0))
    cate_name = request.GET.get('cate_name', 0)
    super_id = int(request.GET.get('super_id', 0))

    cate_list = Category.objects.filter(id=cate_id)

    level = request.session.get('level', 1)
    cate1_id = request.session.get('cate1_id', 0)
    cate2_id = request.session.get('cate2_id', 0)

    url = '/item/cate?level=%s&cate1=%s&cate2=%s' % (level, cate1_id, cate2_id)

    if cate_list:
        cate = cate_list[0]
    else:
        return HttpResponseRedirect(url)

    if cate_name:
        cate.name = cate_name

    if super_id:
        cate.cate_id = super_id

    try:
        cate.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(url)


# 删除分类
def cate_del(request):
    cate_id = int(request.GET.get('cate_id', 0))

    cate_list = Category.objects.filter(id=cate_id)

    level = request.session.get('level', 1)
    cate1_id = request.session.get('cate1_id', 0)
    cate2_id = request.session.get('cate2_id', 0)

    url = '/item/cate?level=%s&cate1=%s&cate2=%s' % (level, cate1_id, cate2_id)

    if cate_list:
        cate = cate_list[0]
    else:
        return HttpResponseRedirect(url)

    # 查询分类是否包含子类

    try:
        cate.delete()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(url)


# 添加分类
def cate_add(request):
    cate_name = request.GET.get('cate_name', '')
    cate_level = request.GET.get('level', '')
    super_id = request.GET.get('super_id', 0)

    level = request.session.get('level', 1)
    cate1_id = request.session.get('cate1_id', 0)
    cate2_id = request.session.get('cate2_id', 0)

    url = '/item/cate?level=%s&cate1=%s&cate2=%s' % (level, cate1_id, cate2_id)

    if not cate_name:
        return HttpResponseRedirect(url)

    if '一' in cate_level:
        cate_level = 2
    elif '二' in cate_level:
        cate_level = 3
    elif '三' in cate_level:
        cate_level = 4
    else:
        cate_level = 2
    print(cate_name, cate_level)
    cate = Category()
    cate.name = cate_name
    cate.level = cate_level
    if super_id:
        cate.cate_id = super_id

    try:
        cate.save()
    except Exception as e:
        print(e)

    return HttpResponseRedirect(url)
