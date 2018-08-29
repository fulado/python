from django.shortcuts import render
from tj8890_item.models import Category
from .models import Information

import time

# Create your views here.


# 显示所有知识页面
def all_show(request):
    # 获得查询知识提交的信息
    cate1 = int(request.GET.get('cate1', 0))
    cate2 = int(request.GET.get('cate2', 0))
    cate3 = int(request.GET.get('cate3', 0))
    cate4 = int(request.GET.get('cate4', 0))
    recd_time_begin = request.GET.get('recd_time_begin', '0')
    recd_time_end = request.GET.get('recd_time_end', '0')
    keyword = request.GET.get('keyword', '')

    if recd_time_begin == '0':
        recd_time_begin = time.strftime('%Y-01-01', time.localtime())
    if recd_time_end == '0':
        recd_time_end = time.strftime('%Y-%m-%d', time.localtime())

    # 将检索信息保存到session
    request.session['cate1'] = cate1
    request.session['cate2'] = cate2
    request.session['cate3'] = cate3
    request.session['cate4'] = cate4
    request.session['recd_time_begin'] = recd_time_begin
    request.session['recd_time_end'] = recd_time_end
    request.session['keyword'] = keyword

    # 事项分类
    cate1_list = Category.objects.filter(level=1)
    cate2_list = Category.objects.filter(level=2)
    cate3_list = Category.objects.filter(cate_id=cate2)
    cate4_list = Category.objects.filter(cate_id=cate3)

    # 查询事项全部知识
    info_list = Information.objects.all().order_by('-upload_time')

    # 按照表单中的的信息进行过滤
    info_list = info_list.filter(recd_time__gte=recd_time_begin)
    info_list = info_list.filter(recd_time__lte=recd_time_end)

    if cate1 != 0:
        info_list = info_list.filter(category1_id=cate1)
    if cate2 != 0:
        info_list = info_list.filter(category2_id=cate2)
    if cate3 != 0:
        info_list = info_list.filter(category3_id=cate3)
    if cate4 != 0:
        info_list = info_list.filter(category4_id=cate4)

    return render(request, 'info/all.html')


# 显示知识详情页面
def detail_show(request):
    return render(request, 'info/detail.html')
