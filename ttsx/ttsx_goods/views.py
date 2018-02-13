from django.shortcuts import render

# Create your views here.


def show_list(request):
    context = {'title': '商品列表', 'show': '2'}
    return render(request, 'goods/list.html', context)


def show_detail(request):
    context = {'title': '商品详情', 'show': '2'}
    return render(request, 'goods/list.html', context)
