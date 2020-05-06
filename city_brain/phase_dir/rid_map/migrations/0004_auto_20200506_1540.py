# Generated by Django 3.0.5 on 2020-05-06 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rid_map', '0003_auto_20200427_1224'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='interrid',
            name='id',
        ),
        migrations.AlterField(
            model_name='custfroad',
            name='id',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='interrid',
            name='rid',
            field=models.CharField(max_length=50, primary_key=True, serialize=False),
        ),
        migrations.CreateModel(
            name='RoadRidMap',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rid', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rid_map.InterRid')),
                ('road', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='rid_map.CustFroad')),
            ],
        ),
    ]
