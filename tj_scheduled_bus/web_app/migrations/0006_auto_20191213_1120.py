# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2019-12-13 11:20
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('web_app', '0005_auto_20191213_1100'),
    ]

    operations = [
        migrations.RenameField(
            model_name='department',
            old_name='dpt_address',
            new_name='dept_address',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='dpt_name',
            new_name='dept_name',
        ),
        migrations.RenameField(
            model_name='department',
            old_name='dpt_phone',
            new_name='dept_phone',
        ),
    ]
