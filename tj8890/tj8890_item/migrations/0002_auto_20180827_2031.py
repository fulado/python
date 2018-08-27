# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-27 20:31
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tj8890_item', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='item',
            name='is_urge',
        ),
        migrations.AddField(
            model_name='item',
            name='delay_apply_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='delay_reason',
            field=models.CharField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='delay_to_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
