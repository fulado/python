# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-05-25 18:29
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tj_orta_app', '0011_backup1'),
    ]

    operations = [
        migrations.AddField(
            model_name='backup1',
            name='file_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]