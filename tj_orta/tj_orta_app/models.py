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


# 审核状态表
# 1-未提交, 2-环保局审核, 3-交管局审核, 4-审核通过, 5-审核不通过
class Status(models.Model):
    name = models.CharField(max_length=50, unique=True)


# 车辆类型表
# 1-大型货车, 2-小型货车, 15-挂式货车
class Type(models.Model):
    name = models.CharField(max_length=50, unique=True)


# 车牌所在地表
class Location(models.Model):
    name = models.CharField(max_length=10, unique=True)
    full_name = models.CharField(max_length=20, null=True, blank=True)


# 车辆表
class Vehicle(models.Model):
    location = models.ForeignKey(Location, null=True, blank=True)           # 车牌所在地
    number = models.CharField(max_length=20)                                # 号牌号码
    engine = models.CharField(max_length=50, null=True, blank=True)         # 发动机型号
    vehicle_type = models.ForeignKey(Type, null=True, blank=True)           # 车辆类型
    vehicle_model = models.CharField(max_length=50, null=True, blank=True)  # 车辆型号
    register_date = models.DateField(null=True, blank=True)                 # 车辆注册日期
    route = models.CharField(max_length=400, null=True, blank=True)         # 路线
    status = models.ForeignKey(Status, default=1)                           # 审核状态
    modify_time = models.DateTimeField(null=True, blank=True)               # 车辆信息修改时间
    submit_time = models.DateTimeField(null=True, blank=True)               # 用户提交时间
    hbj_time = models.DateTimeField(null=True, blank=True)                  # 环保局审核时间
    jgj_time = models.DateTimeField(null=True, blank=True)                  # 交换据审核时间
    enterprise = models.ForeignKey(User, null=True, blank=True)             # 车辆所属企业
    reason = models.CharField(max_length=100, null=True, blank=True)        # 未通过原因
    file_name = models.CharField(max_length=100, null=True, blank=True)     # 通行证完整保存路径
    cert_id = models.CharField(max_length=30, null=True, blank=True)        # 通行证id
