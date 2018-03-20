from django.db import models

# Create your models here.


# 部门模型
class Dept(models.Model):
    dept_name = models.CharField(max_length=255)
    supervisor = models.ForeignKey('self')
    is_delete = models.BooleanField(default=False)


# 用户模型
class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    real_name = models.CharField(max_length=50)
    dept = models.ForeignKey(Dept)
    is_delete = models.BooleanField(default=False)
