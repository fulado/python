# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('dept_name', models.CharField(max_length=255)),
                ('is_delete', models.BooleanField(default=False)),
                ('supervisor', models.ForeignKey(to='tj8890_user.Dept')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('real_name', models.CharField(max_length=50)),
                ('is_delete', models.BooleanField(default=False)),
                ('dept', models.ForeignKey(to='tj8890_user.Dept')),
            ],
        ),
    ]
