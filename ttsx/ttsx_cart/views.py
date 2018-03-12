from django.shortcuts import render
from django.http import JsonResponse
from .models import CartInfo
from django.db.models import Sum
from app_ttsx.decorator import login_check
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
def cart(request):
    user_id = request.session.get('user_id')
    carts = CartInfo.objects.filter(user_id=user_id)
    context = {'carts': carts, 'title': '购物车', 'show': '1'}
    return render(request, 'cart/cart.html', context)
