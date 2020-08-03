from django.shortcuts import render, redirect
from .models import TypeInfo, GoodsInfo
from django.core.paginator import Paginator

# Create your views here.


# 显示商品列表页
def show_list(request, type_id, page_num, order):
    # 列表排序模式, 1-默认, 2-价格, 3-人气
    if order == '2':
        price = request.GET.get('price')
        desc = request.GET.get('desc')
        # print(desc)
        # 如果点击的是"价格"按钮,则每点击一次翻转价格排序的顺序:升序->降序,  降序->升序
        if price == '1':
            if desc == '1':
                desc = '0'
            else:
                desc = '1'
        # 判断按正序或者倒序排列
        if desc == '1':
            order_by = '-price'
        else:
            order_by = 'price'

    elif order == '3':
        order_by = 'count'
        desc = ''
    else:
        order_by = '-id'
        desc = ''

    # print(order_by)

    goods_type = TypeInfo.objects.get(id=type_id)
    recent_goods = goods_type.goodsinfo_set.order_by('-id')[0: 2]
    goods_list = goods_type.goodsinfo_set.order_by(order_by)

    paginator = Paginator(goods_list, 10)

    # 防止当用户给出的page_num超出分页范围
    if int(page_num) < 1:
        page_num = 1
    elif int(page_num) > paginator.num_pages:
        page_num = paginator.num_pages

    begin_page = int(page_num) - 2
    end_page = int(page_num) + 2
    if begin_page < 1:
        begin_page = 1
    if end_page > paginator.num_pages:
        end_page = paginator.num_pages

    page_range = range(begin_page, end_page + 1)

    if begin_page > 1:
        symbol_begin = '1'
    else:
        symbol_begin = '0'

    if end_page < paginator.num_pages:
        symbol_end = '1'
    else:
        symbol_end = '0'

    goods = paginator.page(page_num)

    context = {'title': '商品列表', 'show': '2', 'recent_goods': recent_goods, 'goods': goods,
               'page_range': page_range, 'goods_type': goods_type, 'symbol_begin': symbol_begin,
               'symbol_end': symbol_end, 'order': order, 'desc': desc}
    return render(request, 'goods/list.html', context)


# 显示商品详细信息
def show_detail(request, goods_id):
    # 使用get方法查询数据会抛异常
    try:
        goods = GoodsInfo.objects.get(id=goods_id)
        recent_goods = goods.type.goodsinfo_set.order_by('-id')[0: 2]

        context = {'title': '商品详情', 'show': '2', 'recent_goods': recent_goods, 'goods': goods}
        response = render(request, 'goods/detail.html', context)

        if 'recent_views' in request.COOKIES.keys():
            view_list = request.COOKIES.get('recent_views').split(',')
        else:
            view_list = []

        if goods_id in view_list:
            view_list.remove(goods_id)

        view_list.insert(0, goods_id)
        if len(view_list) > 5:
            view_list.pop()

        response.set_cookie('recent_views', ','.join(view_list))

        return response
    except Exception as e:
        print(e)
        # 有异常跳转到404页面
        return redirect('/404.html')
