# Generated by Django 3.0.5 on 2020-05-07 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rid_map', '0009_auto_20200507_2100'),
    ]

    operations = [
        migrations.AddField(
            model_name='roadridmap',
            name='cust_froad_id',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='roadridmap',
            name='cust_signal_id',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]