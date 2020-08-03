# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from __future__ import unicode_literals

from django.db import models


class TbCarData(models.Model):
    id = models.CharField(primary_key=True, max_length=32)
    hphm = models.CharField(max_length=20, blank=True, null=True)
    hpzl = models.CharField(max_length=10, blank=True, null=True)
    wfdm = models.CharField(max_length=10, blank=True, null=True)
    qssj = models.DateTimeField(blank=True, null=True)
    jzsj = models.DateTimeField(blank=True, null=True)
    crsj = models.DateTimeField(blank=True, null=True)
    gxsj = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'tb_car_data'
