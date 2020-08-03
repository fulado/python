from django.shortcuts import render
from django.http import JsonResponse
from .models import CartInfo
from app_ttsx.decorator import login_check
from app_ttsx.models import UserSite
# Create your views here.


def add(request):
    try:
        user_id = request.session.get('user_id')
        goods_id = int(request.GET.get('goods_id'))
        num = int(request.GET.get('num', 1))

        cart_list = CartInfo.objects.filter(user_id=user_id, goods_id=goods_id)
        if len(cart_list) == 0:
            cart = CartInfo()
            cart.user_id = user_id
            cart.goods_id = goods_id
            cart.amount = num

        else:
            cart = cart_list[0]
            cart.amount += num

        cart.save()

        return JsonResponse({'is_add': 1})
    except Exception as e:
        print(e)
        return JsonResponse({'is_add': 0})


def cart_count(request):
    user_id = request.session.get('user_id')
    count = CartInfo.objects.filter(user_id=user_id).count()

    return JsonResponse({'count': count})


# 显示购物车
@login_check
def cart_show(request):
    user_id = request.session.get('user_id')
    carts = CartInfo.objects.filter(user_id=user_id)
    context = {'carts': carts, 'title': '购物车', 'show': '1'}
    return render(request, 'cart/cart.html', context)


# 修改购物车中商品数量
def modify(request):
    cart_id = request.GET.get('cart_id', '0')
    num = request.GET.get('num', '0')
    cart_list = CartInfo.objects.filter(id=cart_id)

    if len(cart_list) > 0:
        cart = cart_list[0]
        cart.amount = num
        cart.save()
        return JsonResponse({'ok': True})
    else:
        return JsonResponse({'ok': False})


# 删除购物车中商品
def del_cart(request):
    # 获取购物车id
    cart_id = int(request.GET.get('cart_id', '0'))
    if cart_id > 0:
        cart_list = CartInfo.objects.filter(id=cart_id)
    else:
        return JsonResponse({'ok': False})

    if len(cart_list) > 0:
        cart_list[0].delete()
        return JsonResponse({'ok': True})
    else:
        return JsonResponse({'ok': False})


# 显示提交订单页面
@login_check
def order(request):
    # 获取用户id
    user_id = request.session.get('user_id', '0')
    if user_id == '0':
        return render(request, '404.html')

    # 获取用户地址
    site_list = UserSite.objects.filter(user_id=user_id)
    if len(site_list) == 0:
        site_list = ['']

    # 获取用户选择的购物车
    id_list = request.POST.getlist('select')
    id_list_str = ','.join(id_list)
    if len(id_list) == 0:
        return render(request, '404.html')
    cart_list = CartInfo.objects.filter(id__in=id_list)
    if len(cart_list) == 0:
        return render(request, '404.html')

    context = {'title': '提交订单', 'show': '1', 'site': site_list[0], 'cart_list': cart_list, 'id_list_str': id_list_str}
    return render(request, 'cart/place_order.html', context)
