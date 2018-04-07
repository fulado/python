from django.db import models

# Create your models here.


# 部门模型
class Dept(models.Model):
    name = models.CharField(max_length=255)
    supervisor = models.ForeignKey('self', null=True, blank=True)
    is_delete = models.BooleanField(default=False)


# 用户模型
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    real_name = models.CharField(max_length=50)
    dept = models.ForeignKey(Dept, null=True, blank=True)
    duty = models.CharField(max_length=50, null=True, blank=True)
    number = models.CharField(max_length=50, null=True, blank=True)  # 警号
    phone = models.CharField(max_length=20, null=True, blank=True)
    authority = models.IntegerField(default=3)  # 权限等级
    is_delete = models.BooleanField(default=False)
