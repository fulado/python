# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-23 20:38
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tj_orta_app', '0006_vehicle_file_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='cert_id',
            field=models.CharField(blank=True, max_length=30, null=True),
        ),
    ]