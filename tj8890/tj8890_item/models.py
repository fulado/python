from django.db import models
from tj8890_user.models import Dept, User

#  Create your models here.


# 事件类型模型
class Category(models.Model):
    name = models.CharField(max_length=50, null=True, blank=True)   # 分类名称
    level = models.IntegerField(null=True, blank=True)              # 分类等级
    cate = models.ForeignKey('self', null=True, blank=True)         # 所属分类


# 事项办理状态
class ItemStatus(models.Model):
    status_name = models.CharField(max_length=50, null=True, blank=True)     # 事项状态


#  事件模型
class Item(models.Model):
    id = models.CharField(max_length=50, primary_key=True)              # 自动生成事件id
    order_id = models.CharField(max_length=50, null=True, blank=True)   # 工单编号
    source = models.CharField(max_length=50, null=True, blank=True)     # 求助来源
    category1 = models.ForeignKey(Category, null=True, blank=True, related_name='category1_set')  # 求助类别1
    category2 = models.ForeignKey(Category, null=True, blank=True, related_name='category2_set')  # 求助类别2
    category3 = models.ForeignKey(Category, null=True, blank=True, related_name='category3_set')  # 求助类别3
    category4 = models.ForeignKey(Category, null=True, blank=True, related_name='category4_set')  # 求助类别4
    sh_phone = models.CharField(max_length=20, null=True, blank=True)   # 求租号码
    sh_person = models.CharField(max_length=50, null=True, blank=True)  # 求助人员
    c_phone = models.CharField(max_length=20, null=True, blank=True)    # 联系电话
    fax = models.CharField(max_length=20, null=True, blank=True)        # 传真
    sex = models.CharField(max_length=10, null=True, blank=True)        # 性别
    area = models.CharField(max_length=50, null=True, blank=True)       # 所在区域
    d_address = models.CharField(max_length=200, null=True, blank=True)  # 详细地址
    p_address = models.CharField(max_length=200, null=True, blank=True)  # 通讯地址
    work_place = models.CharField(max_length=50, null=True, blank=True)  # 工作单位
    recorder = models.CharField(max_length=20, null=True, blank=True)   # 录入人员
    recd_time = models.DateTimeField(null=True, blank=True)             # 录入时间
    emergency = models.IntegerField(default=1)  # 紧急程度, 1-普通(3天), 2-加急(2天), 3-紧急(当日回复), 4-特急(两小时内回复)
    is_redeliver = models.BooleanField(default=False)                   # 是否重派
    content = models.CharField(max_length=500, null=True, blank=True)   # 反映内容
    is_redeal = models.BooleanField(default=False)                      # 是否重办
    r_unit = models.CharField(max_length=50, null=True, blank=True)     # 被反映单位
    attribute = models.CharField(max_length=50, null=True, blank=True)  # 问题属性
    title = models.CharField(max_length=50, null=True, blank=True)      # 标题
    summary = models.CharField(max_length=500, null=True, blank=True)   # 内容摘要
    assign_dept = models.ForeignKey(Dept, null=True, blank=True, related_name='assign_dept_set')  # 指派承办部门
    agency_dept = models.ForeignKey(Dept, null=True, blank=True, related_name='agency_dept_set')  # 承办部门/牵头部门
    is_assist = models.BooleanField(default=False)                      # 是否协办
    assist_dept = models.ForeignKey(Dept, null=True, blank=True, related_name='assist_dept_set')  # 协办部门
    deliver_time = models.DateTimeField(null=True, blank=True)          # 派单时间
    receiver = models.ForeignKey(User, null=True, blank=True, related_name='receiver_set')  # 接件人员
    receive_time = models.DateTimeField(null=True, blank=True)          # 接件时间
    receive_limit = models.DateTimeField(null=True, blank=True)         # 接单时限
    deal_limit = models.DateTimeField(null=True, blank=True)            # 承办时限
    # status = models.IntegerField(default=0)
    status = models.ForeignKey(ItemStatus, null=True, blank=True, default=0)       # 办件状态, 1-未转办, 2-已转办, 3-办理中, 4-已反馈, 5-已超时, 6-退回重办, 7-申请延期
    is_overtime = models.BooleanField(default=False)                    # 是否超时
    comment = models.CharField(max_length=500, null=True, blank=True)   # 拟办意见
    leader_comment = models.CharField(max_length=500, null=True, blank=True)  # 领导批示
    result = models.CharField(max_length=500, null=True, blank=True)    # 办理结果
    complete_time = models.DateTimeField(null=True, blank=True)         # 办结时间
    deal_person = models.CharField(max_length=20, null=True, blank=True)  # 办理人员
    is_delay = models.BooleanField(default=False)                       # 是否延期
    is_remind = models.BooleanField(default=False)                      # 是否催办
    is_reply = models.BooleanField(default=False)                       # 是否回复市民
    reply_content = models.CharField(max_length=500, null=True, blank=True)  # 市民回复内容
    return_approver = models.ForeignKey(User, null=True, related_name='return_approver_set')  # 退回批准人
    return_reason = models.CharField(max_length=50, null=True, blank=True)  # 退回原因
    return_person = models.ForeignKey(User, null=True, blank=True, related_name='return_person_set')  # 退回人
    return_time = models.DateTimeField(null=True, blank=True)           # 退回时间
    revisit_time = models.DateTimeField(null=True, blank=True)          # 回访时间
    revisit_person = models.ForeignKey(User, null=True, blank=True, related_name='revisit_person_set')  # 回访人
    evaluation = models.CharField(max_length=200, null=True, blank=True)  # 评价结果
    revisit_content = models.CharField(max_length=500, null=True, blank=True)  # 回访内容
    is_archived = models.BooleanField(default=False)  # 是否直接归档
    archive_reason = models.CharField(max_length=50, null=True, blank=True)  # 直接归档理由
    check_result = models.CharField(max_length=50, null=True, blank=True)  # 审核结果
    check_comments = models.CharField(max_length=500, null=True, blank=True)  # 审核意见
    check_person = models.ForeignKey(User, null=True, blank=True, related_name='check_person_set')  # 审核人
    check_time = models.DateTimeField(null=True, blank=True)            # 审核时间
    industry = models.CharField(max_length=50, null=True, blank=True)   # 所属行业
    name = models.CharField(max_length=20, null=True, blank=True)       # 姓名/名称
    is_scene = models.BooleanField(default=False)                       # 是否出现场
    is_delete = models.BooleanField(default=False)                      # 是否删除
