# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-04-23 11:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('tj_orta_app', '0003_location_full_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='vehicle',
            name='enterprise',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tj_orta_app.User'),
        ),
    ]
