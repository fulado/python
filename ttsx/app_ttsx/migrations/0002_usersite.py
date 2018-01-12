# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_ttsx', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserSite',
            fields=[
                ('id', models.AutoField(serialize=False, auto_created=True, verbose_name='ID', primary_key=True)),
                ('receiver', models.CharField(max_length=50)),
                ('site', models.CharField(max_length=200)),
                ('zip', models.CharField(max_length=20)),
                ('phone', models.CharField(max_length=20)),
                ('user', models.ForeignKey(to='app_ttsx.UserInfo')),
            ],
        ),
    ]
