# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2020-01-18 20:13
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0020_user_locked_vehicle_cnt'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='locked_vehicle_cnt',
            new_name='marked_vehicle_cnt',
        ),
    ]
