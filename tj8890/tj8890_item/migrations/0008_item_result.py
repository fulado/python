# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-12 11:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tj8890_item', '0007_auto_20180911_2007'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='result',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
    ]
