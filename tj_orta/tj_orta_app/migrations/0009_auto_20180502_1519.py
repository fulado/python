# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-02 15:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tj_orta_app', '0008_auto_20180424_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='applied_number',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='limit_number',
            field=models.IntegerField(blank=True, default=1, null=True),
        ),
    ]