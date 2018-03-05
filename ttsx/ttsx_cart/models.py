from django.db import models
from app_ttsx.models import UserInfo

# Create your models here.


class CartInfo(models.Model):
    user = models.ForeignKey(UserInfo)
    goods = models.ForeignKey('ttsx_goods.GoodsInfo')
    amount = models.IntegerField()
