# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-01-18 19:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0019_stationcount'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='locked_vehicle_cnt',
            field=models.IntegerField(default=0),
        ),
    ]
