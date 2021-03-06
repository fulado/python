# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-03-23 08:02
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Authority',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('auth', models.CharField(max_length=255)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Dept',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_delete', models.BooleanField(default=False)),
                ('supervisor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tj8890_user.Dept')),
            ],
        ),
        migrations.CreateModel(
            name='Duty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('is_delete', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=50)),
                ('password', models.CharField(max_length=50)),
                ('real_name', models.CharField(max_length=50)),
                ('duty', models.CharField(blank=True, max_length=50, null=True)),
                ('number', models.CharField(blank=True, max_length=50, null=True)),
                ('phone', models.CharField(blank=True, max_length=20, null=True)),
                ('authority', models.IntegerField(default=3)),
                ('is_delete', models.BooleanField(default=False)),
                ('dept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tj8890_user.Dept')),
            ],
        ),
    ]
