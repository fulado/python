# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-12-28 23:24
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0015_auto_20191228_2322'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='route',
            name='route_station',
        ),
        migrations.AddField(
            model_name='route',
            name='route_station',
            field=models.ManyToManyField(blank=True, null=True, to='web_app.Station'),
        ),
    ]
