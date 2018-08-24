# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2018-08-24 07:13
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('tj8890_user', '0002_auto_20180405_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=50, null=True)),
                ('level', models.IntegerField(blank=True, null=True)),
                ('cate', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tj8890_item.Category')),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.CharField(max_length=50, primary_key=True, serialize=False)),
                ('order_id', models.CharField(blank=True, max_length=50, null=True)),
                ('source', models.CharField(blank=True, max_length=50, null=True)),
                ('sh_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('sh_person', models.CharField(blank=True, max_length=50, null=True)),
                ('c_phone', models.CharField(blank=True, max_length=20, null=True)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
                ('sex', models.CharField(blank=True, max_length=10, null=True)),
                ('area', models.CharField(blank=True, max_length=50, null=True)),
                ('d_address', models.CharField(blank=True, max_length=200, null=True)),
                ('p_address', models.CharField(blank=True, max_length=200, null=True)),
                ('work_place', models.CharField(blank=True, max_length=50, null=True)),
                ('recorder', models.CharField(blank=True, max_length=20, null=True)),
                ('recd_time', models.DateTimeField(blank=True, null=True)),
                ('emergency', models.IntegerField(default=1)),
                ('is_redeliver', models.BooleanField(default=False)),
                ('content', models.CharField(blank=True, max_length=500, null=True)),
                ('is_redeal', models.BooleanField(default=False)),
                ('r_unit', models.CharField(blank=True, max_length=50, null=True)),
                ('attribute', models.CharField(blank=True, max_length=50, null=True)),
                ('title', models.CharField(blank=True, max_length=50, null=True)),
                ('summary', models.CharField(blank=True, max_length=500, null=True)),
                ('is_assist', models.BooleanField(default=False)),
                ('deliver_time', models.DateTimeField(blank=True, null=True)),
                ('receive_time', models.DateTimeField(blank=True, null=True)),
                ('receive_limit', models.DateTimeField(blank=True, null=True)),
                ('deal_limit', models.DateTimeField(blank=True, null=True)),
                ('is_overtime', models.BooleanField(default=False)),
                ('comment', models.CharField(blank=True, max_length=500, null=True)),
                ('leader_comment', models.CharField(blank=True, max_length=500, null=True)),
                ('result', models.CharField(blank=True, max_length=500, null=True)),
                ('complete_time', models.DateTimeField(blank=True, null=True)),
                ('deal_person', models.CharField(blank=True, max_length=20, null=True)),
                ('is_delay', models.BooleanField(default=False)),
                ('is_remind', models.BooleanField(default=False)),
                ('is_reply', models.BooleanField(default=False)),
                ('reply_content', models.CharField(blank=True, max_length=500, null=True)),
                ('return_reason', models.CharField(blank=True, max_length=50, null=True)),
                ('return_time', models.DateTimeField(blank=True, null=True)),
                ('revisit_time', models.DateTimeField(blank=True, null=True)),
                ('evaluation', models.CharField(blank=True, max_length=200, null=True)),
                ('revisit_content', models.CharField(blank=True, max_length=500, null=True)),
                ('is_archived', models.BooleanField(default=False)),
                ('archive_reason', models.CharField(blank=True, max_length=50, null=True)),
                ('check_result', models.CharField(blank=True, max_length=50, null=True)),
                ('check_comments', models.CharField(blank=True, max_length=500, null=True)),
                ('check_time', models.DateTimeField(blank=True, null=True)),
                ('industry', models.CharField(blank=True, max_length=50, null=True)),
                ('name', models.CharField(blank=True, max_length=20, null=True)),
                ('is_scene', models.BooleanField(default=False)),
                ('is_delete', models.BooleanField(default=False)),
                ('is_urge', models.BooleanField(default=False)),
                ('agency_dept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='agency_dept_set', to='tj8890_user.Dept')),
                ('assign_dept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assign_dept_set', to='tj8890_user.Dept')),
                ('assist_dept', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='assist_dept_set', to='tj8890_user.Dept')),
                ('category1', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category1_set', to='tj8890_item.Category')),
                ('category2', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category2_set', to='tj8890_item.Category')),
                ('category3', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category3_set', to='tj8890_item.Category')),
                ('category4', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category4_set', to='tj8890_item.Category')),
                ('check_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='check_person_set', to='tj8890_user.User')),
                ('receiver', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='receiver_set', to='tj8890_user.User')),
                ('return_approver', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='return_approver_set', to='tj8890_user.User')),
                ('return_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='return_person_set', to='tj8890_user.User')),
                ('revisit_person', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='revisit_person_set', to='tj8890_user.User')),
            ],
        ),
        migrations.CreateModel(
            name='ItemStatus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status_name', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='item',
            name='status',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='tj8890_item.ItemStatus'),
        ),
    ]
