from django.db import models
from tj8890_user.models import Dept, User

#  Create your models here.


# 事件类型模型
class Category(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)   # 分类名称
    level = models.IntegerField(null=True, blank=True)              # 分类等级
    cate = models.ForeignKey('self', null=True, blank=True)         # 所属分类


# 事件分类
class Cate(models.Model):
    name = models.CharField(max_length=10, null=True, blank=True)  # 分类名称


# 事项办理状态
class ItemStatus(models.Model):
    status_name = models.CharField(max_length=50, null=True, blank=True)     # 事项状态


#  事件模型
class Item(models.Model):
    id = models.CharField(max_length=50, primary_key=True)                      # 工单编号
    cate = models.ForeignKey(Cate, null=True, blank=True)                       # 求助类别
    person = models.CharField(max_length=20, null=True, blank=True)             # 求助人员
    phone = models.CharField(max_length=20, null=True, blank=True)              # 联系电话
    area = models.CharField(max_length=50, null=True, blank=True)               # 所在区域
    emergency = models.IntegerField(default=1)  # 紧急程度, 1-普通(3天), 2-加急(2天), 3-紧急(当日回复), 4-特急(两小时内回复)
    title = models.CharField(max_length=50, null=True, blank=True)              # 标题
    content = models.CharField(max_length=500, null=True, blank=True)           # 内容
    accept_time = models.DateTimeField(null=True, blank=True)                   # 接件时间
    limit_time = models.DateTimeField(null=True, blank=True)                    # 承办时限
    # 办件状态, 1-未转办, 2-已转办, 3-办理中, 4-已反馈, 5-已超时, 6-退回重办, 7-申请延期, 8-催办，9-退驳 ,66-办结
    status = models.ForeignKey(ItemStatus, null=True, blank=True, default=1)
    assign_dept = models.ForeignKey(Dept, null=True, blank=True)                # 转办部门
    dead_time = models.DateTimeField(null=True, blank=True)                     # 办理时限
    accept_user = models.ForeignKey(User, null=True, blank=True, related_name='accept_user')   # 接收人员
    reject_user = models.ForeignKey(User, null=True, blank=True, related_name='reject_user')   # 回驳人员
    reject_reason = models.CharField(max_length=500, null=True, blank=True)     # 回驳原因
    result = models.CharField(max_length=500, null=True, blank=True)            # 办理情况
    delay_time = models.DateTimeField(null=True, blank=True)                    # 延期时间
    delay_reason = models.CharField(max_length=500, null=True, blank=True)      # 延期原因
    return_reason = models.CharField(max_length=500, null=True, blank=True)     # 退回重办原因
    save_time = models.DateTimeField(null=True, blank=True)                     # 办结时间
    is_exported = models.BooleanField(default=False)                            # 是否已经导出
    approval_content = models.CharField(max_length=500, null=True, blank=True)  # 审批内容
    approval_person = models.CharField(max_length=20, null=True, blank=True)    # 审批人
    cate1 = models.ForeignKey(Category, related_name='cate1', null=True, blank=True)  # 求助类别
    cate2 = models.ForeignKey(Category, related_name='cate2', null=True, blank=True)  # 求助类别
    cate3 = models.ForeignKey(Category, related_name='cate3', null=True, blank=True)  # 求助类别
