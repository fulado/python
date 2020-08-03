# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_ttsx', '0002_usersite'),
        ('ttsx_goods', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OrderDetail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('count', models.IntegerField()),
                ('price', models.DecimalField(max_digits=10, decimal_places=2)),
                ('goods', models.ForeignKey(to='ttsx_goods.GoodsInfo')),
            ],
        ),
        migrations.CreateModel(
            name='OrderMain',
            fields=[
                ('id', models.CharField(max_length=20, primary_key=True, serialize=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('total', models.DecimalField(max_digits=10, decimal_places=2)),
                ('state', models.IntegerField(default=0)),
                ('user', models.ForeignKey(to='app_ttsx.UserInfo')),
            ],
        ),
        migrations.AddField(
            model_name='orderdetail',
            name='order',
            field=models.ForeignKey(to='ttsx_order.OrderMain'),
        ),
    ]
