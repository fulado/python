from django.db import models

# Create your models here.


# 权限表
# 1-企业, 2-环保局, 3-交管局
class Authority(models.Model):
    name = models.CharField(max_length=50, unique=True)


# 用户表
class User(models.Model):
    username = models.CharField(max_length=50, unique=True)                     # 帐号
    password = models.CharField(max_length=50)                                  # 密码
    authority = models.ForeignKey(Authority, null=True, blank=True)             # 权限等级
    enterprise_name = models.CharField(max_length=200, null=True, blank=True)   # 企业名称
    enterprise_phone = models.CharField(max_length=20, null=True, blank=True)   # 企业联系方式
    legal_person = models.CharField(max_length=50, null=True, blank=True)       # 法人
    organization_code = models.CharField(max_length=50, null=True, blank=True)  # 组织机构代码
    contact = models.CharField(max_length=50, null=True, blank=True)            # 联系人
    contact_phone = models.CharField(max_length=20, null=True, blank=True)      # 联系人电话
    limit_number = models.IntegerField(default=1, null=True, blank=True)        # 可申请最大数量通行证
    applied_number = models.IntegerField(default=0, null=True, blank=True)      # 已申请通行证数量
    is_delete = models.BooleanField(default=False)                              # 是否删除



