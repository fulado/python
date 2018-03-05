from django.shortcuts import render
from django.http import JsonResponse
from .models import CartInfo
# Create your views here.


def add(request):
    try:
        user_id = request.session.get('user_id')
        goods_id = int(request.GET.get('goods_id'))

        cart = CartInfo()
        cart.user_id = user_id
        cart.goods_id = goods_id
        cart.amount = 1
        cart.save()

        return JsonResponse({'is_add': 1})
    except Exception as e:
        print(e)
        return JsonResponse({'is_add': 0})
