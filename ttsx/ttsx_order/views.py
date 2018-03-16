from django.shortcuts import render
from ttsx_cart.models import CartInfo
from .models import OrderMain, OrderDetail
from django.db import transaction
import time

# Create your views here.


# 处理订单
'''
1 接收提交订单中商品信息(id, 数量)
2 生成主订单对象
    2.1 主订单id: 时间+用户id
    2.2 计算总价(在生成详细订单数据时同步计算)
3 生成详细订单对象
    3.1 购买商品, 数量, 价格(单价)
    3.2 判断商品数量是否小于等于库存, 是继续生成订单, 否取消反馈购物车页面
    3.3 计算总价
4 操作数据库
    4.1 设置事务回滚点
    4.2 写入订单数据库(主表, 详单表)
    4.3 删除购物车中的数据
    4.4 修改商品表中的库存数量
    4.5 如有异常则事务回滚
5 跳转到用户中心--订单页面
'''
@transaction.atomic
def order_handler(request):
    # 4.1 设置事务回滚点
    sid = transaction.savepoint()
    try:
        # 1 接收提交订单中的商品信息
        id_list = request.POST.get('id_list').split(',')
        cart_list = CartInfo.objects.filter(id__in=id_list)
        # 2 生成主订单
        order_main = OrderMain()
        user_id = request.session.get('user_id')
        order_main.id = "%s%d" % (time.strftime("%Y%m%d%H%M%S", time.localtime()), user_id)
        order_main.user_id = user_id
        order_main.state = 1  # 1- 订单生成, 未支付; 2- 已支付; 3- 已发货; 4- 已收货; 5- 申请退货; 6- 已收到退货, 退款中;
        # 7- 已退款; 8- 申请换货; 9- 收到换货, 未发新货;
        order_main.total = 0
        order_main.save()

        # 3 生成详单
        for cart in cart_list:
            if cart.amount <= cart.goods.stored:
                order_detail = OrderDetail()
                order_detail.order_id = order_main.id
                order_detail.goods = cart.goods
                order_detail.count = cart.amount
                order_detail.price = cart.goods.price
                order_detail.save()
                cart.delete()  # 删除购物车中的商品
                order_main.total += order_detail.count * order_detail.price

                # 修改商品的库存
                cart.goods.stored -= cart.amount
                cart.goods.save()
            else:
                context = {'info': '库存不足'}
                return render(request, 'cart/cart.html', context)

        # 4 操作数据库
        order_main.save()
        # 事务提交
        transaction.savepoint_commit(sid)
        return render(request, 'app_ttsx/user_center_order.html')
    except Exception as e:
        print(e)
        # 出现异常, 事务回滚
        transaction.savepoint_rollback(sid)
        context = {'info': '订单为生成, 请重试'}
        return render(request, 'cart/cart.html', context)
