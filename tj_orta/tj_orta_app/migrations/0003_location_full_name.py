# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-23 10:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tj_orta_app', '0002_auto_20180423_0959'),
    ]

    operations = [
        migrations.AddField(
            model_name='location',
            name='full_name',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
