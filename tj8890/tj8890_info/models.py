from django.db import models

from tj8890_user.models import User

# Create your models here.


# 知识库数据
class Information(models.Model):
    info_name = models.CharField(max_length=50, null=True, blank=True)   # 事项名称
    info_abstract = models.CharField(max_length=200, null=True, blank=True)   # 事项摘要
    info_content = models.CharField(max_length=500, null=True, blank=True)   # 事项内容
    upload_user = models.ForeignKey(User, null=True, blank=True)  # 上传人员
    upload_time = models.DateTimeField(null=True, blank=True)     # 上传时间

