# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-09-12 14:21
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tj8890_item', '0008_item_result'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='delay_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]