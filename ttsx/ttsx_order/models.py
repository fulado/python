from django.db import models
from app_ttsx.models import UserInfo
from ttsx_goods.models import GoodsInfo
# Create your models here.


class OrderMain(models.Model):
    id = models.CharField(max_length=20, primary_key=True)  # 2017010203987
    user = models.ForeignKey(UserInfo)
    date = models.DateTimeField(auto_now_add=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    state = models.IntegerField(default=0)


class OrderDetail(models.Model):
    order = models.ForeignKey(OrderMain)
    goods = models.ForeignKey(GoodsInfo)
    count = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
